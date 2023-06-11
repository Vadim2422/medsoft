from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.user.user_router import router as user_router

app = FastAPI(
    title="Medsoft"
)
app.include_router(user_router)

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



