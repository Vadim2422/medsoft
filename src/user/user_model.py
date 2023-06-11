from datetime import datetime

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, ForeignKey, \
    Integer, DateTime
from sqlalchemy.orm import relationship

from src.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", BigInteger, primary_key=True)
    name = Column("name", String(15), nullable=False)
    surname = Column("surname", String(15), nullable=False)
    patronymic = Column("patronymic", String(15))
    phone_number = Column("phone", BigInteger, nullable=False)
    password = Column("password", String(300), nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.now)


class RefreshToken(Base):
    __tablename__ = "tokens"
    id = Column("id", BigInteger, primary_key=True)
    token = Column("token", String(500), nullable=False)
    exp = Column("expires", TIMESTAMP)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", lazy='joined')


class VerificationCode(Base):
    __tablename__ = 'verification_codes'
    id = Column(BigInteger, primary_key=True)
    phone_number = Column(BigInteger, nullable=False, unique=True)
    verification_code = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
