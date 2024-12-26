from __future__ import annotations

from typing import Any, List, Sequence, Union

from fastapi import Request
from pydantic import BaseModel, HttpUrl


class PageNumberPagination(BaseModel):
    items: List[Any] = []
    total: int
    next: Union[HttpUrl, None] = None
    prev: Union[HttpUrl, None] = None


def get_page_number_url(request: Request, page: int, per_page: int, total: int):
    if page * per_page > total or page <= 0:
        return

    query_params = dict(request.query_params.items())
    query_params["page"] = page
    query_params["per_page"] = per_page

    url = request.url.replace_query_params(**query_params)

    return str(url)


def paginate_by_page_number(request: Request, items: Sequence, total: int, page: int, per_page: int):
    return dict(
        items=items,
        total=total,
        next=get_page_number_url(request, page + 1, per_page, total),
        prev=get_page_number_url(request, page - 1, per_page, total),
    )
