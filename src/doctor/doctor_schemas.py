import datetime
from typing import List

from pydantic import BaseModel, validator

from src.doctor.doctor_model import Appointment
from src.patient.patient_schemas import AppointmentsOut


def get_day_of_the_week(day: int):
    match day:
        case 0:
            return 'Пн'
        case 1:
            return 'Вт'
        case 2:
            return 'Ср'
        case 3:
            return 'Чт'
        case 4:
            return 'Пт'
        case 5:
            return 'Сб'
        case 6:
            return 'Вс'


class DoctorSetAppointment(BaseModel):
    doctor_id: int
    time: str


# class DoctorBase(BaseModel):
#     date: datetime.datetime
#     day_of_the_week: str


class DoctorShort(BaseModel):
    id: int
    fio: str
    info: str
    photo: str | None


class AppointmentBasicOut(BaseModel):
    id: int
    date: datetime.datetime


class AppointmentById(AppointmentBasicOut):
    info: str
    fio: str
    doctor_id: int
    anamnesis: str | None

class Anamnesis(BaseModel):
    anamnesis: str



class DayAppointmentOut(BaseModel):
    date: datetime.date
    appointments: List[AppointmentsOut | AppointmentBasicOut]
    day_of_the_week: str = None

    def get_class_with_day_week(self):
        self.day_of_the_week = get_day_of_the_week(self.date.weekday())
        return self


class DoctorOut(DoctorShort):
    category: str
    work_experience: int
    specialization: List[str]
    price: int
    day_appointments: List[DayAppointmentOut]

    # @validator('day_of_the_week')
    # def validate_day_of_the_week(cls, day_of_the_week, values):
    #     date = values['date']
    #     return cls.get_day_of_the_week(date.date().weekday())


class PatientOut(BaseModel):
    id: int
    patient: str
    doctor: str

