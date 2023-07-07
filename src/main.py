from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.doctor.doctor_router import router as doctor_router
from src.user.user_router import router as user_router
from src.photo.photo_router import router as photo_router
from src.patient.patient_router import router as patient_router

app = FastAPI(
    title="Lumen"
)

app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(photo_router)
app.include_router(patient_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return "Ok"
