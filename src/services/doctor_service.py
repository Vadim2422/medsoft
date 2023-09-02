from fastapi import HTTPException

from src.api.dependencies import UOWDep
from src.schemas.doctor_schemas import DoctorShort
from src.services.base_service import BaseService
from src.utils.repository import AbstractRepository


class DoctorService(BaseService):
    async def get_doctor_info(self, doctor_id: int):
        async with self.uow:
            doctor_db = await self.uow.doctor.find_one(id=doctor_id)
        if not doctor_db:
            raise HTTPException(status_code=404, detail="Doctor not found")

    async def get_all_doctor(self):
        async with self.uow:
            doctors = [row for row in await self.uow.doctor.find_all()]
        return [DoctorShort(**doctor.__dict__, fio=doctor.user.get_fio(), photo=doctor.user.photo) for doctor in
                doctors]

    async def get_doctor_by_id(self, doctor_id: int):
        # await app_service.get_schedule_for_doctor(doctor_id)
        async with self.uow:
            return await self.uow.doctor.find_one(id=doctor_id)

    async def get_doctor_by_user_id(self, user_id: int):
        # await app_service.get_schedule_for_doctor(doctor_id)
        async with self.uow:
            return await self.uow.doctor.find_one(user_id=user_id)


