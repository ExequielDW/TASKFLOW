from pydantic import BaseModel


class Task(BaseModel):
    id: str | None = None
    title: str
    description: str
    priority: str
    status: str
    deadline: str
    owner: str | None = None
