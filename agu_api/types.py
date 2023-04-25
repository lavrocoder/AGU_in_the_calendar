import hashlib
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

    def hash(self) -> str:
        """
        Хэширует пару алгоритмом SHA-256.
        :return: Хэшированная пара
        """
        string = self.__str__()
        hash_object = hashlib.sha256(string.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig
