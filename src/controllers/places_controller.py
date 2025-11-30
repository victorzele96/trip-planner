import os
import json
import uuid
from src.db.db import get_connection

# CRUD - Create | Read | Update | Delete
DEFAULT_VISITED = False
DEFAULT_PRIORITY = 3

def create_places_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            city VARCHAR(100),
            country VARCHAR(100),
            note TEXT,
            visited BOOLEAN DEFAULT FALSE,
            priority INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table 'places' ready!")

def cr_json_places():
    # Getting the current dir of my main.py file 
    current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    folder = os.path.join(current_dir, "data")
    file_path = os.path.join(folder, "places.json")

    # create a new folder if not exists 
    os.makedirs(folder, exist_ok=True)

    # create a new json file if not exists 
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
        print("The folder and JSON file were successfully created.")
        print(f"File path is: {file_path}.\n")
    else:
        print("The folder and JSON file already exist.")
        print(f"File path is: {file_path}.\n")

    return file_path

def load_places():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, city, country, note, visited, priority, created_at FROM places ORDER BY created_at DESC")
    rows = cur.fetchall()
    places = []
    for r in rows:
        places.append({
            "id": r[0],
            "name": r[1],
            "city": r[2],
            "country": r[3],
            "note": r[4],
            "visited": r[5],
            "priority": r[6],
            "created_at": r[7],
        })
    cur.close()
    conn.close()
    return places

def show_places(places, file_path):
    places = load_places(file_path)

    if not places: 
        print("No places found!")
        return []
    
    print(f"All the places in the JSON file.")

    for idx, place in enumerate(places, start=1):
        print(f"Name: {place['name']} \nCity: {place['city']} \nCountry: {place['country']} \nVisited: {place['visited']} \nNotes: {place['notes']} \nPriority: {place['priority']}\n")

def add_place(place):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""INSERT INTO places (name, city, country, note, visited, priority) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (place['name'], place['city'], place['country'], place.get("note", ""), place.get("visited", False), place.get("priority", None)))
    
    conn.commit()
    cur.close()
    conn.close()

    print(f"Added a new place '{place['name']} to the DB.")

def update_place(place):
    places = load_places()

    conn = get_connection()
    cur = conn.cursor()

    if not places:
        print("No place to update.")
        return

    cur.execute("""UPDATE places 
                    SET name=%s, city=%s, country=%s, note=%s, visited=%s, priority=%s 
                        WHERE id=%s 
                """,    (
                            place['name'],
                            place.get('city', ''),
                            place.get('country', ''),
                            place.get('note', ''),
                            place.get('visited', False),
                            place.get('priority', None),
                            place['id']
                        ))
    
    conn.commit()
    cur.close()
    conn.close()

    print(f"Place '{place['name']}' updated successfully!")

def delete_place(place_id):
    places = load_places()

    conn = get_connection()
    cur = conn.cursor()

    if not places:
        print("No place to delete.")
        return []

    cur.execute("""DELETE FROM places
                    WHERE id=%s
                """, (
                    (place_id, )
                ))

    conn.commit()
    cur.close()
    conn.close()

def get_current_dir():
    return cr_json_places()


if __name__ == "__main__":
    #current_dir = cr_json_places()
    create_places_table()

"""
print(f"File directory {current_dir}")
places = load_places(current_dir)
print(f"Json content {places}")

new_place = {
        "name": "City in USA",
        "city": "Vegas",
        "country": "USA",
        "visited": False,
        "notes": "Must see at night",
        "priority": 3,
        "id": "b74b6590-73e1-499c-b544-3cea71dd2e35"
    }

add_place(new_place, current_dir)
#delete_place(new_place, current_dir)
show_places(load_places(current_dir), current_dir)"""

