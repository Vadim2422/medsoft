import datetime
from typing import Annotated, List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import get_id_from_token, oauth2_scheme, check_user_role, check_patient
from src.database import get_async_session
from src.doctor.doctor_model import Doctor, Appointment
from src.doctor.doctor_schemas import DoctorSetAppointment, AppointmentById
from src.patient.patient_model import Patient, HealthMetrics
from src.patient.patient_schemas import PatientPostAppointment, AppointmentsOut, HealthMetricsPost, GetMetrics, \
    HealthMetricsOut
from src.user.user_model import User
from src.user.user_role import UserRole
from src.user.user_schemas import UserCreate, UserOut, UserAuth, UserUpdate, UserCreateOut
from src.user.user_service import UserService
from src.utils.sms_service import send_verification_sms, confirm_sms_code

router = APIRouter(tags=["Patient"])
SessionDep = Depends(get_async_session)





@router.post("/patient/appointment/{appointment_id}", status_code=201, response_description="Возвращает подробную информацию о приеме по id")
async def set_appointment(appointment_id: int, user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    stmt = select(Appointment).where(and_(Appointment.id == appointment_id))
    appointment: Appointment = await session.scalar(stmt)
    if appointment.patient_id:
        raise HTTPException(status_code=404, detail="Appointment is exist")
    user_service = UserService(session)
    user: User = await user_service.get_user_by_id(user_id)
    appointment.patient = user.patient
    await session.commit()


@router.get("/patient/appointments", status_code=200, response_model=List[AppointmentsOut], response_description="Возвращает все приемы пациента")
async def get_appointments(user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user: User = await user_service.get_user_by_id(user_id)
    patient: Patient = user.patient
    if patient.appointments:
        apps = sorted(patient.appointments, key=lambda x: x.date)
    else:
        apps = []

    return [AppointmentsOut(**app.__dict__,
                                   doctor_id=app.day_appointments.doctor.id,
                                   info=app.day_appointments.doctor.info,
                                   fio=(await app.day_appointments.doctor.awaitable_attrs.user).get_fio(),
                                   check=True if app.anamnesis else False) for app in apps]


@router.get("/patient/appointment/{appointment_id}", status_code=200, response_model=AppointmentById, response_description="Возвращает подробную информацию о приеме по id")
async def get_appointment(appointment_id: int, user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user: User = await user_service.get_user_by_id(user_id)
    patient: Patient = user.patient
    stmt = select(Appointment).where(and_(Appointment.id == appointment_id))
    appointment: Appointment = await session.scalar(stmt)
    doctor = appointment.day_appointments.doctor
    if appointment.patient_id != patient.id:
        raise HTTPException(status_code=404, detail="Patient dont have this appointment")

    return AppointmentById(**appointment.__dict__,
                           user_id=appointment.patient.user.id,
                           doctor_id=doctor.id,
                           fio=appointment.patient.user.get_fio(),
                           info=doctor.info)


@router.post("/patient/health", status_code=201, response_description="Сохраняет данные о состоянии пациента утром или вечером")
async def set_health(health: HealthMetricsPost, user_id=Depends(get_id_from_token), session: AsyncSession = SessionDep):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id)
    check_patient(user)



    health_metrics = HealthMetrics(**health.__dict__, date=datetime.datetime.now())
    health_metrics.user = user
    session.add(health_metrics)

    await session.commit()


@router.get("/patient/health", status_code=201, response_model=List[HealthMetricsOut], response_description="Сохраняет данные о состоянии пациента утром или вечером")
async def set_health(user_id: int, date: datetime.date, session: AsyncSession = SessionDep):
    stmt = select(HealthMetrics).where(and_(HealthMetrics.user_id == user_id,
                                            HealthMetrics.date >= date,
                                            HealthMetrics.date < date + datetime.timedelta(days=1)))
    health_metrics = await session.scalars(stmt)
    return [HealthMetricsOut(**metrics.__dict__) for metrics in health_metrics.unique()]

