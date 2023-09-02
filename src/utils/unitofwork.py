from abc import ABC, abstractmethod
from typing import Type

from src.database import async_session_maker
from src.repositories.appointment_repository import AppointmentRepository
from src.repositories.day_appointment_repository import DayAppointmentRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.token_repository import TokenRepository
from src.repositories.user_repository import UserRepository


class IUnitOfWork(ABC):
    users: UserRepository
    appointments: AppointmentRepository
    day_appointment: DayAppointmentRepository
    token: TokenRepository
    doctor: DoctorRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.appointments = AppointmentRepository(self.session)
        self.day_appointment = DayAppointmentRepository(self.session)
        self.doctor = DoctorRepository(self.session)
        self.token = TokenRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
