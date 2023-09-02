from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.models.doctor_model import Doctor
from src.schemas.doctor_schemas import DoctorShort, DayAppointmentOut, AppointmentBasicOut, DoctorOut
from src.services.day_appointment_service import DayAppointmentService
from src.services.doctor_service import DoctorService

router = APIRouter(
    prefix="/doctor",
    tags=["Doctor"]
)


# @router.get("/lk")
# async def get_doctor_lk(user_db: Annotated[User, Depends(user_service().get_user_from_token)]):
#     tmp = await app_service.get_appointments_for_patient(user_db)
#     print(tmp)


@router.get("/all")
async def get_all_doctor(doc_service: Annotated[DoctorService, Depends(doctor_service)]) -> List[DoctorShort]:
    return await doc_service.get_all_doctor()


@router.get("/{doctor_id}")
async def get_page_doctor_by_id(doctor_db: Annotated[Doctor, Depends(doctor_service().get_doctor_by_id)],
                                day_app_service: Annotated[DayAppointmentService, Depends(day_appointment_service)]) \
        -> DoctorOut:
    days = await day_app_service.get_schedule_for_doctor(doctor_db.id)
    days_out = [DayAppointmentOut(date=day.date,
                                  appointments=[AppointmentBasicOut(**app.__dict__) for app in day.appointments if
                                                app.patient_id is None]) for day in days]
    return DoctorOut(**doctor_db.__dict__, fio=doctor_db.user.get_fio(),
                     photo=doctor_db.user.photo,
                     day_appointments=days_out)


