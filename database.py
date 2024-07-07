import sqlite3

def create_database_and_tables(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    create_rooms_table = '''
    CREATE TABLE IF NOT EXISTS Rooms (
        room_id INTEGER PRIMARY KEY,
        room_number TEXT NOT NULL,
        is_occupied BOOLEAN NOT NULL DEFAULT 0
    );
    '''
    
    create_reservations_table = '''
    CREATE TABLE IF NOT EXISTS Reservations (
        reservation_id INTEGER PRIMARY KEY,
        reservation_owner TEXT NOT NULL,
        reservation_start_date DATE NOT NULL,
        reservation_end_date DATE NOT NULL,
        room_id INTEGER,
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
    );
    '''

    try:
        cur.execute(create_rooms_table)
        cur.execute(create_reservations_table)
        conn.commit()
        print("Tables created successfully or already exist.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        conn.close()
