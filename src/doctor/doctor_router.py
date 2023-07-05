from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from sqlalchemy.orm import selectinload

from src.database import get_async_session
from src.doctor.doctor_model import Doctor, DayAppointment, Appointment
from src.doctor.doctor_schemas import DoctorShort, DoctorOut, DayAppointmentOut, AppointmentBasicOut
from src.main import SessionDep

router = APIRouter(tags=["Doctor"])




@router.get("/doctors/{doctor_id}", status_code=200, response_model=DoctorOut)
async def get_doctor(doctor_id: int, session: AsyncSession = SessionDep):
    stmt = select(Doctor).where(and_(Doctor.id == doctor_id))
    doctor: Doctor = await session.scalar(stmt)

    stmt = select(DayAppointment).where(and_(DayAppointment.doctor_id == doctor.id,
                                             DayAppointment.date >= datetime.date.today(),
                                             DayAppointment.date <= datetime.date.today() + datetime.timedelta(days=7)))
    day = await session.execute(stmt)
    days = list(day.scalars().unique())

    days.sort(key=lambda x: x.date)
    for day in days:
        day.appointments.sort(key=lambda x: x.date)
    days_out = [DayAppointmentOut(date=day.date,
                                  appointments=[AppointmentBasicOut(**app.__dict__) for app in day.appointments if
                                                app.patient_id == None]).get_class_with_day_week() for day in days]
    doctor_out = DoctorOut(**doctor.__dict__, fio=doctor.user.get_fio(),
                           photo=doctor.user.photo,
                           day_appointments=days_out)
    return doctor_out


@router.get("/doctor/{1}", status_code=200, response_model=List[DoctorShort])
async def get_doctor(session: AsyncSession = SessionDep, atl="afokt", tmp = Depends(check_user_role)):
    stmt = select(Doctor)
    result = await session.execute(stmt)
    doctors = result.scalars().unique()
    return [DoctorShort(**doctor.__dict__, fio=doctor.user.get_fio(), photo=doctor.user.photo) for doctor in doctors]

# @router.get("/doctor")
