import pytest
from src.controllers.places_controller import (
    create_places_table,
    add_place,
    delete_place,
    load_places
)
from src.db.db import get_connection

@pytest.fixture(scope="module")
def setup_test_db():
    create_places_table()
    yield
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS places;")
    conn.commit()
    cur.close()
    conn.close()

def test_crud_places(setup_test_db):
    # Create
    new_place = {
        "name": "Test Place",
        "city": "Test City",
        "country": "Test Country",
        "note": "Test note",
        "visited": False,
        "priority": 1
    }
    add_place(new_place)

    # Read
    places = load_places()
    assert any(p["name"] == "Test Place" for p in places)

    # Update
    place = next(p for p in places if p["name"] == "Test Place")
    place["note"] = "Updated note"
    place["visited"] = True
    from src.controllers.places_controller import update_place
    update_place(place)

    updated_place = next(p for p in load_places() if p["name"] == "Test Place")
    assert updated_place["note"] == "Updated note"
    assert updated_place["visited"] is True

    # Delete
    delete_place(place["id"])
    places_after_delete = load_places()
    assert not any(p["name"] == "Test Place" for p in places_after_delete)
