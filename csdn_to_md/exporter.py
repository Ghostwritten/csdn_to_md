import math
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup

from .config import ARTICLES_PER_PAGE
from .exceptions import CSDNExportError
from .models import BlogArticle, BlogColumn, FailedArticle
from .utils import build_output_root, ensure_directory, extract_article_id, sanitize_name

_IMAGE_PATTERN = re.compile(r"(!\[([^\]]*)\])\((https?://[^)\s\"]+)\)")
_VALID_IMAGE_EXTS = frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"})
_CONTENT_TYPE_TO_EXT: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "image/bmp": ".bmp",
}


class CSDNExporter:
    def __init__(self, http_client, logger):
        self.http_client = http_client
        self.logger = logger

    def fetch_blog_columns(self, csdn_id, output_root):
        homepage_url = f"https://blog.csdn.net/{csdn_id}"
        response = self.http_client.get(homepage_url, referer="https://blog.csdn.net/")
        parsed = BeautifulSoup(response.content, "html.parser")
        column_links = parsed.find_all("a", attrs={"class": "special-column-name"})

        columns = []
        seen_urls = set()

        for link in column_links:
            href = link.get("href", "").strip()
            if not href or href in seen_urls:
                continue

            seen_urls.add(href)
            column_name = sanitize_name(link.get_text(strip=True))
            ensure_directory(output_root / column_name)

            column_response = self.http_client.get(href, referer=homepage_url)
            column_page = BeautifulSoup(column_response.content, "html.parser")
            count_node = column_page.find("span", attrs={"class": "special-column-num"})
            article_count = 0
            if count_node:
                count_match = re.search(r"(\d+)", count_node.get_text(strip=True))
                if count_match:
                    article_count = int(count_match.group(1))

            columns.append(BlogColumn(url=href, name=column_name, article_count=article_count))

        return columns

    def append_blog_info(self, blog_column_url, blog_column_name, blogs, seen_article_urls):
        response = self.http_client.get(blog_column_url, referer=f"https://blog.csdn.net/")
        parsed = BeautifulSoup(response.content, "html.parser")
        article_lists = parsed.find_all("ul", attrs={"class": "column_article_list"})

        for article_list in article_lists:
            for blog_info in article_list.find_all("li"):
                link = blog_info.find("a", attrs={"target": "_blank"})
                title_node = blog_info.find("h2", attrs={"class": "title"})
                if not link or not title_node:
                    continue

                blog_url = link.get("href", "").strip()
                if not blog_url or blog_url in seen_article_urls:
                    continue

                seen_article_urls.add(blog_url)
                blog_title = sanitize_name(title_node.get_text(strip=True).replace(" ", "_"))
                blogs.append(BlogArticle(column=blog_column_name, url=blog_url, title=blog_title))

        return blogs

    def fetch_blog_list(self, csdn_id, output_root):
        columns = self.fetch_blog_columns(csdn_id, output_root)
        blogs = []
        seen_article_urls = set()

        for column in columns:
            if column.article_count > ARTICLES_PER_PAGE:
                page_num = math.ceil(column.article_count / ARTICLES_PER_PAGE)
                for page_index in range(page_num, 0, -1):
                    page_url = f"{column.url.rsplit('.html', 1)[0]}_{page_index}.html"
                    self.append_blog_info(page_url, column.name, blogs, seen_article_urls)
            else:
                self.append_blog_info(column.url, column.name, blogs, seen_article_urls)

        return blogs

    def fetch_markdown(self, article_id):
        url = f"https://blog-console-api.csdn.net/v1/editor/getArticle?id={article_id}"
        payload = self.http_client.get(url, expect_json=True)

        if payload.get("code") not in (200, 0):
            message = payload.get("msg") or payload.get("message") or "未知错误"
            raise CSDNExportError(f"文章接口返回失败: {message}")

        data = payload.get("data") or {}
        content = data.get("markdowncontent")
        if not content:
            raise CSDNExportError("接口未返回 markdowncontent，可能是 Cookie 已失效")

        return content.replace("@[toc]", "")

    def _resolve_image_ext(self, url: str, response) -> str:
        """从 URL path 或响应 Content-Type 推断图片扩展名，保底返回 .jpg。"""
        ext = Path(unquote(urlparse(url).path)).suffix.lower()
        if ext in _VALID_IMAGE_EXTS:
            return ext
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
        return _CONTENT_TYPE_TO_EXT.get(content_type, ".jpg")

    def _download_images(self, content: str, images_dir: Path, article_id: str) -> str:
        """解析 markdown 中的远程图片链接，下载到 images/ 目录，按文章 ID 顺序命名后替换链接。

        命名规则：{article_id}_{序号:02d}.{ext}，例如 12345678_01.png
        """
        counter = 0
        ensure_directory(images_dir)

        def replace_image(match: re.Match) -> str:
            nonlocal counter
            prefix = match.group(1)  # ![alt]
            url = match.group(3)

            try:
                response = self.http_client.get(url)
            except CSDNExportError as exc:
                self.logger.warning("图片下载失败: %s; 原因: %s", url, exc)
                return match.group(0)  # 保留原始链接

            counter += 1
            ext = self._resolve_image_ext(url, response)
            filename = f"{article_id}_{counter:02d}{ext}"
            local_path = images_dir / filename

            if not local_path.exists():
                local_path.write_bytes(response.content)
                self.logger.debug("图片已下载: %s", filename)

            return f"{prefix}(./images/{filename})"

        return _IMAGE_PATTERN.sub(replace_image, content)

    def export_markdown(self, csdn_id, cookie, output_dir, download_images=True):
        if not cookie:
            raise CSDNExportError("缺少 CSDN Cookie，请通过 --cookie 或环境变量 CSDN_COOKIE 提供")

        root_dir = build_output_root(output_dir, csdn_id)
        blogs = self.fetch_blog_list(csdn_id, root_dir)
        success_count = 0
        failed_articles = []

        for blog in blogs:
            try:
                article_id = extract_article_id(blog.url)
                content = self.fetch_markdown(article_id)
                article_path = root_dir / blog.column / f"{blog.title}.md"
                ensure_directory(article_path.parent)
                if download_images:
                    images_dir = article_path.parent / "images"
                    content = self._download_images(content, images_dir, article_id)
                article_path.write_text(content, encoding="utf-8")
                success_count += 1
                self.logger.info("download blog markdown blog:【%s】%s", blog.column, blog.title)
            except (CSDNExportError, OSError) as exc:
                failed_articles.append(FailedArticle(url=blog.url, reason=str(exc)))
                self.logger.error("导出失败: %s; 原因: %s", blog.url, exc)

        self.logger.info(
            "导出完成，总数: %s，成功: %s，失败: %s",
            len(blogs),
            success_count,
            len(failed_articles),
        )
        return failed_articles