from sqlalchemy import and_

from src.api.dependencies import UOWDep
from src.models.doctor_model import Appointment
from src.utils.repository import AbstractRepository
from src.utils.unitofwork import IUnitOfWork


class AppointmentService:
    @staticmethod
    async def get_appointment_by_id(uow: UOWDep, appointment_id: int) -> Appointment:
        filters = {"id": appointment_id}
        async with uow:
            return await uow.appointments.find_one(filters=filters)

    @staticmethod
    async def get_all_doctor_appointments(uow: UOWDep, doctor_id: int):
        where = and_(Appointment.doctor_id == doctor_id)
        async with uow:
            return await uow.appointments.find_all(where=where)

    async def get_all_patient_appointments(self):
        pass
