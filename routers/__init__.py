from .hotels import app as hotels_router
from .room_types import app as room_types_router
from .rooms import app as rooms_router
from .guests import app as guests_router
from .bookings import app as bookings_router

__all__ = ['hotels_router', 'room_types_router', 'rooms_router', 'guests_router', 'bookings_router']