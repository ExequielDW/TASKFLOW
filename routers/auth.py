from bson import ObjectId
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from database.client import db_client
from models.user import MailUpdate, NameUpdate, PasswordUpdate, User, UserInDB
from services.auth_services import ALGORITHM, DURACTION, SECRET_KEY, current_user
from services.schemas import (
    crypto,
    mail_validatorup,
    name_validatorup,
    password_validator,
    schema_user,
    search_user,
    search_user_db,
    validator_user,
)

# router
router = APIRouter(
    prefix="/usuario", tags=["usuario"], responses={404: {"Error": "Usuario no válido"}}
)


@router.post("/created", response_model=User, status_code=status.HTTP_201_CREATED)
async def registro(user: UserInDB):
    if search_user("email", user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya está registrado",
        )
    usuario = validator_user(user)
    user_insert_id = db_client.user_taskflow.insert_one(usuario).inserted_id
    user_db = schema_user(db_client.user_taskflow.find_one({"_id": user_insert_id}))
    return User(**user_db)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = search_user_db("username", form.username)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    if not crypto.verify(form.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(DURACTION))
    token_de_acesso = {"sub": usuario.username, "exp": expire}
    return {
        "access_token": jwt.encode(token_de_acesso, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "Bearer",
    }


@router.get("/token/me", response_model=User, status_code=status.HTTP_200_OK)
async def userme(user: User = Depends(current_user)):
    return user


@router.get("/token/{username}", response_model=User, status_code=status.HTTP_200_OK)
async def userme(username: str, user: User = Depends(current_user)):
    found_user = search_user("username", username)
    if found_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return found_user


@router.put("/token/me/name", response_model=User, status_code=status.HTTP_200_OK)
async def update_name(name: NameUpdate, user: User = Depends(current_user)):
    nombre = name_validatorup(name)
    user.name = nombre
    user_dict = dict(user)
    del user_dict["id"]
    try:
        updated = db_client.user_taskflow.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuario inválido",
        )
    return search_user("_id", ObjectId(user.id))


@router.put("/token/me/email", response_model=User, status_code=status.HTTP_200_OK)
async def update_name(email: MailUpdate, user: User = Depends(current_user)):
    mail = mail_validatorup(email)
    user.email = mail
    user_dict = dict(user)
    del user_dict["id"]
    try:
        updated = db_client.user_taskflow.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de usuario inválido",
        )
    return search_user("_id", ObjectId(user.id))


@router.put(
    "/token/me/password", response_model=UserInDB, status_code=status.HTTP_200_OK
)
async def update_name(password: PasswordUpdate, user: User = Depends(current_user)):
    contraseña = password_validator(password, user)
    updated = db_client.user_taskflow.find_one_and_replace(
        {"username": user.username}, contraseña
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return search_user_db("username", user.username)
