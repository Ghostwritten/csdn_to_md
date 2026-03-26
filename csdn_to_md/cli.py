import argparse
import os
import sys

from .config import configure_logging
from .exceptions import CSDNExportError
from .exporter import CSDNExporter
from .http_client import HttpClient


def parse_args():
    parser = argparse.ArgumentParser(description="批量导出 CSDN 文章为 Markdown")
    parser.add_argument("-i", "--id", dest="csdn_id", type=str, required=True, help="CSDN 用户名")
    parser.add_argument("--cookie", dest="cookie", type=str, help="CSDN 登录后的 Cookie")
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        type=str,
        default=".",
        help="Markdown 输出目录，默认为当前目录",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="输出调试日志")
    parser.add_argument(
        "--no-images",
        dest="no_images",
        action="store_true",
        help="跳过图片下载，保留原始远程链接",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logger = configure_logging(args.verbose)
    cookie = args.cookie or os.getenv("CSDN_COOKIE")

    exporter = CSDNExporter(HttpClient(cookie=cookie, logger=logger), logger)

    try:
        failed_articles = exporter.export_markdown(
            args.csdn_id, cookie, args.output_dir, download_images=not args.no_images
        )
    except CSDNExportError as exc:
        logger.error(str(exc))
        sys.exit(1)

    if failed_articles:
        sys.exit(2)