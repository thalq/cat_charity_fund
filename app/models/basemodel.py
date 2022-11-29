from datetime import datetime
from typing import ClassVar

from app.core.db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer


class BaseModel(Base):
    __abstract__: ClassVar[bool] = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)
