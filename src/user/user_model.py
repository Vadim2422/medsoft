from datetime import datetime
from src.patient.patient_model import Patient
from src.doctor.doctor_model import Doctor
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, ForeignKey, \
    Integer, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped

from src.database import Base
from src.user.user_role import UserRole


class User(Base):
    __tablename__ = "users"
    id = Column("id", BigInteger, primary_key=True)
    name = Column("name", String(15), nullable=False)
    surname = Column("surname", String(15), nullable=False)
    patronymic = Column("patronymic", String(15))
    phone_number = Column("phone", String(15), nullable=False)
    photo = Column("photo", String(100))
    password = Column("password", String(300), nullable=False)
    role = Column("user_role", Enum(UserRole))
    registered_at = Column(TIMESTAMP, default=datetime.now)

    doctor: Mapped["Doctor"] = relationship(back_populates="user", lazy='joined')
    patient: Mapped["Patient"] = relationship(back_populates="user", lazy='joined')

    def get_fio(self):
        fio = f"{self.surname} {self.name}"
        if self.patronymic:
            fio += f" {self.patronymic}"
        return fio


# class Docktor(Base):


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
