from datetime import date

from pydantic import BaseModel


class StudentUpdateModel(BaseModel):
    name:str | None = None
    birth_date: date | None = None
    course_name: str | None = None
    photo_url: str | None = None