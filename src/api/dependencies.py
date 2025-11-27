from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(10, description="Количество отелей на странице", ge=1, le=100)]


PaginationDep = Annotated[PaginationParams, Depends()]