from database import create_database_and_tables
from rooms import add_room, get_available_rooms
from reservations import create_reservation
from utils import str_to_date

if __name__ == "__main__":
    db_path = 'hotel_reservation_system.db'

    # Crear las tablas
    create_database_and_tables(db_path)

    # Agregar habitaciones
    add_room(db_path, "101")
    add_room(db_path, "102")
    add_room(db_path, "103")

    # Crear una reserva
    reservation_owner = "John Doe"
    reservation_start_date = str_to_date("2024-07-15")
    reservation_end_date = str_to_date("2024-07-20")
    room_id = 1  # ID de la habitación

    # Verificar disponibilidad antes de reservar
    available_rooms = get_available_rooms(db_path, reservation_start_date, reservation_end_date)
    if available_rooms:
        create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, room_id)
    else:
        print("No rooms available for the selected dates.")
