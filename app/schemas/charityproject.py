from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[int]
    invested_amount: Optional[int] = Field(0)
    fully_invested: Optional[bool] = Field(False)
    create_date: Optional[datetime] = Field(
        datetime.now(), example=datetime.now().isoformat(timespec="minutes")
    )
    close_date: Optional[datetime] = Field(
        datetime.now(), example=datetime.now().isoformat(timespec="minutes")
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: int


class CharityProjectRoomDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
