from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from sqlalchemy.orm import selectinload

from src.auth.auth import check_user_role, get_id_from_token, check_doctor
from src.database import get_async_session
from src.doctor.doctor_model import Doctor, DayAppointment, Appointment
from src.doctor.doctor_schemas import DoctorShort, DoctorOut, DayAppointmentOut, AppointmentBasicOut, AppointmentById, \
    Anamnesis
from src.patient.patient_schemas import AppointmentsOut
from src.user.user_model import User
from src.user.user_service import UserService

router = APIRouter(tags=["Doctor"])

SessionDep = Depends(get_async_session)


@router.get("/doctors/{doctor_id}", status_code=200, response_model=DoctorOut, response_description="Возвращает информацию о докторе вместе с расписанием по id")
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


@router.get("/doctors", status_code=200, response_model=List[DoctorShort], response_description="Возвращает список всех докторов")
async def get_doctor(session: AsyncSession = SessionDep):
    stmt = select(Doctor)
    result = await session.execute(stmt)
    doctors = result.scalars().unique()
    return [DoctorShort(**doctor.__dict__, fio=doctor.user.get_fio(), photo=doctor.user.photo) for doctor in doctors]


@router.get("/doctor/appointment/{appointment_id}", status_code=200, response_model=AppointmentById, response_description="Возвращает подробную информацию о приеме по id")
async def get_appointment(appointment_id: int, user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user: User = await user_service.get_user_by_id(user_id)
    check_doctor(user)
    doctor: Doctor = user.doctor
    stmt = select(Appointment).where(and_(Appointment.id == appointment_id))
    appointment: Appointment = await session.scalar(stmt)

    if not appointment or appointment.day_appointments.doctor_id != doctor.id:
        raise HTTPException(status_code=404, detail="Doctor dont have this appointment")
    if not appointment.patient:
        raise HTTPException(status_code=404, detail="")

    return AppointmentById(**appointment.__dict__,
                           doctor_id=doctor.id,
                           fio=appointment.patient.user.get_fio(),
                           info=doctor.info)


@router.post("/doctor/appointment/{appointment_id}/anamnesis", status_code=201, response_description="Сохраняет анамнез")
async def set_anamnesis(appointment_id: int, anamnesis: Anamnesis, user_id=Depends(get_id_from_token),
                        session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user: User = await user_service.get_user_by_id(user_id)
    check_doctor(user)
    doctor: Doctor = user.doctor
    stmt = select(Appointment).where(and_(Appointment.id == appointment_id))
    appointment: Appointment = await session.scalar(stmt)
    if appointment.day_appointments.doctor_id != doctor.id:
        raise HTTPException(status_code=404, detail="Doctor dont have this appointment")
    if not appointment.patient:
        raise HTTPException(status_code=404, detail="")
    appointment.anamnesis = anamnesis.anamnesis
    await session.commit()


@router.get("/doctor/appointments/today", status_code=200, response_model=List[AppointmentsOut], response_description="Возвращает информацию о приемах на сегодня")
async def get_doctor_appointments(user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id)
    check_doctor(user)
    doctor: Doctor = user.doctor
    stmt = select(DayAppointment).where(
        and_(DayAppointment.doctor_id == doctor.id, DayAppointment.date == datetime.date.today()))
    day_appointments: DayAppointment = await session.scalar(stmt)
    if day_appointments:
        appointments: List[Appointment] = [app for app in day_appointments.appointments if app.patient_id]
        appointments.sort(key=lambda x: x.date)
        if not appointments:
            appointments = []
    else:
        raise HTTPException(status_code=404)
    return [AppointmentsOut(**app.__dict__,
                            doctor_id=app.day_appointments.doctor.id,
                            info=app.day_appointments.doctor.info,
                            fio=app.patient.user.get_fio(),
                            check=True if app.anamnesis else False) for app in appointments]


@router.get("/doctor/appointments/all", status_code=200, response_model=List[DayAppointmentOut], response_description="Возвращает все прошедшие приему, кроме сегодняшних")
async def get_doctor_appointments(user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id)
    check_doctor(user)
    doctor: Doctor = user.doctor
    stmt = select(DayAppointment).where(
        and_(DayAppointment.doctor_id == doctor.id, DayAppointment.date < datetime.date.today()))
    result = await session.execute(stmt)

    day_appointments: List[DayAppointment] = list(result.scalars().unique())

    day_appointments.sort(key=lambda x: x.date)
    for day_appointment in day_appointments:
        day_appointment.appointments.sort(key=lambda x: x.date)

    if not day_appointments:
        raise HTTPException(status_code=404)
    day_appointments_out = []
    for day in day_appointments:
        appointments_out = [AppointmentsOut(**app.__dict__, info=app.day_appointments.doctor.info, check=True,
                                            fio=app.patient.user.get_fio(),
                                            doctor_id=app.day_appointments.doctor.id) for app in
                            day.appointments if app.patient_id is not None]
        if appointments_out:
            day_appointments_out.append(DayAppointmentOut(date=day.date,
                                                          appointments=appointments_out).get_class_with_day_week())
    return day_appointments_out
