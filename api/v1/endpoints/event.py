from fastapi import APIRouter, Depends

from api.v1.servises.authorization import get_current_user
from core.schemas.schemas import UserSchema, MessageGroupSchema
from api.v1.servises.events import get_online_user, get_long_polling_event

router = APIRouter()


@router.get("/online/")
async def online_user(current_user: UserSchema = Depends(get_current_user)):
    users = await get_online_user()
    return {"online user": users}


@router.get("/polling/")
async def long_polling(current_user: UserSchema = Depends(get_current_user)):
    events = get_long_polling_event(current_user)
    return {"events": events}


