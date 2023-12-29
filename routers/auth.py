from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("/login")
async def login():
    return {"test": "login"}