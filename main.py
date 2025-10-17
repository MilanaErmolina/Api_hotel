from fastapi import FastAPI
from database import db
from contextlib import asynccontextmanager
from models import Hotel, RoomType, Room, Guest, Booking  # Импорт из models.py
from routers import hotels_router, room_types_router, rooms_router, guests_router, bookings_router

app = FastAPI(title="Hotel Booking API", version="1.0.0")

# Подключение всех роутеров
app.include_router(hotels_router)
app.include_router(room_types_router)
app.include_router(rooms_router)
app.include_router(guests_router)
app.include_router(bookings_router)

# Создание таблиц при запуске
@app.on_event("startup")
def startup():
    db.connect()
    db.create_tables([Hotel, RoomType, Room, Guest, Booking], safe=True)

@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()

@app.get("/")
def root():
    return {"message": "Hotel Booking API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)