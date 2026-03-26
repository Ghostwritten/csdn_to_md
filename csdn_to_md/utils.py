from pathlib import Path

from .config import ARTICLE_ID_PATTERN, INVALID_FILENAME_CHARS
from .exceptions import CSDNExportError


def sanitize_name(name):
    cleaned = INVALID_FILENAME_CHARS.sub("_", name).strip().strip(".")
    return cleaned or "untitled"


def ensure_directory(path):
    path.mkdir(parents=True, exist_ok=True)


def extract_article_id(article_url):
    match = ARTICLE_ID_PATTERN.search(article_url)
    if not match:
        raise CSDNExportError(f"无法从文章链接中提取 article id: {article_url}")
    return match.group(1)


def build_output_root(output_dir, csdn_id):
    root_dir = Path(output_dir).resolve() / sanitize_name(csdn_id)
    ensure_directory(root_dir)
    return root_dir