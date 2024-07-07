import sqlite3

def add_room(db_path, room_number, room_type):
    """
    Agrega una nueva habitación a la base de datos.

    Parámetros:
        db_path (str): La ruta al archivo de la base de datos SQLite.
        room_number (str): El número de la habitación a agregar.
        room_type (str): El tipo de habitación ('private' o 'shared').
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_room_sql = '''
    INSERT INTO Rooms (room_number, room_type, is_occupied)
    VALUES (?, ?, 0);
    '''

    try:
        cur.execute(insert_room_sql, (room_number, room_type))
        conn.commit()
        print("Room added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def add_bed(db_path, room_id):
    """
    Agrega una nueva cama a una habitación compartida.

    Parámetros:
        db_path (str): La ruta al archivo de la base de datos SQLite.
        room_id (int): El ID de la habitación a la que se va a agregar la cama.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_bed_sql = '''
    INSERT INTO Beds (room_id, is_occupied)
    VALUES (?, 0);
    '''

    try:
        cur.execute(insert_bed_sql, (room_id,))
        conn.commit()
        print("Bed added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_available_rooms_and_beds(db_path, start_date, end_date):
    """
    Obtiene una lista de habitaciones privadas y camas en habitaciones compartidas disponibles para un rango de fechas.

    Parámetros:
        db_path (str): La ruta al archivo de la base de datos SQLite.
        start_date (date): La fecha de inicio del rango.
        end_date (date): La fecha de fin del rango.

    Retorna:
        dict: Un diccionario con habitaciones privadas y camas compartidas disponibles.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    get_private_rooms_sql = '''
    SELECT room_id, room_number FROM Rooms
    WHERE room_type = 'private'
    AND is_occupied = 0
    AND room_id NOT IN (
        SELECT room_id FROM Reservations
        WHERE (reservation_start_date <= ? AND reservation_end_date >= ?)
    );
    '''

    get_shared_beds_sql = '''
    SELECT Beds.bed_id, Rooms.room_number FROM Beds
    JOIN Rooms ON Beds.room_id = Rooms.room_id
    WHERE Rooms.room_type = 'shared'
    AND Beds.is_occupied = 0
    AND Beds.bed_id NOT IN (
        SELECT bed_id FROM Reservations
        WHERE (reservation_start_date <= ? AND reservation_end_date >= ?)
    );
    '''

    try:
        cur.execute(get_private_rooms_sql, (end_date, start_date))
        private_rooms = cur.fetchall()
        
        cur.execute(get_shared_beds_sql, (end_date, start_date))
        shared_beds = cur.fetchall()

        return {'private_rooms': private_rooms, 'shared_beds': shared_beds}
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {'private_rooms': [], 'shared_beds': []}
    finally:
        conn.close()
