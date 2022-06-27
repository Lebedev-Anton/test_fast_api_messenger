from fastapi import APIRouter, Depends

from core.schemas.schemas import RegistrationSchema, UserSchema, GroupSchema
from api.v1.servises.authorization import register_new_user
from api.v1.servises.groups import get_group_info, register_new_group

router = APIRouter()


@router.post('/user/', response_model=UserSchema, status_code=201)
async def register_user(registration_info: RegistrationSchema):
    new_user = await register_new_user(registration_info)
    return new_user


@router.post('/group/', response_model=GroupSchema, status_code=201)
async def register_group(group_info: GroupSchema = Depends(get_group_info)):
    new_group = await register_new_group(group_info)
    return new_group
