import sqlite3

def add_room(db_path, room_number):
    """
    Agrega una nueva habitación a la base de datos.

    Parámetros:
        db_path (str): La ruta al archivo de la base de datos SQLite.
        room_number (str): El número de la habitación a agregar.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_room_sql = '''
    INSERT INTO Rooms (room_number, is_occupied)
    VALUES (?, 0);
    '''

    try:
        cur.execute(insert_room_sql, (room_number,))
        conn.commit()
        print("Room added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_available_rooms(db_path, start_date, end_date):
    """
    Obtiene una lista de habitaciones disponibles para un rango de fechas.

    Parámetros:
        db_path (str): La ruta al archivo de la base de datos SQLite.
        start_date (date): La fecha de inicio del rango.
        end_date (date): La fecha de fin del rango.

    Retorna:
        list: Una lista de habitaciones disponibles en el formato (room_id, room_number).
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    get_rooms_sql = '''
    SELECT room_id, room_number FROM Rooms
    WHERE is_occupied = 0
    AND room_id NOT IN (
        SELECT room_id FROM Reservations
        WHERE (reservation_start_date <= ? AND reservation_end_date >= ?)
    );
    '''

    try:
        cur.execute(get_rooms_sql, (end_date, start_date))
        available_rooms = cur.fetchall()
        return available_rooms
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()
