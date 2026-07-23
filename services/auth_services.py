from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from models.user import User
from services.schemas import search_user

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
DURACTION = config("DURACTION_MINUTES")
oatuh2 = OAuth2PasswordBearer(tokenUrl="/usuario/token")


async def autenticador(token: str = Depends(oatuh2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    user = search_user("username", payload)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


async def current_user(user: User = Depends(autenticador)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo",
        )
    return user
