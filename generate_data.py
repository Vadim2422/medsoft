import asyncio
import datetime
import json
import random

from sqlalchemy import select, and_

from src.auth.auth import get_password_hash, create_access_token
from src.doctor.doctor_model import Doctor, DayAppointment, Appointment
from src.patient.patient_model import Patient
from src.user.user_model import User
from src.user.user_role import UserRole
from src.database import async_session_maker

session = async_session_maker()


async def generate_model():
    stmt = select(Doctor).where(and_(Doctor.id == 1))
    doc = await session.scalar(stmt)
    if doc:
        await session.close()
        return
    for i in range(0, 12):
        with open(f"dataset/data/{i}.json") as f:
            data = json.load(f)
        fio = data['fio'].split()
        password = random.randint(1000, 9999).__str__()
        user_doctor = User(
                    # id=i+2,
                    photo=data['photo'],
                    name=fio[0],
                    surname=fio[1],
                    patronymic=fio[2],
                    phone_number=f"+79{random.randint(100000000, 999999999)}",
                    password=get_password_hash(password),
                    role=UserRole.DOCTOR
                    )

        doctor = Doctor(info=data['info'],
                        category=data['category'],
                        work_experience=int(data['work_experience']),
                        specialization=data['specialization'],
                        price=int(data['price'])
                        )
        doctor.user = user_doctor



















        day_appointments = [DayAppointment(date=datetime.date.today() - datetime.timedelta(days=3) + datetime.timedelta(days=j),
                                          appointments=[Appointment(date=datetime.datetime.combine(
                                              datetime.date.today() - datetime.timedelta(days=3) + datetime.timedelta(days=j),
                                              datetime.time(8, 0)) + datetime.timedelta(hours=i))
                                                        for i in range(5)]) for j in range(1, 8)]
        # for day in day_appointment:
        #     day.appointments = [Appointment(
        #         date=datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=j),
        #                                        datetime.time(8, 0)) + datetime.timedelta(hours=i))
        #                         for i in range(5)]
        doctor.day_appointments.extend(day_appointments)
        if i == 0:
            appointment = day_appointments[0].appointments[0]


            user_patient = User(
                        name="Владлен",
                        surname="Абобус",
                        patronymic="Игоревич",
                        phone_number=f"+79009859434",
                        password=get_password_hash(password),
                        role=UserRole.PATIENT
                        )
            patient = Patient()
            patient.user = user_patient
            appointment.patient = patient
            session.add_all([user_patient, patient])


            if i == 0:
                session.add(user_doctor)
                await session.commit()
                print("patient data")
                print(patient.user.phone_number)
                print(password)
                print(create_access_token(user_patient, 43200).token)
                print("doctor data")
                print(user_doctor.phone_number)
                print(password)
                print(create_access_token(user_doctor, 43200).token)
        session.add_all([user_doctor, doctor])
    await session.commit()
    await session.close()


asyncio.run(generate_model())
