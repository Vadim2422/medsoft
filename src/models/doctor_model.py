from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Integer, ARRAY, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.schemas.doctor_schemas import DoctorModel


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column("id", BigInteger, primary_key=True)
    info = Column("info", String(100), nullable=False)
    category = Column("category", String(100), nullable=False)
    work_experience = Column("experience", Integer, nullable=False)
    specialization = Column("specialization", ARRAY(String), nullable=False)
    price = Column("price", Integer, nullable=False)
    day_appointments = relationship("DayAppointment", back_populates="doctor", lazy="dynamic")
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="doctor", lazy="joined")

    def to_model(self):
        return DoctorModel.model_validate(self)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column("id", BigInteger, primary_key=True)
    date = Column("time", TIMESTAMP, nullable=False)
    anamnesis = Column("anamnesis", String(1000))
    day_appointments_id = Column(ForeignKey("day_appointments.id"))
    day_appointments = relationship("DayAppointment", back_populates="appointments", lazy="joined")
    doctor_id = Column(ForeignKey("doctors.id"))
    doctor = relationship("Doctor", lazy="joined")


class DayAppointment(Base):
    __tablename__ = "day_appointments"
    id = Column("id", BigInteger, primary_key=True)
    date = Column("date", Date, nullable=False)
    doctor_id = Column(ForeignKey("doctors.id"))
    doctor = relationship("Doctor", back_populates="day_appointments", lazy="joined")
    appointments = relationship("Appointment", back_populates="day_appointments", lazy="joined")
