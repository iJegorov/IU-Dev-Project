from pydantic import BaseModel, Field


class TableRangeResponse(BaseModel):
    name: str
    range: str
    start_row: int
    start_column: int
    end_row: int
    end_column: int


class AnalyzeResponse(BaseModel):
    filename: str
    tables: list[TableRangeResponse]


class ErrorResponse(BaseModel):
    detail: str