import sqlite3

def add_room(db_path, room_number, room_type):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_room_sql = '''
    INSERT INTO Rooms (room_number, room_type)
    VALUES (?, ?);
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
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_bed_sql = '''
    INSERT INTO Beds (room_id)
    VALUES (?);
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
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    get_private_rooms_sql = '''
    SELECT room_id, room_number FROM Rooms
    WHERE room_type = 'private'
    AND room_id NOT IN (
        SELECT room_id FROM Reservations
        WHERE (? <= reservation_end_date AND ? >= reservation_start_date)
    );
    '''

    get_shared_beds_sql = '''
    SELECT Beds.bed_id, Rooms.room_number FROM Beds
    JOIN Rooms ON Beds.room_id = Rooms.room_id
    WHERE Rooms.room_type = 'shared'
    AND Beds.bed_id NOT IN (
        SELECT bed_id FROM Reservations
        WHERE (? <= reservation_end_date AND ? >= reservation_start_date)
    );
    '''

    try:
        cur.execute(get_private_rooms_sql, (start_date, end_date))
        private_rooms = cur.fetchall()
        
        cur.execute(get_shared_beds_sql, (start_date, end_date))
        shared_beds = cur.fetchall()

        return {'private_rooms': private_rooms, 'shared_beds': shared_beds}
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {'private_rooms': [], 'shared_beds': []}
    finally:
        conn.close()
