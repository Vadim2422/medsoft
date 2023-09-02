from src.models.doctor_model import Doctor
from src.utils.repository import SQLAlchemyRepository


class DoctorRepository(SQLAlchemyRepository):
    model = Doctor
