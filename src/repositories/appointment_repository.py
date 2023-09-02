from src.models.doctor_model import Appointment
from src.utils.repository import SQLAlchemyRepository


class AppointmentRepository(SQLAlchemyRepository):
    model = Appointment