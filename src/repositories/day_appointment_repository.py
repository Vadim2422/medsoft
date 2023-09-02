from src.models.doctor_model import DayAppointment
from src.utils.repository import SQLAlchemyRepository


class DayAppointmentRepository(SQLAlchemyRepository):
    model = DayAppointment
