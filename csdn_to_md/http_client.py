import time

from curl_cffi import requests

from .config import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT, MAX_RETRIES
from .exceptions import CSDNExportError


class HttpClient:
    def __init__(self, cookie=None, logger=None):
        self.logger = logger
        self.session = requests.Session(impersonate="chrome131")
        self.session.headers.update({
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        if cookie:
            self.session.headers.update({"Cookie": cookie})

    def get(self, url, *, timeout=DEFAULT_TIMEOUT, expect_json=False, referer=None):
        last_error = None
        headers = {"Referer": referer} if referer else {}
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.get(url, timeout=timeout, headers=headers)
                response.raise_for_status()
                if expect_json:
                    return response.json()
                return response
            except (requests.RequestsError, ValueError) as exc:
                last_error = exc
                if attempt == MAX_RETRIES:
                    break
                if self.logger:
                    self.logger.warning("请求失败，%s 秒后重试: %s", attempt, url)
                time.sleep(attempt)
        raise CSDNExportError(f"请求失败: {url}; 原因: {last_error}")