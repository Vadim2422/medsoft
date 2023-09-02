import datetime

from sqlalchemy import and_

from src.models.doctor_model import Appointment, DayAppointment
from src.models.user_model import User
from src.utils.repository import AbstractRepository


class DayAppointmentService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def get_appointments_for_patient(self, user_db: User):
        filters = {'patient_id': user_db.patient.id}
        orders = tuple(Appointment.date.asc())
        return await self.repository.find_all(filters, orders)

    async def get_schedule_for_doctor(self, doctor_id: int):
        where = and_(DayAppointment.doctor_id == doctor_id,
                     DayAppointment.date >= datetime.date.today(),
                     DayAppointment.date <= datetime.date.today() + datetime.timedelta(days=7))
        orders = (DayAppointment.date.asc(),)
        days = await self.repository.find_all(where=where, orders=orders)
        for day in days:
            day: DayAppointment
            day.appointments.sort(key=lambda x: x.date)
        return days

