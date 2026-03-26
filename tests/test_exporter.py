import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from csdn_to_md.exporter import CSDNExporter


class DummyLogger:
    def info(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def error(self, *args, **kwargs):
        return None


class DummyHttpClient:
    def __init__(self, payloads):
        self.payloads = payloads

    def get(self, url, *, timeout=None, expect_json=False, referer=None):
        payload = self.payloads[url]
        if expect_json:
            return payload
        return payload


class DummyResponse:
    def __init__(self, content):
        self.content = content.encode("utf-8")


class ExporterTestCase(unittest.TestCase):
    def test_export_markdown_writes_file(self):
        homepage = '<a class="special-column-name" href="https://blog.csdn.net/category_1.html">Python</a>'
        column_page = '<span class="special-column-num">1篇</span><ul class="column_article_list"><li><a target="_blank" href="https://blog.csdn.net/user/article/details/123"></a><h2 class="title">demo title</h2></li></ul>'
        article_payload = {"code": 200, "data": {"markdowncontent": "content@[toc]"}}

        payloads = {
            "https://blog.csdn.net/demo": DummyResponse(homepage),
            "https://blog.csdn.net/category_1.html": DummyResponse(column_page),
            "https://blog-console-api.csdn.net/v1/editor/getArticle?id=123": article_payload,
        }

        exporter = CSDNExporter(DummyHttpClient(payloads), DummyLogger())

        with TemporaryDirectory() as temp_dir:
            failures = exporter.export_markdown("demo", "cookie", temp_dir)
            output_file = Path(temp_dir) / "demo" / "Python" / "demo_title.md"
            self.assertEqual(failures, [])
            self.assertTrue(output_file.exists())
            self.assertEqual(output_file.read_text(encoding="utf-8"), "content")


if __name__ == "__main__":
    unittest.main()