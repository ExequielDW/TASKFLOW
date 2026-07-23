from database.client import db_client
from models.user import User, UserInDB, NameUpdate, MailUpdate, PasswordUpdate
from fastapi import HTTPException, status
from pwdlib import PasswordHash

crypto = PasswordHash.recommended()


def schema_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "name": user["name"],
        "surname": user["surname"],
        "email": user["email"],
        "disabled": user["disabled"],
    }


def schema_user_db(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "name": user["name"],
        "surname": user["surname"],
        "email": user["email"],
        "disabled": user["disabled"],
        "password": user["password"],
    }


def schema_user_list(users) -> list:
    return [schema_user(user) for user in users]


def search_user(field: str, key):
    user = db_client.user_taskflow.find_one({field: key})
    if user is None:
        return None
    return User(**schema_user(user))


def search_user_db(field: str, key):
    user = db_client.user_taskflow.find_one({field: key})
    if user is None:
        return None
    return UserInDB(**schema_user_db(user))


def validator_user(user: UserInDB):
    if search_user("username", user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if search_user("email", user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long",
        )
    if user.name == None or user.surname == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name and surname cannot be empty",
        )
    user_dict = dict(user)
    del user_dict["id"]
    user_dict["password"] = crypto.hash(user_dict["password"])
    return user_dict


def name_validatorup(name: NameUpdate):
    if not name or not name.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name and surname cannot be empty",
        )
    return name.name


def mail_validatorup(email: MailUpdate):
    if not email.email or not "@" in email.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El mail no puede estar vacio, y debe contener un formato válido",
        )
    return email.email


def password_validator(password: PasswordUpdate, user: User):
    user_db = search_user_db("username", user.username)
    if len(password.current_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La contraseña no puede ser menor a 6 caracteres",
        )
    if not crypto.verify(password.current_password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="La contraseña es incorrecta"
        )
    if len(password.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La contraseña no puede ser menor a 6 caracteres",
        )
    if crypto.verify(password.new_password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La nueva contraseña no puede ser igual a la anterior",
        )
    user_dict = dict(user_db)
    del user_dict["id"]
    user_dict["password"] = crypto.hash(password.new_password)
    return user_dict
