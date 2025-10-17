from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Guest
from schemas import GuestCreate

app = APIRouter(prefix="/guests", tags=["guests"])

class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class GuestUpdate(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str

@app.get("/")
def get_guests():
    guests = Guest.select()
    return [{
        'id': guest.id,
        'first_name': guest.first_name,
        'last_name': guest.last_name,
        'email': guest.email,
        'phone': guest.phone
    } for guest in guests]

@app.get("/{guest_id}")
def get_guest(guest_id: int):
    try:
        guest = Guest.get(Guest.id == guest_id)
        return {
            'id': guest.id,
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'phone': guest.phone
        }
    except Guest.DoesNotExist:
        raise HTTPException(status_code=404, detail="Guest not found")

@app.post("/")
def create_guest(guest: GuestCreate):
    guest = Guest.create(
        first_name=guest.first_name,
        last_name=guest.last_name,
        email=guest.email,
        phone=guest.phone
    )
    return {
        'id': guest.id,
        'first_name': guest.first_name,
        'last_name': guest.last_name,
        'email': guest.email,
        'phone': guest.phone
    }

@app.put("/")
def update_guest(guest_update: GuestUpdate):
    try:
        guest = Guest.get(Guest.id == guest_update.id)
        guest.first_name = guest_update.first_name
        guest.last_name = guest_update.last_name
        guest.email = guest_update.email
        guest.phone = guest_update.phone
        guest.save()
        return {
            'id': guest.id,
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'phone': guest.phone
        }
    except Guest.DoesNotExist:
        raise HTTPException(status_code=404, detail="Guest not found")

@app.delete('/{guest_id}')
def delete_guest(guest_id: int):
    try:
        guest = Guest.get(Guest.id == guest_id)
        guest.delete_instance()
        return {"message": "Guest deleted successfully"}
    except Guest.DoesNotExist:
        raise HTTPException(status_code=404, detail="Guest not found")
