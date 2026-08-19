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
    tareas_cursor = db_client.tareas.find(
        {"owner": str(user.id)}, {"status": 1, "priority": 1}
    )

    estatis = {
        "total_tasks": 0,
        "completed": 0,
        "pending": 0,
        "in_progress": 0,
        "high_priority": 0,
    }
    mapa_de_categorias = {
        "Completada": "completed",
        "Pendiente": "pending",
        "En progreso": "in_progress",
        "Alta": "high_priority",
    }
    for t in tareas_cursor:
        estatis["total_tasks"] += 1
        cat_db = t.get("status")
        pri_db = t.get("priority")
        if cat_db in mapa_de_categorias:
            clave = mapa_de_categorias[cat_db]
            estatis[clave] += 1
        if pri_db in mapa_de_categorias:
            clave_pri = mapa_de_categorias[pri_db]
            estatis[clave_pri] += 1
    return estatis
