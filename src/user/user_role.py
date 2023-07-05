import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    PATIENT = "patient"
    DOCTOR = "doctor"
