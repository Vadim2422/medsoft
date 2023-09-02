import datetime

from pydantic import BaseModel


class AppointmentOut(BaseModel):
    id: int
    date: datetime.datetime
    info: str
    fio_doctor: str
    fio_patient: str
    doctor_id: int
    patient_id: int
    anamnesis: str | None
