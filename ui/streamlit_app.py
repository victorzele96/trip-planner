
import streamlit as st
import pandas as pd
from src.controllers.places_controller import add_place, show_places, get_current_dir, load_places, update_place, delete_place, create_places_table

# make sure that the DB exists before running
create_places_table()

file_path = get_current_dir()
places = load_places()
page = st.sidebar.selectbox("Choose Page", ["Home", "Add Place", "View Places", "Edit Place", "Delete Place"])


if page == "Home":
    st.title("Welcome to Trip Planner")

    st.markdown("""
    <div style="
        background-color:#eafaf1;  /* ירוק בהיר טבעי */
        border-radius: 15px;
        padding: 20px 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        ">
        <h2 style="color:#2b7de9;">📌 Project Description</h2>
        <p style="font-size:16px; color:#333;">
            <strong>Trip Planner</strong> is a smart system for managing travel itineraries around the world.  
            It allows users to easily plan, view, and edit their trips using an intuitive interface.
        </p>
        <ul style="font-size:16px; color:#444;">
            <li>🆕 <b>Create</b> new places to visit</li>
            <li>📖 <b>Read</b> and view existing places</li>
            <li>✏️ <b>Update</b> place details</li>
            <li>🗑️ <b>Delete</b> places from your list</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif  page == "Add Place":
    # Input form
    st.title("Add Place")
    name = st.text_input("Place Name")
    city = st.text_input("City")
    country = st.text_input("Country")
    notes = st.text_input("Notes")
    priority = st.number_input("Priority | 1 is the best and 10 is the worst", min_value=1, max_value=10, step=1, value=5)
    visited = st.selectbox("Visited", ["False", "True"])

    if st.button("Add Place"):
        new_place = {"name": name, "city": city, "country": country, "note": notes, "priority": priority, "visited": visited}
        add_place(new_place)
        st.success(f"{name} added!") 

elif page == "View Places":
    st.title("View Places")
    places = load_places() 

    if places:
        df = pd.DataFrame(places).drop(columns=["id"])
        st.dataframe(df)
    else:
        st.write("No places yet.")

elif  page == "Edit Place":
    # Display all places
    st.title("Edit Place")
    place_names = [p['name'] for p in places]
    selected_name = st.selectbox("Select place to edit", [""] + place_names)
    selected_place = next((p for p in places if p["name"] == selected_name), None)

    if selected_place:   
        st.write(f"Editing: {selected_name}")
        name = st.text_input("Place Name", value=selected_place["name"])
        city = st.text_input("City", value=selected_place["city"])
        country = st.text_input("Country", value=selected_place["country"])
        note = st.text_input("Note", value=selected_place.get("note", ""))
        visited = st.text_input("Visited", value=selected_place.get("visited", ""))
        priority = st.text_input("Priority", value=selected_place.get("priority", ""))
        id = selected_place["id"]

        new_place = {"name": name, "city": city, "country": country, "visited": visited, "priority": priority, "note": note, "id": id}

        if new_place != selected_place:
            if st.button("Edit Place"):
                update_place(new_place)
                st.success(f"{name} updated!")
        else:
            st.info("Change at least one field to enable the button.")

    else:
        st.warning("Please select a valid place to edit.")

elif  page == "Delete Place":
    # Display all places
    st.title("Delete Place")
    place_names = [p['name'] for p in places]
    selected_name = st.selectbox("Select place to edit", [""] + place_names)
    selected_place = next((p for p in places if p["name"] == selected_name), None)

    if selected_place:   
        st.write(f"Expecting delete: {selected_name}")
        id = selected_place["id"]

        if selected_place:
            if st.button("Delete Place"):
                delete_place(id)
                st.success(f"{selected_name} deleted!")
        else:
            st.info("Change at least one field to enable the button.")

    else:
        st.warning("Please select a valid place to delete.")
     