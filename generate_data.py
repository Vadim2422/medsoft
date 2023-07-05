import asyncio
import datetime
import json
import random

from sqlalchemy import select

from src.doctor.doctor_model import Doctor, DayAppointment, Appointment
from src.user.user_model import User
from src.user.user_role import UserRole
from src.database import async_session_maker

session = async_session_maker()


async def generate_model():
    stmt = select(Doctor).where(Doctor.id == 1)
    doc = await session.scalar(stmt)
    if doc:
        return
    for i in range(0, 12):
        with open(f"dataset/data/{i}.json") as f:
            data = json.load(f)
        fio = data['fio'].split()
        user = User(photo=data['photo'],
                    name=fio[0],
                    surname=fio[1],
                    patronymic=fio[2],
                    phone_number=int(f"79{random.randint(100000000, 999999999)}"),
                    password=random.randint(1000, 9999).__str__(),
                    role=UserRole.PATIENT
                    )
        doctor = Doctor(info=data['info'],
                        category=data['category'],
                        work_experience=int(data['work_experience']),
                        specialization=data['specialization'],
                        price=int(data['price'])
                        )
        doctor.user = user



















        day_appointment = [DayAppointment(date=datetime.date.today() + datetime.timedelta(days=j),
                                          appointments=[Appointment(date=datetime.datetime.combine(
                                              datetime.date.today() + datetime.timedelta(days=j),
                                              datetime.time(8, 0)) + datetime.timedelta(hours=i))
                                                        for i in range(5)]) for j in range(1, 8)]
        # for day in day_appointment:
        #     day.appointments = [Appointment(
        #         date=datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=j),
        #                                        datetime.time(8, 0)) + datetime.timedelta(hours=i))
        #                         for i in range(5)]
        doctor.day_appointments.extend(day_appointment)

        session.add_all([user, doctor])
        await session.commit()
        await session.close()


asyncio.run(generate_model())
