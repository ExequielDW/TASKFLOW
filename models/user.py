from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    username: str
    name: str
    surname: str
    email: str
    disabled: bool


class UserInDB(User):
    password: str


class MailUpdate(BaseModel):
    email: str


class NameUpdate(BaseModel):
    name: str


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
