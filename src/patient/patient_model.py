from datetime import datetime

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Enum, Integer, ARRAY, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.doctor.doctor_model import Appointment
from src.database import Base
from src.user.user_role import UserRole


class Patient(Base):
    __tablename__ = "patients"
    id = Column("id", BigInteger, primary_key=True)
    appointments = relationship("Appointment", back_populates="patient", lazy="joined")
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="patient", lazy="joined")


