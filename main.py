from database import create_database
from rooms import get_available_rooms_and_beds
from reservations import create_reservation
from utils import str_to_date

if __name__ == "__main__":
    db_path = 'hotel_reservation_system.db'
    create_database(db_path)	

    reservation_owner = "John Doe"
    reservation_start_date = str_to_date("2024-07-15")
    reservation_end_date = str_to_date("2024-07-20")

    available = get_available_rooms_and_beds(db_path, reservation_start_date, reservation_end_date)
    print("Available private rooms:", available['private_rooms'])
    print("Available shared beds:", available['shared_beds'])

    if available['private_rooms']:
        room_id = available['private_rooms'][0][0]
        create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, room_id=room_id)
    elif available['shared_beds']:
        bed_id = available['shared_beds'][0][0]
        create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, bed_id=bed_id)
    else:
        print("No available rooms or beds for the selected dates.")

    create_reservation(db_path, "Jane Smith", str_to_date("2024-07-15"), str_to_date("2024-07-20"), bed_id=1)
    create_reservation(db_path, "Jane Smith", str_to_date("2024-07-15"), str_to_date("2024-07-20"), bed_id=1)

