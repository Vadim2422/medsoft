import datetime
from typing import Annotated, List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import get_id_from_token, oauth2_scheme
from src.database import get_async_session
from src.doctor.doctor_model import Doctor, Appointment
from src.doctor.doctor_schemas import DoctorSetAppointment, PatientAppointmentOut
from src.main import SessionDep
from src.patient.patient_model import Patient
from src.user.user_model import User
from src.user.user_role import UserRole
from src.user.user_schemas import UserCreate, UserOut, UserAuth, UserUpdate, UserCreateOut
from src.user.user_service import UserService
from src.utils.sms_service import send_verification_sms, confirm_sms_code

router = APIRouter(tags=["Patient"])



# @router.post("/appointment", status_code=200, response_model=DoctorBase)
# async def set_appointment(doctor_data: DoctorSetAppointment, user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
#     stmt = select(Doctor).where(and_(Doctor.id == doctor_data.doctor_id))
#     doctor: Doctor = await session.scalar(stmt)
#     doctor.appointments
#     user_service = UserService(session)
#     user: User = await user_service.get_user_by_id(user_id)
#     user.patient.appointments.append()
#     return doctor


@router.get("/appointment", status_code=200, response_model=List[PatientAppointmentOut])
async def get_appointment(user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user: User = await user_service.get_user_by_id(user_id)
    appointments: List[Appointment] = user.patient.appointments
    #todo sort by dataset
    appointments.sort(key=lambda appointment: appointment.date)
    return [PatientAppointmentOut(id=app.id, date=app.date, doctor=app.day_appointments.doctor.user.get_fio()) for app in appointments]



