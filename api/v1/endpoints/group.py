from fastapi import APIRouter, Depends

from api.v1.servises.authorization import get_current_user
from core.schemas.schemas import UserSchema, MessageGroupSchema
from api.v1.servises.groups import get_group_story, send_group_message, get_group_by_user

router = APIRouter()


@router.get("/{group}/")
async def show_group_message(
        group: str,
        current_user: UserSchema = Depends(get_current_user)):
    messages = await get_group_story(group, current_user)
    return {"group_messages": messages}


@router.post("/{group}/", response_model=MessageGroupSchema, status_code=201)
async def post_group_message(
        message: MessageGroupSchema,
        current_user: UserSchema = Depends(get_current_user)):
    new_message = await send_group_message(message, current_user)
    return new_message


@router.get("/show/me/")
async def user_group(
        current_user: UserSchema = Depends(get_current_user)):
    groups = get_group_by_user(current_user)
    return groups
