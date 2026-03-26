import unittest

from csdn_to_md.utils import extract_article_id, sanitize_name


class UtilsTestCase(unittest.TestCase):
    def test_sanitize_name_replaces_invalid_chars(self):
        # INVALID_FILENAME_CHARS 使用 + 量词，连续非法字符合并为单个 _
        self.assertEqual(sanitize_name('a:b/c*?"<>|'), "a_b_c_")

    def test_extract_article_id(self):
        self.assertEqual(
            extract_article_id("https://blog.csdn.net/user/article/details/123456789"),
            "123456789",
        )


if __name__ == "__main__":
    unittest.main()