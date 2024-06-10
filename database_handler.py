from flask import Flask, request, send_from_directory
import sqlite3
import cv2
import uuid
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = 'mydatabase.db'
DB_PATH = os.path.join(BASE_DIR, DATABASE)
# Create a connection to the SQLite database (or create it if not exists)
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id TEXT PRIMARY KEY,
        number_plate TEXT,
        state TEXT,
        entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

table_names = [table[0] for table in tables]
print("Tables in the database:", table_names)
conn.commit()
conn.close()


def create(item):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Store each frame in the database along with the video ID
        newUUID = str(uuid.uuid4())
        status = cv2.imwrite(
            'upload/images/'+newUUID+".png", item['img'])
        print(status)
        state = item['state']
        plate = item['plate']
        cursor.execute('INSERT INTO cars (id,number_plate,state) VALUES (?,?,?)',
                       (newUUID, plate, state))

        # Commit the changes
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def get_all_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve all image data from the database
    cursor.execute('SELECT id,number_plate,state,entry_time FROM cars')
    data = cursor.fetchall()

    # Close the connection
    conn.close()
    return data


def append_details(plate_details):
    for idx in range(len(plate_details)):
        create(plate_details[idx])
