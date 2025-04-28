from datetime import date

from pydantic import BaseModel


class StudentUpdateModel(BaseModel):
    name: str
    birth_date: date
    course_name: str | None = None
    photo_url: str | None = None