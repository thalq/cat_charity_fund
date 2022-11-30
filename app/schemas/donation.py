# from datetime import datetime
# from typing import Optional

# from pydantic import BaseModel, Extra, Field, validator


# class DonationBase(BaseModel):
#     user_id: Optional[int]
#     comment: Optional[str]
#     full_amount: Optional[int]
#     invested_amount: Optional[int] = Field(0)
#     fully_invested: Optional[bool] = Field(False)
#     create_date: Optional[datetime] = Field(
#         datetime.now(), example=datetime.now().isoformat(timespec="minutes")
#     )
#     close_date: Optional[datetime] = Field(
#         None, example=datetime.now().isoformat(timespec="minutes")
#     )

#     class Config:
#         extra = Extra.forbid


# class DonationCreate(DonationBase):
#     full_amount: int


# class CharityProjectRoomDB(CharityProjectCreate):
#     id: int

#     class Config:
#         orm_mode = True
