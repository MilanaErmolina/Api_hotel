# schemas.py
from pydantic import BaseModel

class HotelCreate(BaseModel):
    name: str
    address: str
    city: str
    rating: float

class RoomTypeCreate(BaseModel):
    name: str
    description: str
    capacity: int

class RoomCreate(BaseModel):
    hotel_id: int
    room_type_id: int
    room_number: str
    price_per_night: float

class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float