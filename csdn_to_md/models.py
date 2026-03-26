from dataclasses import dataclass


@dataclass(frozen=True)
class BlogColumn:
    url: str
    name: str
    article_count: int


@dataclass(frozen=True)
class BlogArticle:
    column: str
    url: str
    title: str


@dataclass(frozen=True)
class FailedArticle:
    url: str
    reason: str