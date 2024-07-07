import sqlite3
from rooms import add_room, add_bed

def create_database_and_tables(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    create_rooms_table = '''
    CREATE TABLE IF NOT EXISTS Rooms (
        room_id INTEGER PRIMARY KEY,
        room_number TEXT NOT NULL,
        room_type TEXT NOT NULL CHECK (room_type IN ('private', 'shared'))
    );
    '''
    
    create_beds_table = '''
    CREATE TABLE IF NOT EXISTS Beds (
        bed_id INTEGER PRIMARY KEY,
        room_id INTEGER NOT NULL,
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
    );
    '''
    
    create_reservations_table = '''
    CREATE TABLE IF NOT EXISTS Reservations (
        reservation_id INTEGER PRIMARY KEY,
        reservation_owner TEXT NOT NULL,
        reservation_start_date DATE NOT NULL,
        reservation_end_date DATE NOT NULL,
        room_id INTEGER,
        bed_id INTEGER,
        FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
        FOREIGN KEY (bed_id) REFERENCES Beds(bed_id)
    );
    '''

    try:
        cur.execute(create_rooms_table)
        cur.execute(create_beds_table)
        cur.execute(create_reservations_table)
        conn.commit()
        print("Tables created successfully or already exist.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        conn.close()
        
def create_database(db_path):
    create_database_and_tables(db_path)
    add_room(db_path, "101", "private")
    add_room(db_path, "102", "private")
    add_room(db_path, "103", "private")
    add_room(db_path, "104", "shared")
    add_room(db_path, "105", "shared")
    add_room(db_path, "106", "shared")

    add_bed(db_path, 4)
    add_bed(db_path, 4)
    add_bed(db_path, 4)
    add_bed(db_path, 5)
    add_bed(db_path, 5)
    add_bed(db_path, 5)
    add_bed(db_path, 6)
    add_bed(db_path, 6)
    add_bed(db_path, 6)
