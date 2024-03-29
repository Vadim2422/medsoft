import asyncio
import datetime
import json
import random

from sqlalchemy import select, and_

from src.auth.auth import get_password_hash
from src.models.doctor_model import Doctor, DayAppointment, Appointment
from src.models.user_model import User
from src.models.user_role import UserRole
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
        password = (1234).__str__()
        user_doctor = User(
                    # id=i+2,
                    photo=data['photo'],
                    surname=fio[0],
                    name=fio[1],
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
                        name="Иван",
                        surname="Иванов",
                        patronymic="Иванович",
                        phone_number=f"+79009859434",
                        password=get_password_hash(1234),
                        role=UserRole.PATIENT
                        )
            print("patient data")
            print(1234)



            print("doctor data")
        print(user_doctor.surname)
        print(user_doctor.phone_number)
        print(password)
        session.add_all([user_doctor, doctor])
    await session.commit()
    await session.close()


asyncio.run(generate_model())
