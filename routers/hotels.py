# routers/hotels.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Hotel, Room
from schemas import HotelCreate

app = APIRouter(prefix="/hotels", tags=["hotels"])

class HotelCreate(BaseModel):
    name: str
    address: str
    city: str
    rating: float

class HotelUpdate(BaseModel):
    id: int
    name: str
    address: str
    city: str
    rating: float

@app.get("/")
def get_hotels():
    hotels = Hotel.select()
    return [{
        'id': hotel.id,
        'name': hotel.name,
        'address': hotel.address,
        'city': hotel.city,
        'rating': hotel.rating
    } for hotel in hotels]

@app.get("/{hotel_id}")
def get_hotel(hotel_id: int):
    try:
        hotel = Hotel.get(Hotel.id == hotel_id)
        return {
            'id': hotel.id,
            'name': hotel.name,
            'address': hotel.address,
            'city': hotel.city,
            'rating': hotel.rating
        }
    except Hotel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Hotel not found")

@app.post("/")
def create_hotel(hotel: HotelCreate):
    hotel = Hotel.create(
        name=hotel.name,
        address=hotel.address,
        city=hotel.city,
        rating=hotel.rating
    )
    return {
        'id': hotel.id,
        'name': hotel.name,
        'address': hotel.address,
        'city': hotel.city,
        'rating': hotel.rating
    }

@app.put("/")
def update_hotel(hotel_update: HotelUpdate):
    try:
        hotel = Hotel.get(Hotel.id == hotel_update.id)
        hotel.name = hotel_update.name
        hotel.address = hotel_update.address
        hotel.city = hotel_update.city
        hotel.rating = hotel_update.rating
        hotel.save()
        
        return {
            'id': hotel.id,
            'name': hotel.name,
            'address': hotel.address,
            'city': hotel.city,
            'rating': hotel.rating
        }
    except Hotel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Hotel not found")

@app.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    try:
        hotel = Hotel.get(Hotel.id == hotel_id)
        hotel.delete_instance()
        return {"message": "Hotel deleted successfully"}
    except Hotel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
@app.get('/{hotel_id}/rooms')
def get_hotel_rooms(hotel_id: int):
    """Получить все номера конкретного отеля"""
    try:
        hotel = Hotel.get(Hotel.id == hotel_id)
        rooms = Room.select().where(Room.hotel == hotel)
        return [{
            'id': room.id,
            'room_type': room.room_type.name,
            'room_number': room.room_number,
            'price_per_night': room.price_per_night,
            'is_available': room.is_available
        } for room in rooms]
    except Hotel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Hotel not found")