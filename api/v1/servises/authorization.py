from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.v1.servises.crud.crud import get_user_by_email, set_new_user
from core.schemas.schemas import RegistrationSchema, UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(email: str = Depends(oauth2_scheme)) -> UserSchema:
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации",
        )
    return UserSchema(id=user.id, email=user.email)


def register_new_user(registration_info: RegistrationSchema) -> UserSchema:
    user = get_user_by_email(registration_info.email)
    if user is None:
        new_user = set_new_user(registration_info.email)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой пользователь уже зарегестрирован",
        )
    return UserSchema(id=new_user.id, email=new_user.email)
