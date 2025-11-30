🌍 Trip Planner Project

📌 Project Description
    Trip Planner is a system for managing travel itineraries around the world.
    It allows users to:

🆕 Create new places
    Read and view existing places
    Update place details
    Delete places

Each place stores information such as:

Name
City
Country
Notes
Priority
Visited status
Data is stored in a JSON file by default, with future support for databases. The project also supports integration with a UI layer like Streamlit.


trip_planner_project/
│
├── src/                       # Source code
│   ├── controllers/           # CRUD logic
│   │   └── places_controller.py
│   ├── db/                    # Database connection (future)
│       └── db.py
│── tests/ 
│    ├──test_db_connection.py
│    │
│    ├──test_places_crud.py
│
├── data/                      # Data storage
│   └── places.json
│
├── ui/                        # User interface
│   └── streamlit_app.py
│
└── README.md


⚙️ Installation & Running

    Install Python 3.10 or higher.
    Install required packages (if using Streamlit):
    pip install -r requirements.txt
    
    To run the Streamlit UI:
    python -m streamlit run ui/streamlit_app.py

🐋 Run using Docker compose
    
    docker-compose up -d

🐋 End running 
    
    docker-compose down

🧪 run Docker tests:

    docker-compose run --rm tests

    