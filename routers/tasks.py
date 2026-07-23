from fastapi import APIRouter, HTTPException, status, Depends
from models.task import Task
from models.user import User
from database.client import db_client
from services.auth_services import current_user
from services.task_services import (
    validator_taks,
    search_task,
    schema_task,
    schema_task_list,
    estadisticas,
)
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(
    prefix="/tareas", tags=["tareas"], responses={404: {"Error": "Tarea no válida"}}
)


@router.post("/crear", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task, user: User = Depends(current_user)):
    tarea_validada = validator_taks(task)
    tarea_dict = dict(tarea_validada)
    del tarea_dict["id"]
    tarea_dict["owner"] = str(user.id)
    id_isert = db_client.tareas.insert_one(tarea_dict).inserted_id
    tarea_db = schema_task(db_client.tareas.find_one({"_id": id_isert}))
    return Task(**tarea_db)


@router.get("/", response_model=list[Task], status_code=status.HTTP_200_OK)
async def taskme(user: User = Depends(current_user)):
    tareas_cursor = db_client.tareas.find({"owner": str(user.id)})
    return schema_task_list(tareas_cursor)


@router.get("/stats", status_code=status.HTTP_200_OK)
async def statics(user: User = Depends(current_user)):
    return estadisticas(user)


@router.get("/{id}", response_model=Task, status_code=status.HTTP_200_OK)
async def taskme(id: str, user: User = Depends(current_user)):
    tarea_buscada = search_task("_id", ObjectId(id))
    if tarea_buscada is None or tarea_buscada.owner != str(user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada"
        )

    return schema_task(tarea_buscada)


@router.put("/{id}", response_model=Task, status_code=status.HTTP_200_OK)
async def up_task(id: str, tarea: Task, user: User = Depends(current_user)):
    tarea_buscada = search_task("_id", ObjectId(id))
    if tarea_buscada is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tarea inválido"
        )
    tarea_valid = validator_taks(tarea)
    tarea_dict = dict(tarea_valid)
    del tarea_dict["_id"]
    del tarea_dict["owner"]
    tarea_dict["owner"] = str(user.id)
    try:
        db_client.tareas.find_one_and_replace(
            {"_id": ObjectId(id), "owner": str(user.id)}, tarea_dict
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tarea no actualziada"
        )
    return search_task("_id", ObjectId(id))


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_task(id: str, user: User = Depends(current_user)):
    try:
        id_verificada = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tarea inválido"
        )
    found = db_client.tareas.find_one_and_delete(
        {"_id": id_verificada, "owner": str(user.id)}
    )
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada o no autorizada",
        )
    return {"Mesagge": "Tarea eliminada"}
