from database import create_database_and_tables, create_database
from rooms import add_room, add_bed, get_available_rooms_and_beds
from reservations import create_reservation
from utils import str_to_date

if __name__ == "__main__":
    db_path = 'hotel_reservation_system.db'
    

    # Crear una reserva
    reservation_owner = "John Doe"
    reservation_start_date = str_to_date("2024-07-15")
    reservation_end_date = str_to_date("2024-07-20")

    # Verificar disponibilidad antes de reservar
    available = get_available_rooms_and_beds(db_path, reservation_start_date, reservation_end_date)
    print("Available private rooms:", available['private_rooms'])
    print("Available shared beds:", available['shared_beds'])

    # Realizar una reserva de una habitación privada si está disponible
    if available['private_rooms']:
        room_id = available['private_rooms'][0][0]  # Obtiene el ID de la primera habitación privada disponible
        create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, room_id=room_id)
    elif available['shared_beds']:
        bed_id = available['shared_beds'][0][0]  # Obtiene el ID de la primera cama disponible en una habitación compartida
        create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, bed_id=bed_id)
    else:
        print("No available rooms or beds for the selected dates.")

    # Realizar una reserva de una cama en una habitación compartida
    create_reservation(db_path, "Jane Smith", str_to_date("2024-07-15"), str_to_date("2024-07-20"), bed_id=1)