import sqlite3

def create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, room_id=None, bed_id=None):
    """
    Crea una nueva reserva para una habitación privada o una cama en una habitación compartida.

    Parámetros:
        db_path (str): La ruta al archivo de la base de datos SQLite.
        reservation_owner (str): El nombre del dueño de la reserva.
        reservation_start_date (date): La fecha de inicio de la reserva.
        reservation_end_date (date): La fecha de fin de la reserva.
        room_id (int, opcional): El ID de la habitación privada a reservar.
        bed_id (int, opcional): El ID de la cama a reservar en una habitación compartida.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_reservation_sql = '''
    INSERT INTO Reservations (reservation_owner, reservation_start_date, reservation_end_date, room_id, bed_id)
    VALUES (?, ?, ?, ?, ?);
    '''

    if room_id:
        update_room_status_sql = '''
        UPDATE Rooms
        SET is_occupied = 1
        WHERE room_id = ?;
        '''
    elif bed_id:
        update_bed_status_sql = '''
        UPDATE Beds
        SET is_occupied = 1
        WHERE bed_id = ?;
        '''

    try:
        cur.execute(insert_reservation_sql, (reservation_owner, reservation_start_date, reservation_end_date, room_id, bed_id))
        
        if room_id:
            cur.execute(update_room_status_sql, (room_id,))
        elif bed_id:
            cur.execute(update_bed_status_sql, (bed_id,))

        conn.commit()
        print("Reservation added and room/bed status updated successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
