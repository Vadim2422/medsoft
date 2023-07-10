import enum
from datetime import datetime

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Enum, Integer, ARRAY, Date, ForeignKey, Float
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



class StateOfHealth(enum.Enum):
    UNWELL = "Плохое"
    NORMAL = "Нормальное"
    GOOD = "Хорошее"
    great = "Отличное"





class HealthMetrics(Base):
    __tablename__ = "health_metrics"
    id = Column("id", BigInteger, primary_key=True)
    pressure = Column("pressure", String(10))
    temperature = Column("temperature", Float)
    pulse = Column("pulse", Integer)
    saturation = Column("saturation", Integer)
    sugar = Column("sugar", Float)
    state = Column(Enum(StateOfHealth))
    complaints = Column("complaints", String(1000))
    date = Column(TIMESTAMP, default=datetime.now)

    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", lazy="joined")

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if value:
                setattr(self, field, value)
