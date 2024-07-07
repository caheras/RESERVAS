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

    check_conflict_sql = '''
    SELECT * FROM Reservations
    WHERE (reservation_start_date <= ? AND reservation_end_date >= ?)
    AND (room_id = ? OR bed_id = ?);
    '''

    insert_reservation_sql = '''
    INSERT INTO Reservations (reservation_owner, reservation_start_date, reservation_end_date, room_id, bed_id)
    VALUES (?, ?, ?, ?, ?);
    '''

    try:
        # Verificar si hay conflictos de fechas
        cur.execute(check_conflict_sql, (reservation_end_date, reservation_start_date, room_id, bed_id))
        conflicts = cur.fetchall()

        if conflicts:
            print("Error: La habitación o cama ya está reservada para las fechas seleccionadas.")
            return

        cur.execute(insert_reservation_sql, (reservation_owner, reservation_start_date, reservation_end_date, room_id, bed_id))
        conn.commit()
        print("Reservation added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
