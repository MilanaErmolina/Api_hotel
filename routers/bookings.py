from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Booking 
from schemas import BookingCreate  
from datetime import date

app = APIRouter(prefix="/bookings", tags=["bookings"])

class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str

class BookingUpdate(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    total_price: float
    status: str

@app.get('/')
def get_bookings():
    bookings = Booking.select()
    return [{
        'id': booking.id,
        'guest_id': booking.guest.id,
        'room_id': booking.room.id,
        'check_in_date': booking.check_in_date,
        'check_out_date': booking.check_out_date,
        'total_price': booking.total_price,
        'status': booking.status
    } for booking in bookings]

@app.get('/{booking_id}')
def get_booking(booking_id: int):
    try:
        booking = Booking.get(Booking.id == booking_id)
        return {
            'id': booking.id,
            'guest_id': booking.guest.id,
            'room_id': booking.room.id,
            'check_in_date': booking.check_in_date,
            'check_out_date': booking.check_out_date,
            'total_price': booking.total_price,
            'status': booking.status
        }
    except Booking.DoesNotExist:
        raise HTTPException(status_code=404, detail="Booking not found")

@app.post('/')
def create_booking(booking: BookingCreate):
    booking = Booking.create(
        guest=booking.guest_id,
        room=booking.room_id,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        total_price=booking.total_price,
        status=booking.status
    )
    return {
        'id': booking.id,
        'guest_id': booking.guest.id,
        'room_id': booking.room.id,
        'check_in_date': booking.check_in_date,
        'check_out_date': booking.check_out_date,
        'total_price': booking.total_price,
        'status': booking.status
    }

@app.put('/')
def update_booking(booking_update: BookingUpdate):
    try:
        booking = Booking.get(Booking.id == booking_update.id)
        booking.guest = booking_update.guest_id
        booking.room = booking_update.room_id
        booking.check_in_date = booking_update.check_in_date
        booking.check_out_date = booking_update.check_out_date
        booking.total_price = booking_update.total_price
        booking.status = booking_update.status
        booking.save()
        return {
            'id': booking.id,
            'guest_id': booking.guest.id,
            'room_id': booking.room.id,
            'check_in_date': booking.check_in_date,
            'check_out_date': booking.check_out_date,
            'total_price': booking.total_price,
            'status': booking.status
        }
    except Booking.DoesNotExist:
        raise HTTPException(status_code=404, detail="Booking not found")

@app.delete('/{booking_id}')
def delete_booking(booking_id: int):
    try:
        booking = Booking.get(Booking.id == booking_id)
        booking.delete_instance()
        return {"message": "Booking deleted successfully"}
    except Booking.DoesNotExist:
        raise HTTPException(status_code=404, detail="Booking not found")
