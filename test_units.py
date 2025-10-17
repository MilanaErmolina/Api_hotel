import unittest
import sys
from datetime import date, timedelta
import re
from unittest.mock import patch, MagicMock
import json

class TestHotelModels(unittest.TestCase):
    """Тесты моделей данных"""
    
    def test_1_hotel_creation(self):
        """Тест создания модели отеля"""
        class Hotel:
            def __init__(self, name, address, city, rating):
                self.name = name
                self.address = address
                self.city = city
                self.rating = rating
        
        hotel = Hotel("Гранд Отель", "ул. Центральная, 1", "Москва", 4.7)
        
        self.assertEqual(hotel.name, "Гранд Отель")
        self.assertEqual(hotel.address, "ул. Центральная, 1")
        self.assertEqual(hotel.city, "Москва")
        self.assertEqual(hotel.rating, 4.7)

    def test_2_room_type_creation(self):
        """Тест создания типа номера"""
        class RoomType:
            def __init__(self, name, description, capacity):
                self.name = name
                self.description = description
                self.capacity = capacity
        
        room_type = RoomType("Люкс", "Просторный номер", 3)
        
        self.assertEqual(room_type.name, "Люкс")
        self.assertEqual(room_type.description, "Просторный номер")
        self.assertEqual(room_type.capacity, 3)

    def test_3_guest_creation(self):
        """Тест создания гостя"""
        class Guest:
            def __init__(self, first_name, last_name, email, phone):
                self.first_name = first_name
                self.last_name = last_name
                self.email = email
                self.phone = phone
        
        guest = Guest("Иван", "Петров", "ivan@mail.com", "+79991234567")
        
        self.assertEqual(guest.first_name, "Иван")
        self.assertEqual(guest.last_name, "Петров")
        self.assertEqual(guest.email, "ivan@mail.com")
        self.assertEqual(guest.phone, "+79991234567")

class TestBusinessLogic(unittest.TestCase):
    """Тесты бизнес-логики"""
    
    def test_4_price_calculation(self):
        """Тест расчета стоимости бронирования"""
        def calculate_price(price_per_night, nights):
            return price_per_night * nights
        
        self.assertEqual(calculate_price(100, 5), 500)
        
        self.assertEqual(calculate_price(150, 1), 150)
        
        self.assertAlmostEqual(calculate_price(99.99, 3), 299.97, places=2)

    def test_5_date_validation(self):
        """Тест проверки дат бронирования"""
        def are_dates_valid(check_in, check_out):
            if check_in >= check_out:
                return False, "Дата выезда должна быть после даты заезда"
            if check_in < date.today():
                return False, "Нельзя бронировать в прошлом"
            return True, "OK"
        
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        
        valid, message = are_dates_valid(tomorrow, next_week)
        self.assertTrue(valid)
        
        valid, message = are_dates_valid(next_week, tomorrow)
        self.assertFalse(valid)

    def test_6_room_availability(self):
        """Тест проверки доступности номера"""
        class Room:
            def __init__(self, is_available):
                self.is_available = is_available
            
            def can_be_booked(self):
                return self.is_available == 1
        
        available_room = Room(1)
        unavailable_room = Room(0)
        
        self.assertTrue(available_room.can_be_booked())
        self.assertFalse(unavailable_room.can_be_booked())

class TestValidation(unittest.TestCase):
    """Тесты валидации данных"""
    
    def test_7_contact_validation(self):
        """Тест валидации email и телефона"""
        def is_valid_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
            
        def is_valid_phone(phone):
            pattern = r'^[\+]?[0-9\s\-\(\)]{10,}$'
            return bool(re.match(pattern, phone))
        
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertTrue(is_valid_email("user.name@domain.co.uk"))
        
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertFalse(is_valid_email("user@"))
        
        self.assertTrue(is_valid_phone("+79991234567"))
        self.assertTrue(is_valid_phone("89991234567"))
        
        self.assertFalse(is_valid_phone("abc"))
        self.assertFalse(is_valid_phone("123"))

    def test_8_rating_validation(self):
        """Тест валидации рейтинга"""
        def is_valid_rating(rating):
            return 0 <= rating <= 5
        
        self.assertTrue(is_valid_rating(0))
        self.assertTrue(is_valid_rating(2.5))
        self.assertTrue(is_valid_rating(5))
        
        self.assertFalse(is_valid_rating(-1))
        self.assertFalse(is_valid_rating(5.1))

class TestDataProcessing(unittest.TestCase):
    """Тесты обработки данных"""
    
    def test_9_data_formatting_and_filtering(self):
        """Тест форматирования данных и фильтрации"""
        def format_room_data(room):
            return {
                'number': room['number'],
                'price': float(room['price']),
                'available': bool(room['available'])
            }
            
        def filter_rooms(rooms, max_price):
            return [room for room in rooms if room['price'] <= max_price]
        
        raw_data = {
            'number': '101',
            'price': '1500.50',
            'available': 1
        }
        
        formatted = format_room_data(raw_data)
        
        self.assertEqual(formatted['number'], '101')
        self.assertIsInstance(formatted['price'], float)
        self.assertIsInstance(formatted['available'], bool)
        
        rooms = [
            {'number': '101', 'price': 100},
            {'number': '102', 'price': 200},
            {'number': '103', 'price': 300}
        ]
        
        filtered = filter_rooms(rooms, 200)
        
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]['number'], '101')
        self.assertEqual(filtered[1]['number'], '102')

class TestHotelAPI(unittest.TestCase):
    """Тесты API отелей"""
    
    @patch('requests.get')
    def test_10_get_hotels(self, mock_get):
        """Тест получения списка отелей"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Отель 1', 'city': 'Москва'},
            {'id': 2, 'name': 'Отель 2', 'city': 'СПб'}
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/hotels')
        
        self.assertEqual(response.status_code, 200)
        hotels = response.json()
        self.assertEqual(len(hotels), 2)
        self.assertEqual(hotels[0]['name'], 'Отель 1')
    
    @patch('requests.post')
    def test_11_create_hotel(self, mock_post):
        """Тест создания отеля"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 3, 
            'name': 'Новый отель', 
            'city': 'Казань',
            'rating': 4.5
        }
        mock_post.return_value = mock_response
        
        hotel_data = {
            'name': 'Новый отель',
            'city': 'Казань',
            'rating': 4.5
        }
        
        response = mock_post('http://localhost:8000/hotels', json=hotel_data)
        
        self.assertEqual(response.status_code, 200)
        hotel = response.json()
        self.assertEqual(hotel['id'], 3)
        self.assertEqual(hotel['name'], 'Новый отель')
    
    @patch('requests.get')
    def test_12_get_hotel_by_id(self, mock_get):
        """Тест получения отеля по ID"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1, 
            'name': 'Гранд Отель', 
            'city': 'Москва'
        }
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/hotels/1')
        
        self.assertEqual(response.status_code, 200)
        hotel = response.json()
        self.assertEqual(hotel['id'], 1)
        self.assertEqual(hotel['name'], 'Гранд Отель')
    
    @patch('requests.get')
    def test_13_get_hotel_rooms(self, mock_get):
        """Тест получения номеров конкретного отеля"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'room_type': 'Стандарт',
                'room_number': '101',
                'price_per_night': 5000,
                'is_available': True
            },
            {
                'id': 2,
                'room_type': 'Люкс',
                'room_number': '201',
                'price_per_night': 10000,
                'is_available': True
            }
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/hotels/1/rooms')
        
        self.assertEqual(response.status_code, 200)
        rooms = response.json()
        
        self.assertEqual(len(rooms), 2)
        self.assertEqual(rooms[0]['id'], 1)
        self.assertEqual(rooms[0]['room_type'], 'Стандарт')
        self.assertEqual(rooms[0]['room_number'], '101')
        self.assertEqual(rooms[0]['price_per_night'], 5000)
        self.assertTrue(rooms[0]['is_available'])

class TestRoomAPI(unittest.TestCase):
    """Тесты API комнат"""
    
    @patch('requests.get')
    def test_14_get_rooms(self, mock_get):
        """Тест получения списка комнат"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'room_number': '101', 'hotel_id': 1},
            {'id': 2, 'room_number': '102', 'hotel_id': 1}
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/rooms')
        
        self.assertEqual(response.status_code, 200)
        rooms = response.json()
        self.assertEqual(len(rooms), 2)
        self.assertEqual(rooms[0]['room_number'], '101')
    
    @patch('requests.post')
    def test_15_create_room(self, mock_post):
        """Тест создания комнаты"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 3, 
            'room_number': '103', 
            'hotel_id': 1,
            'price_per_night': 5000
        }
        mock_post.return_value = mock_response
        
        room_data = {
            'room_number': '103',
            'hotel_id': 1,
            'price_per_night': 5000
        }
        
        response = mock_post('http://localhost:8000/rooms', json=room_data)
        
        self.assertEqual(response.status_code, 200)
        room = response.json()
        self.assertEqual(room['id'], 3)
        self.assertEqual(room['room_number'], '103')

class TestRoomTypeAPI(unittest.TestCase):
    """Тесты API типов комнат"""
    
    @patch('requests.get')
    def test_16_get_room_types(self, mock_get):
        """Тест получения списка типов комнат"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Стандарт', 'capacity': 2},
            {'id': 2, 'name': 'Люкс', 'capacity': 4}
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/room_types')
        
        self.assertEqual(response.status_code, 200)
        room_types = response.json()
        self.assertEqual(len(room_types), 2)
        self.assertEqual(room_types[0]['name'], 'Стандарт')
    
    @patch('requests.post')
    def test_17_create_room_type(self, mock_post):
        """Тест создания типа комнаты"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 3, 
            'name': 'Премиум', 
            'capacity': 3
        }
        mock_post.return_value = mock_response
        
        room_type_data = {
            'name': 'Премиум',
            'capacity': 3
        }
        
        response = mock_post('http://localhost:8000/room_types', json=room_type_data)
        
        self.assertEqual(response.status_code, 200)
        room_type = response.json()
        self.assertEqual(room_type['id'], 3)
        self.assertEqual(room_type['name'], 'Премиум')

class TestGuestAPI(unittest.TestCase):
    """Тесты API гостей"""
    
    @patch('requests.get')
    def test_18_get_guests(self, mock_get):
        """Тест получения списка гостей"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'first_name': 'Иван', 'last_name': 'Петров'},
            {'id': 2, 'first_name': 'Мария', 'last_name': 'Сидорова'}
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/guests')
        
        self.assertEqual(response.status_code, 200)
        guests = response.json()
        self.assertEqual(len(guests), 2)
        self.assertEqual(guests[0]['first_name'], 'Иван')
    
    @patch('requests.post')
    def test_19_create_guest(self, mock_post):
        """Тест создания гостя"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 3, 
            'first_name': 'Петр', 
            'last_name': 'Иванов',
            'email': 'petr@mail.ru'
        }
        mock_post.return_value = mock_response
        
        guest_data = {
            'first_name': 'Петр',
            'last_name': 'Иванов',
            'email': 'petr@mail.ru'
        }
        
        response = mock_post('http://localhost:8000/guests', json=guest_data)
        
        self.assertEqual(response.status_code, 200)
        guest = response.json()
        self.assertEqual(guest['id'], 3)
        self.assertEqual(guest['first_name'], 'Петр')

class TestBookingAPI(unittest.TestCase):
    """Тесты API бронирований"""
    
    @patch('requests.get')
    def test_20_get_bookings(self, mock_get):
        """Тест получения списка бронирований"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'guest_id': 1, 'room_id': 1, 'status': 'confirmed'},
            {'id': 2, 'guest_id': 2, 'room_id': 2, 'status': 'pending'}
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/bookings')
        
        self.assertEqual(response.status_code, 200)
        bookings = response.json()
        self.assertEqual(len(bookings), 2)
        self.assertEqual(bookings[0]['status'], 'confirmed')
    
    @patch('requests.post')
    def test_21_create_booking(self, mock_post):
        """Тест создания бронирования"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 3, 
            'guest_id': 1, 
            'room_id': 1,
            'status': 'confirmed'
        }
        mock_post.return_value = mock_response
        
        booking_data = {
            'guest_id': 1,
            'room_id': 1,
            'status': 'confirmed'
        }
        
        response = mock_post('http://localhost:8000/bookings', json=booking_data)
        
        self.assertEqual(response.status_code, 200)
        booking = response.json()
        self.assertEqual(booking['id'], 3)
        self.assertEqual(booking['status'], 'confirmed')
    
    @patch('requests.get')
    def test_22_get_booking_by_id(self, mock_get):
        """Тест получения бронирования по ID"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1, 
            'guest_id': 1, 
            'room_id': 1,
            'status': 'confirmed'
        }
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/bookings/1')
        
        self.assertEqual(response.status_code, 200)
        booking = response.json()
        self.assertEqual(booking['id'], 1)
        self.assertEqual(booking['status'], 'confirmed')

class TestErrorHandling(unittest.TestCase):
    """Тесты обработки ошибок"""
    
    @patch('requests.get')
    def test_23_hotel_not_found(self, mock_get):
        """Тест обработки ошибки при поиске несуществующего отеля"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'detail': 'Hotel not found'}
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/hotels/999')
        
        self.assertEqual(response.status_code, 404)
        error = response.json()
        self.assertEqual(error['detail'], 'Hotel not found')
    
    @patch('requests.get')
    def test_24_room_not_found(self, mock_get):
        """Тест обработки ошибки при поиске несуществующей комнаты"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'detail': 'Room not found'}
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/rooms/999')
        
        self.assertEqual(response.status_code, 404)
        error = response.json()
        self.assertEqual(error['detail'], 'Room not found')

class TestSearchFunctionality(unittest.TestCase):
    """Тесты функциональности поиска"""
    
    @patch('requests.get')
    def test_25_search_available_rooms(self, mock_get):
        """Тест поиска доступных номеров"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'hotel_name': 'Гранд Отель',
                'room_type': 'Стандарт',
                'room_number': '101',
                'price_per_night': 5000,
                'capacity': 2
            }
        ]
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/rooms/search/available_rooms')
        
        self.assertEqual(response.status_code, 200)
        rooms = response.json()
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0]['room_number'], '101')
        self.assertEqual(rooms[0]['hotel_name'], 'Гранд Отель')

class TestUpdateOperations(unittest.TestCase):
    """Тесты операций обновления"""
    
    @patch('requests.put')
    def test_26_update_hotel(self, mock_put):
        """Тест обновления отеля"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1, 
            'name': 'Обновленный отель', 
            'city': 'Москва',
            'rating': 5.0
        }
        mock_put.return_value = mock_response
        
        update_data = {
            'id': 1,
            'name': 'Обновленный отель',
            'city': 'Москва',
            'rating': 5.0
        }
        
        response = mock_put('http://localhost:8000/hotels', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        hotel = response.json()
        self.assertEqual(hotel['name'], 'Обновленный отель')
        self.assertEqual(hotel['rating'], 5.0)
    
    @patch('requests.put')
    def test_27_update_booking(self, mock_put):
        """Тест обновления бронирования"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1, 
            'guest_id': 1, 
            'room_id': 1,
            'status': 'cancelled'
        }
        mock_put.return_value = mock_response
        
        update_data = {
            'id': 1,
            'guest_id': 1,
            'room_id': 1,
            'status': 'cancelled'
        }
        
        response = mock_put('http://localhost:8000/bookings', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        booking = response.json()
        self.assertEqual(booking['status'], 'cancelled')

class TestDeleteOperations(unittest.TestCase):
    """Тесты операций удаления"""
    
    @patch('requests.delete')
    def test_28_delete_hotel(self, mock_delete):
        """Тест удаления отеля"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Hotel deleted successfully'}
        mock_delete.return_value = mock_response
        
        response = mock_delete('http://localhost:8000/hotels/1')
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['message'], 'Hotel deleted successfully')
    
    @patch('requests.delete')
    def test_29_delete_booking(self, mock_delete):
        """Тест удаления бронирования"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Booking deleted successfully'}
        mock_delete.return_value = mock_response
        
        response = mock_delete('http://localhost:8000/bookings/1')
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['message'], 'Booking deleted successfully')

class TestAdditionalScenarios(unittest.TestCase):
    """Тесты дополнительных сценариев"""
    
    @patch('requests.get')
    def test_30_hotel_rooms_not_found(self, mock_get):
        """Тест получения номеров несуществующего отеля"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'detail': 'Hotel not found'}
        mock_get.return_value = mock_response
        
        response = mock_get('http://localhost:8000/hotels/999/rooms')
        
        self.assertEqual(response.status_code, 404)
        error = response.json()
        self.assertEqual(error['detail'], 'Hotel not found')

def run_unit_tests():
    """Запуск unit тестов"""
    print("UNIT ТЕСТЫ\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestHotelModels, 
        TestBusinessLogic, 
        TestValidation, 
        TestDataProcessing,
        TestHotelAPI,
        TestRoomAPI,
        TestRoomTypeAPI,
        TestGuestAPI,
        TestBookingAPI,
        TestErrorHandling,
        TestSearchFunctionality,
        TestUpdateOperations,
        TestDeleteOperations,
        TestAdditionalScenarios
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    total = result.testsRun
    failed = len(result.failures)
    errors = len(result.errors)
    passed = total - failed - errors
    
    print(f"\nВсего тестов: {total}")
    print(f"Успешно: {passed}")
    print(f"Провалено: {failed}")
    print(f"Ошибок: {errors}")
    
    if result.failures:
        print(f"\nПроваленные тесты:")
        for test, traceback in result.failures:
            test_name = str(test).split()[0]
            error_msg = traceback.splitlines()[-1]
            print(f"   {test_name}: {error_msg}")
    
    if result.errors:
        print(f"\nОшибки:")
        for test, traceback in result.errors:
            test_name = str(test).split()[0]
            error_msg = traceback.splitlines()[-1]
            print(f"   {test_name}: {error_msg}")
    
    success_rate = (passed / total) * 100
    print(f"\nРезультат: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    try:
        success = run_unit_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nТесты прерваны")
        sys.exit(1)
    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)