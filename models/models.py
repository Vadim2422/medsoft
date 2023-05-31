from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, TIMESTAMP, Integer, String, func

from db import Base


class User(Base):
    __tablename__ = "user_"
    id = Column("id", Integer, primary_key=True)
    firstname = Column("firstname", String(15), default="gvhbj")
    secondname = Column("secondname", String(15))
    patronymic = Column("patronymic", String(15), nullable=True)
    registered_at = Column(TIMESTAMP, server_default=func.now())
    # registered_at = Column(TIMESTAMP, default=func.now())

