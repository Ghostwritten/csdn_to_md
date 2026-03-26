import logging
import re


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
)
DEFAULT_TIMEOUT = 15
MAX_RETRIES = 3
ARTICLES_PER_PAGE = 40
INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|\r\n]+')
ARTICLE_ID_PATTERN = re.compile(r"/article/details/(\d+)")
LOGGER_NAME = "csdn_to_md"


def configure_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    return logging.getLogger(LOGGER_NAME)