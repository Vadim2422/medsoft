import datetime

from pydantic import BaseModel

from src.patient.patient_model import StateOfHealth, Day


class PatientPostAppointment(BaseModel):
    appointment_id: int
    date: str


class AppointmentsOut(BaseModel):
    id: int
    doctor_id: int
    fio: str
    info: str
    date: datetime.datetime
    check: bool


class HealthMetricsPost(BaseModel):
    pressure: str | None
    temperature: float | None
    pulse: int | None
    saturation: int | None
    sugar: float | None
    state: StateOfHealth | None
    complaints: str | None
    day: Day
    date: datetime.datetime | None
