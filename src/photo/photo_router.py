from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Photo"])


@router.get("/photo/{photo}", status_code=200)
async def get_photo(photo: str):
    return FileResponse(f"dataset/src/{photo}")



