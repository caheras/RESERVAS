import sqlite3

def create_reservation(db_path, reservation_owner, reservation_start_date, reservation_end_date, room_id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    insert_reservation_sql = '''
    INSERT INTO Reservations (reservation_owner, reservation_start_date, reservation_end_date, room_id)
    VALUES (?, ?, ?, ?);
    '''
    
    update_room_status_sql = '''
    UPDATE Rooms
    SET is_occupied = 1
    WHERE room_id = ?;
    '''

    try:
        cur.execute(insert_reservation_sql, (reservation_owner, reservation_start_date, reservation_end_date, room_id))
        cur.execute(update_room_status_sql, (room_id,))
        conn.commit()
        print("Reservation added and room status updated successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
