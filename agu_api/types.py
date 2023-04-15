from datetime import datetime
from typing import List

from pydantic import BaseModel


class Group(BaseModel):
    ID: str
    SNAME: str


class Lesson(BaseModel):
    id: str
    time_begin: datetime
    time_end: datetime
    audience: str
    groups: List[str]
    name: str
    discipline_name: str
    teacher_name: str
    distant: bool = False
