import requests
import time
import sys

BASE_URL = "http://localhost:8000"

class HotelAPITests:
    """Класс для тестирования API отеля"""
    
    def __init__(self):
        self.test_data = {}
        self.session = requests.Session()
        self.test_counter = int(time.time()) 
    
    def cleanup(self):
        """Очистка тестовых данных"""
        resources = ['booking_id', 'room_id', 'guest_id', 'hotel_id', 'room_type_id']
        for resource in resources:
            if resource in self.test_data:
                try:
                    if 'booking' in resource:
                        self.session.delete(f"{BASE_URL}/bookings/{self.test_data[resource]}")
                    elif 'room' in resource:
                        self.session.delete(f"{BASE_URL}/rooms/{self.test_data[resource]}")
                    elif 'guest' in resource:
                        self.session.delete(f"{BASE_URL}/guests/{self.test_data[resource]}")
                    elif 'hotel' in resource:
                        self.session.delete(f"{BASE_URL}/hotels/{self.test_data[resource]}")
                    elif 'room_type' in resource:
                        self.session.delete(f"{BASE_URL}/room_types/{self.test_data[resource]}")
                except Exception as e:
                    print(f"Ошибка при очистке {resource}: {e}")
    
    def run_test(self, test_func, test_name):
        """Запуск отдельного теста с обработкой исключений"""
        try:
            test_func()
            print(f"✓ {test_name}")
            return True
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            return False
    
    def test_server_availability(self):
        """Тест доступности сервера"""
        response = self.session.get(f"{BASE_URL}/hotels", timeout=10)
        assert response.status_code == 200, f"Server returned {response.status_code}"
    
    def test_get_hotels(self):
        """Тест получения списка отелей"""
        response = self.session.get(f"{BASE_URL}/hotels")
        assert response.status_code == 200
        hotels = response.json()
        assert isinstance(hotels, list)
    
    def test_create_hotel(self):
        """Тест создания отеля"""
        hotel_data = {
            "name": f"API Test Hotel {self.test_counter}",
            "address": "API Test Address",
            "city": "API Test City",
            "rating": 4.8
        }
        response = self.session.post(f"{BASE_URL}/hotels", json=hotel_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        hotel = response.json()
        assert hotel["name"] == hotel_data["name"]
        self.test_data['hotel_id'] = hotel['id']
    
    def test_get_single_hotel(self):
        """Тест получения конкретного отеля"""
        if 'hotel_id' not in self.test_data:
            self.test_create_hotel()
        
        response = self.session.get(f"{BASE_URL}/hotels/{self.test_data['hotel_id']}")
        assert response.status_code == 200
        hotel = response.json()
        assert hotel["id"] == self.test_data['hotel_id']
    
    def test_update_hotel(self):
        """Тест обновления отеля"""
        if 'hotel_id' not in self.test_data:
            self.test_create_hotel()
        
        update_data = {
            "id": self.test_data['hotel_id'],
            "name": f"Updated API Hotel {self.test_counter}",
            "address": "Updated Address",
            "city": "Updated City",
            "rating": 5.0
        }
        
        response = self.session.put(f"{BASE_URL}/hotels", json=update_data)
        assert response.status_code == 200
        hotel = response.json()
        assert hotel["name"] == update_data["name"]
        assert hotel["rating"] == update_data["rating"]
    
    def test_delete_hotel(self):
        """Тест удаления отеля"""
        hotel_data = {
            "name": f"Hotel to delete {self.test_counter}",
            "address": "Address to delete",
            "city": "City to delete",
            "rating": 3.0
        }
        response = self.session.post(f"{BASE_URL}/hotels", json=hotel_data)
        assert response.status_code == 200
        hotel_id = response.json()['id']
        
        response = self.session.delete(f"{BASE_URL}/hotels/{hotel_id}")
        assert response.status_code == 200
        
        response = self.session.get(f"{BASE_URL}/hotels/{hotel_id}")
        assert response.status_code == 404
    
    def test_get_room_types(self):
        """Тест получения списка типов комнат"""
        response = self.session.get(f"{BASE_URL}/room_types")
        assert response.status_code == 200
        room_types = response.json()
        assert isinstance(room_types, list)
    
    def test_create_room_type(self):
        """Тест создания типа номера"""
        room_type_data = {
            "name": f"API Test Suite {self.test_counter}",
            "description": "Luxury suite for API testing",
            "capacity": 4
        }
        response = self.session.post(f"{BASE_URL}/room_types", json=room_type_data)
        assert response.status_code == 200
        room_type = response.json()
        assert room_type["name"] == room_type_data["name"]
        self.test_data['room_type_id'] = room_type['id']
    
    def test_get_single_room_type(self):
        """Тест получения конкретного типа комнаты"""
        if 'room_type_id' not in self.test_data:
            self.test_create_room_type()
        
        response = self.session.get(f"{BASE_URL}/room_types/{self.test_data['room_type_id']}")
        assert response.status_code == 200
        room_type = response.json()
        assert room_type["id"] == self.test_data['room_type_id']
    
    def test_update_room_type(self):
        """Тест обновления типа комнаты"""
        if 'room_type_id' not in self.test_data:
            self.test_create_room_type()
        
        update_data = {
            "id": self.test_data['room_type_id'],
            "name": f"Updated Room Type {self.test_counter}",
            "description": "Updated description",
            "capacity": 5
        }
        
        response = self.session.put(f"{BASE_URL}/room_types", json=update_data)
        assert response.status_code == 200
        room_type = response.json()
        assert room_type["name"] == update_data["name"]
        assert room_type["capacity"] == update_data["capacity"]
    
    def test_delete_room_type(self):
        """Тест удаления типа комнаты"""
        room_type_data = {
            "name": f"Room Type to delete {self.test_counter}",
            "description": "Description to delete",
            "capacity": 2
        }
        response = self.session.post(f"{BASE_URL}/room_types", json=room_type_data)
        assert response.status_code == 200
        room_type_id = response.json()['id']
        
        response = self.session.delete(f"{BASE_URL}/room_types/{room_type_id}")
        assert response.status_code == 200
        
        response = self.session.get(f"{BASE_URL}/room_types/{room_type_id}")
        assert response.status_code == 404
    
    def test_get_guests(self):
        """Тест получения списка гостей"""
        response = self.session.get(f"{BASE_URL}/guests")
        assert response.status_code == 200
        guests = response.json()
        assert isinstance(guests, list)
    
    def test_create_guest(self):
        """Тест создания гостя"""
        guest_data = {
            "first_name": "API",
            "last_name": "Tester",
            "email": f"api.tester.{self.test_counter}@example.com", 
            "phone": f"7999{self.test_counter % 10000}"  
        }
        response = self.session.post(f"{BASE_URL}/guests", json=guest_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        guest = response.json()
        assert guest["email"] == guest_data["email"]
        self.test_data['guest_id'] = guest['id']
    
    def test_get_single_guest(self):
        """Тест получения конкретного гостя"""
        if 'guest_id' not in self.test_data:
            self.test_create_guest()
        
        response = self.session.get(f"{BASE_URL}/guests/{self.test_data['guest_id']}")
        assert response.status_code == 200
        guest = response.json()
        assert guest["id"] == self.test_data['guest_id']
    
    def test_update_guest(self):
        """Тест обновления гостя"""
        if 'guest_id' not in self.test_data:
            self.test_create_guest()
        
        update_data = {
            "id": self.test_data['guest_id'],
            "first_name": "Updated",
            "last_name": "User",
            "email": f"updated.{self.test_counter}@example.com",
            "phone": f"7888{self.test_counter % 10000}"
        }
        
        response = self.session.put(f"{BASE_URL}/guests", json=update_data)
        assert response.status_code == 200
        guest = response.json()
        assert guest["first_name"] == update_data["first_name"]
        assert guest["email"] == update_data["email"]
    
    def test_delete_guest(self):
        """Тест удаления гостя"""
        guest_data = {
            "first_name": "Guest",
            "last_name": "ToDelete",
            "email": f"delete.{self.test_counter}@example.com",
            "phone": f"7777{self.test_counter % 10000}"
        }
        response = self.session.post(f"{BASE_URL}/guests", json=guest_data)
        assert response.status_code == 200
        guest_id = response.json()['id']
        
        response = self.session.delete(f"{BASE_URL}/guests/{guest_id}")
        assert response.status_code == 200
        
        response = self.session.get(f"{BASE_URL}/guests/{guest_id}")
        assert response.status_code == 404
    
    def test_get_rooms(self):
        """Тест получения списка комнат"""
        response = self.session.get(f"{BASE_URL}/rooms")
        assert response.status_code == 200
        rooms = response.json()
        assert isinstance(rooms, list)
    
    def test_create_room(self):
        """Тест создания номера"""
        if 'hotel_id' not in self.test_data:
            self.test_create_hotel()
        if 'room_type_id' not in self.test_data:
            self.test_create_room_type()
        
        room_data = {
            "hotel_id": self.test_data['hotel_id'],
            "room_type_id": self.test_data['room_type_id'],
            "room_number": 100 + (self.test_counter % 100), 
            "price_per_night": 250,
            "is_available": 1
        }
        response = self.session.post(f"{BASE_URL}/rooms", json=room_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        room = response.json()
        assert room["room_number"] == room_data["room_number"]
        self.test_data['room_id'] = room['id']
    
    def test_get_single_room(self):
        """Тест получения конкретной комнаты"""
        if 'room_id' not in self.test_data:
            self.test_create_room()
        
        response = self.session.get(f"{BASE_URL}/rooms/{self.test_data['room_id']}")
        assert response.status_code == 200
        room = response.json()
        assert room["id"] == self.test_data['room_id']
    
    def test_update_room(self):
        """Тест обновления комнаты"""
        if 'room_id' not in self.test_data:
            self.test_create_room()
        
        update_data = {
            "id": self.test_data['room_id'],
            "hotel_id": self.test_data['hotel_id'],
            "room_type_id": self.test_data['room_type_id'],
            "room_number": 200 + (self.test_counter % 100),
            "price_per_night": 300,
            "is_available": 0
        }
        
        response = self.session.put(f"{BASE_URL}/rooms", json=update_data)
        assert response.status_code == 200
        room = response.json()
        assert room["room_number"] == update_data["room_number"]
        assert room["price_per_night"] == update_data["price_per_night"]
    
    def test_delete_room(self):
        """Тест удаления комнаты"""
        hotel_data = {
            "name": f"Hotel for room delete {self.test_counter}",
            "address": "Address for delete",
            "city": "City for delete",
            "rating": 3.0
        }
        hotel_response = self.session.post(f"{BASE_URL}/hotels", json=hotel_data)
        hotel_id = hotel_response.json()['id']
        
        room_type_data = {
            "name": f"Room type for delete {self.test_counter}",
            "description": "Description for delete",
            "capacity": 2
        }
        room_type_response = self.session.post(f"{BASE_URL}/room_types", json=room_type_data)
        room_type_id = room_type_response.json()['id']
        
        room_data = {
            "hotel_id": hotel_id,
            "room_type_id": room_type_id,
            "room_number": 999,
            "price_per_night": 100,
            "is_available": 1
        }
        response = self.session.post(f"{BASE_URL}/rooms", json=room_data)
        assert response.status_code == 200
        room_id = response.json()['id']
        
        response = self.session.delete(f"{BASE_URL}/rooms/{room_id}")
        assert response.status_code == 200
        
        response = self.session.get(f"{BASE_URL}/rooms/{room_id}")
        assert response.status_code == 404
        
        self.session.delete(f"{BASE_URL}/hotels/{hotel_id}")
        self.session.delete(f"{BASE_URL}/room_types/{room_type_id}")
    
    def test_get_bookings(self):
        """Тест получения списка бронирований"""
        response = self.session.get(f"{BASE_URL}/bookings")
        assert response.status_code == 200
        bookings = response.json()
        assert isinstance(bookings, list)
    
    def test_create_booking(self):
        """Тест создания бронирования"""
        if 'guest_id' not in self.test_data:
            self.test_create_guest()
        if 'room_id' not in self.test_data:
            self.test_create_room()
        
        booking_data = {
            "guest_id": self.test_data['guest_id'],
            "room_id": self.test_data['room_id'],
            "check_in_date": "2024-06-01",
            "check_out_date": "2024-06-05",
            "total_price": 1000,
            "status": "confirmed"
        }
        response = self.session.post(f"{BASE_URL}/bookings", json=booking_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        booking = response.json()
        assert booking["status"] == "confirmed"
        self.test_data['booking_id'] = booking['id']
    
    def test_get_single_booking(self):
        """Тест получения конкретного бронирования"""
        if 'booking_id' not in self.test_data:
            self.test_create_booking()
        
        response = self.session.get(f"{BASE_URL}/bookings/{self.test_data['booking_id']}")
        assert response.status_code == 200
        booking = response.json()
        assert booking["id"] == self.test_data['booking_id']
    
    def test_update_booking(self):
        """Тест обновления бронирования"""
        if 'booking_id' not in self.test_data:
            self.test_create_booking()
        
        update_data = {
            "id": self.test_data['booking_id'],
            "guest_id": self.test_data['guest_id'],
            "room_id": self.test_data['room_id'],
            "check_in_date": "2024-06-02",
            "check_out_date": "2024-06-06",
            "total_price": 1200,
            "status": "cancelled"
        }
        
        response = self.session.put(f"{BASE_URL}/bookings", json=update_data)
        assert response.status_code == 200
        booking = response.json()
        assert booking["status"] == update_data["status"]
        assert booking["total_price"] == update_data["total_price"]
    
    def test_delete_booking(self):
        """Тест удаления бронирования"""
        guest_data = {
            "first_name": "Booking",
            "last_name": "Delete",
            "email": f"booking.delete.{self.test_counter}@example.com",
            "phone": f"7666{self.test_counter % 10000}"
        }
        guest_response = self.session.post(f"{BASE_URL}/guests", json=guest_data)
        guest_id = guest_response.json()['id']
        
        hotel_data = {
            "name": f"Hotel for booking delete {self.test_counter}",
            "address": "Address for booking delete",
            "city": "City for booking delete",
            "rating": 3.0
        }
        hotel_response = self.session.post(f"{BASE_URL}/hotels", json=hotel_data)
        hotel_id = hotel_response.json()['id']
        
        room_type_data = {
            "name": f"Room type for booking delete {self.test_counter}",
            "description": "Description for booking delete",
            "capacity": 2
        }
        room_type_response = self.session.post(f"{BASE_URL}/room_types", json=room_type_data)
        room_type_id = room_type_response.json()['id']
        
        room_data = {
            "hotel_id": hotel_id,
            "room_type_id": room_type_id,
            "room_number": 888,
            "price_per_night": 150,
            "is_available": 1
        }
        room_response = self.session.post(f"{BASE_URL}/rooms", json=room_data)
        room_id = room_response.json()['id']
        
        booking_data = {
            "guest_id": guest_id,
            "room_id": room_id,
            "check_in_date": "2024-07-01",
            "check_out_date": "2024-07-03",
            "total_price": 300,
            "status": "confirmed"
        }
        response = self.session.post(f"{BASE_URL}/bookings", json=booking_data)
        assert response.status_code == 200
        booking_id = response.json()['id']
        
        response = self.session.delete(f"{BASE_URL}/bookings/{booking_id}")
        assert response.status_code == 200
        
        response = self.session.get(f"{BASE_URL}/bookings/{booking_id}")
        assert response.status_code == 404
        
        self.session.delete(f"{BASE_URL}/guests/{guest_id}")
        self.session.delete(f"{BASE_URL}/rooms/{room_id}")
        self.session.delete(f"{BASE_URL}/hotels/{hotel_id}")
        self.session.delete(f"{BASE_URL}/room_types/{room_type_id}")
    
    def test_search_available_rooms(self):
        """Тест поиска доступных номеров"""
        response = self.session.get(f"{BASE_URL}/rooms/search/available_rooms")
        assert response.status_code == 200
        rooms = response.json()
        assert isinstance(rooms, list)
    
    def test_get_hotel_rooms(self):
        """Тест получения номеров отеля"""
        if 'hotel_id' not in self.test_data:
            self.test_create_hotel()
        
        response = self.session.get(f"{BASE_URL}/hotels/{self.test_data['hotel_id']}/rooms")
        assert response.status_code == 200
        rooms = response.json()
        assert isinstance(rooms, list)
    
    def test_error_cases(self):
        """Тест обработки ошибок"""
        response = self.session.get(f"{BASE_URL}/hotels/999999")
        assert response.status_code == 404
        
        response = self.session.get(f"{BASE_URL}/rooms/999999")
        assert response.status_code == 404

def run_api_tests():
    """Запуск всех API тестов"""
    print("Запуск API тестов...")
    
    tester = HotelAPITests()
    tests_passed = 0
    tests_failed = 0
    
    tests = [
        # Основные тесты
        (tester.test_server_availability, "Проверка доступности сервера"),
        
        # Тесты отелей
        (tester.test_get_hotels, "Получение списка отелей"),
        (tester.test_create_hotel, "Создание отеля"),
        (tester.test_get_single_hotel, "Получение отеля по ID"),
        (tester.test_update_hotel, "Обновление отеля"),
        (tester.test_delete_hotel, "Удаление отеля"),
        
        # Тесты типов комнат
        (tester.test_get_room_types, "Получение списка типов комнат"),
        (tester.test_create_room_type, "Создание типа комнаты"),
        (tester.test_get_single_room_type, "Получение типа комнаты по ID"),
        (tester.test_update_room_type, "Обновление типа комнаты"),
        (tester.test_delete_room_type, "Удаление типа комнаты"),
        
        # Тесты гостей
        (tester.test_get_guests, "Получение списка гостей"),
        (tester.test_create_guest, "Создание гостя"),
        (tester.test_get_single_guest, "Получение гостя по ID"),
        (tester.test_update_guest, "Обновление гостя"),
        (tester.test_delete_guest, "Удаление гостя"),
        
        # Тесты комнат
        (tester.test_get_rooms, "Получение списка комнат"),
        (tester.test_create_room, "Создание комнаты"),
        (tester.test_get_single_room, "Получение комнаты по ID"),
        (tester.test_update_room, "Обновление комнаты"),
        (tester.test_delete_room, "Удаление комнаты"),
        
        # Тесты бронирований
        (tester.test_get_bookings, "Получение списка бронирований"),
        (tester.test_create_booking, "Создание бронирования"),
        (tester.test_get_single_booking, "Получение бронирования по ID"),
        (tester.test_update_booking, "Обновление бронирования"),
        (tester.test_delete_booking, "Удаление бронирования"),
        
        # Дополнительные тесты
        (tester.test_search_available_rooms, "Поиск доступных номеров"),
        (tester.test_get_hotel_rooms, "Получение номеров отеля"),
        (tester.test_error_cases, "Проверка обработки ошибок"),
    ]
    
    for test_func, test_name in tests:
        if tester.run_test(test_func, test_name):
            tests_passed += 1
        else:
            tests_failed += 1
    
    print("\nОчистка тестовых данных...")
    tester.cleanup()
    
    print(f"\n=== Результаты API тестов ===")
    print(f"Успешно: {tests_passed}")
    print(f"Провалено: {tests_failed}")
    print(f"Всего: {tests_passed + tests_failed}")
    
    return tests_failed == 0

if __name__ == "__main__":
    print("Ожидание запуска сервера...")
    time.sleep(3)
    
    success = run_api_tests()
    sys.exit(0 if success else 1)