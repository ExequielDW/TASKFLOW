from models.task import Task
from models.user import User
from fastapi import HTTPException, status
from database.client import db_client


def validator_taks(tarea: Task):
    PRIORIDADES = ["Alta", "Media", "Baja"]
    ESTADO = ["Pendiente", "En progreso", "Completada"]
    if tarea.priority not in PRIORIDADES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La prioridad debe ser un campo válido (Alta, Media, Baja)",
        )
    if tarea.status not in ESTADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estado debe ser un campo válido (Pendiente,En progreso,Completada)",
        )
    return tarea


def schema_task(tarea) -> dict:
    return {
        "id": str(tarea["_id"]),
        "title": tarea["title"],
        "description": tarea["description"],
        "priority": tarea["priority"],
        "status": tarea["status"],
        "deadline": tarea["deadline"],
        "owner": str(tarea["owner"]),
    }


def schema_task_list(tareas) -> list:
    return [schema_task(tarea) for tarea in tareas]


def search_task(field: str, key):
    tarea = db_client.tareas.find_one({field: key})
    if tarea is None:
        return None
    return Task(**schema_task(tarea))


def estadisticas(user: User):
    tareas_cursor = db_client.tareas.find({"owner": str(user.id)})
    dicio_task = schema_task_list(tareas_cursor)
    estatis = {
        "total_tasks": len(dicio_task),
        "completed": sum(1 for t in dicio_task if t["status"] == "Completada"),
        "pending": sum(1 for t in dicio_task if t["status"] == "Pendiente"),
        "in_progress": sum(1 for t in dicio_task if t["status"] == "En progreso"),
        "high_priority": sum(1 for t in dicio_task if t["priority"] == "Alta"),
    }
    return estatis
