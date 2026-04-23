from typing import Any

from pydantic import BaseModel

class Query(BaseModel):
    id: str
    query: str

