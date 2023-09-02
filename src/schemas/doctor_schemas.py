import datetime
from typing import List

from pydantic import BaseModel, ConfigDict



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

class DoctorModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    info: str
    category: str
    work_experience: int
    specialization: List[str]
    price: int
    user_id: int

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
    user_id: int
    anamnesis: str | None


class Anamnesis(BaseModel):
    anamnesis: str


class DayAppointmentOut(BaseModel):
    date: datetime.date
    appointments: List[AppointmentById | AppointmentBasicOut]
    day_of_the_week: str = None
    model_config = ConfigDict(from_attributes=True)


class DoctorOut(DoctorShort):
    category: str
    work_experience: int
    specialization: List[str]
    price: int
    day_appointments: List[DayAppointmentOut]


class PatientOut(BaseModel):
    id: int
    patient: str
    doctor: str
