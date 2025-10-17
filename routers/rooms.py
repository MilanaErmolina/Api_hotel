from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Room, Hotel
from schemas import RoomCreate

app = APIRouter(prefix="/rooms", tags=["rooms"])

class RoomCreate(BaseModel):
    hotel_id: int
    room_type_id: int
    room_number: int
    price_per_night: int
    is_available: int

class RoomUpdate(BaseModel):
    id: int
    hotel_id: int
    room_type_id: int
    room_number: int
    price_per_night: int
    is_available: int

@app.get("/")
def get_rooms():
    rooms = Room.select()
    return [{
        'id': room.id,
        'hotel_id': room.hotel.id,
        'room_type_id': room.room_type.id,
        'room_number': room.room_number,
        'price_per_night': room.price_per_night,
        'is_available': room.is_available
    } for room in rooms]

@app.get('/{room_id}')
def get_room(room_id: int):
    try:
        room = Room.get(Room.id == room_id)
        return {
            'id': room.id,
            'hotel_id': room.hotel.id,
            'room_type_id': room.room_type.id,
            'room_number': room.room_number,
            'price_per_night': room.price_per_night,
            'is_available': room.is_available
        }
    except Room.DoesNotExist:
        raise HTTPException(status_code=404, detail="Room not found")

@app.post('/')
def create_room(room: RoomCreate):
    room = Room.create(
        hotel_id=room.hotel_id,
        room_type_id=room.room_type_id,
        room_number=room.room_number,
        price_per_night=room.price_per_night
    )
    return {
        'id': room.id,
        'hotel_id': room.hotel.id,
        'room_type_id': room.room_type.id,
        'room_number': room.room_number,
        'price_per_night': room.price_per_night,
        'is_available': room.is_available
    }

@app.put('/')
def update_room(room_update: RoomUpdate):
    try:
        room = Room.get(Room.id == room_update.id)
        
        room.hotel = room_update.hotel_id
        room.room_type = room_update.room_type_id
        room.room_number = room_update.room_number
        room.price_per_night = room_update.price_per_night
        room.is_available = room_update.is_available  # добавьте эту строку
        
        room.save()
        
        return {
            'id': room.id,
            'hotel_id': room.hotel.id,
            'room_type_id': room.room_type.id,
            'room_number': room.room_number,
            'price_per_night': room.price_per_night,
            'is_available': room.is_available
        }
    except Room.DoesNotExist:
        raise HTTPException(status_code=404, detail="Room not found")
    
@app.delete('/{room_id}')
def delete_room(room_id: int):
    try:
        room = Room.get(Room.id == room_id)
        room.delete_instance()
        return {"message": "Room deleted successfully"}
    except Room.DoesNotExist:
        raise HTTPException(status_code=404, detail="Room not found")

@app.get('/search/available_rooms')
def search_available_rooms():
    """Поиск доступных номеров"""
    available_rooms = Room.select().where(Room.is_available == 1)
    return [{
        'id': room.id,
        'hotel_name': room.hotel.name,
        'room_type': room.room_type.name,
        'room_number': room.room_number,
        'price_per_night': room.price_per_night,
        'capacity': room.room_type.capacity
    } for room in available_rooms]

