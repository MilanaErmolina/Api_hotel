# routers/room_types.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import RoomType
from schemas import RoomTypeCreate

app = APIRouter(prefix="/room_types", tags=["room_types"])

class RoomTypesCreate(BaseModel):
    name: str
    description: str
    capacity: int

class RoomTypesUpdate(BaseModel):
    id: int
    name: str
    description: str
    capacity: int

@app.get("/")
def get_room_types():
    room_types = RoomType.select()
    return [{
        'id': rt.id,
        'name': rt.name,
        'description': rt.description,
        'capacity': rt.capacity
    } for rt in room_types]

@app.get("/{room_type_id}")
def get_room_type(room_type_id: int):
    try:
        room_type = RoomType.get(RoomType.id == room_type_id)
        return {
            'id': room_type.id,
            'name': room_type.name,
            'description': room_type.description,
            'capacity': room_type.capacity
        }
    except RoomType.DoesNotExist:
        raise HTTPException(status_code=404, detail="Room type not found")

@app.post("/")
def create_room_type(room_types: RoomTypesCreate):
    room_type = RoomType.create(
        name=room_types.name,
        description=room_types.description,
        capacity=room_types.capacity
    )
    return {
        'id': room_type.id,
        'name': room_type.name,
        'description': room_type.description,
        'capacity': room_type.capacity
    }

@app.put("/")
def update_room_type(room_type_update: RoomTypesUpdate):
    try:
        room_type = RoomType.get(RoomType.id == room_type_update.id)
        room_type.name = room_type_update.name
        room_type.description = room_type_update.description
        room_type.capacity = room_type_update.capacity
        room_type.save()
        return {
            'id': room_type.id,
            'name': room_type.name,
            'description': room_type.description,
            'capacity': room_type.capacity
        }
    except RoomType.DoesNotExist:
        raise HTTPException(status_code=404, detail="Room type not found")

@app.delete("/{room_type_id}")
def delete_room_type(room_type_id: int):
    try:
        room_type = RoomType.get(RoomType.id == room_type_id)
        room_type.delete_instance()
        return {"message": "Room type deleted successfully"}
    except RoomType.DoesNotExist:
        raise HTTPException(status_code=404, detail="Room type not found")