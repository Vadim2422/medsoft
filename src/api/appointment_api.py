from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import user_service, appointment_service
from src.schemas.appointment_schemas import AppointmentOut
from src.services.appointment_service import AppointmentService
from src.models.user_model import User
from src.models.user_role import UserRole

router = APIRouter(
    prefix="/appointment",
    tags=["Appointment"]
)

@router.get("/all", status_code=200,
            response_description="Возвращает все прошедшие приемы")
async def get_appointments(user_db: Annotated[User, Depends(user_service().get_user_from_token)],
                           app_service: Annotated[AppointmentService, Depends(appointment_service)]):
    today = await app_service.get_all_doctor_appointments(user_db.doctor.id)
    # stmt = select(DayAppointment).where(
    #     and_(DayAppointment.doctor_id == doctor.id, DayAppointment.date < datetime.date.today()))
    # result = await session.execute(stmt)
    #
    # day_appointments: List[DayAppointment] = list(result.scalars().unique())
    #
    # day_appointments.sort(key=lambda x: x.date)
    # for day_appointment in day_appointments:
    #     day_appointment.appointments.sort(key=lambda x: x.date)
    #
    # if not day_appointments:
    #     raise HTTPException(status_code=404)
    # day_appointments_out = []
    # for day in day_appointments:
    #     appointments_out = [AppointmentsOut(**app.__dict__, info=app.day_appointments.doctor.info, check=True,
    #                                         fio=app.patient.user.get_fio(),
    #                                         doctor_id=app.day_appointments.doctor.id) for app in
    #                         day.appointments if app.patient_id is not None]
    #     if appointments_out:
    #         day_appointments_out.append(DayAppointmentOut(date=day.date,
    #                                                       appointments=appointments_out).get_class_with_day_week())
    # return day_appointments_out


@router.get("/{appointment_id}")
async def get_all_doctor(appointment_id: int,
                         user_db: Annotated[User, Depends(user_service().get_user_from_token)],
                         app_service: Annotated[AppointmentService, Depends(appointment_service)]):
    app = await app_service.get_appointment_by_id(appointment_id)
    if user_db.role == UserRole.DOCTOR:
        if not app or app.day_appointments.doctor_id != user_db.doctor.id:
            raise HTTPException(status_code=404, detail="Doctor dont have this appointment")
    elif user_db.role == UserRole.PATIENT:
        if not app or app.day_appointments.doctor_id != user_db.patient.id:
            raise HTTPException(status_code=404, detail="Patient dont have this appointment")
    return AppointmentOut(**app.__dict__,
                          info=app.day_appointments.doctor.info,
                          fio_doctor=app.day_appointments.doctor.user.get_fio(),
                          fio_patient=app.patient.user.get_fio(),
                          doctor_id=app.day_appointments.doctor_id)

