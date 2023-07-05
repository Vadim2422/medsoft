from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.database import get_async_session
from src.doctor.doctor_router import router as doctor_router
from src.user.user_router import router as user_router
from src.photo.photo_router import router as photo_router

app = FastAPI(
    title="Medsoft"
)


SessionDep = Depends(get_async_session)

app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(photo_router)

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



