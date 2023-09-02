from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.api.routers import all_routers


app = FastAPI(
    title="Lumen"
)
for router in all_routers:
    app.include_router(router)


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
