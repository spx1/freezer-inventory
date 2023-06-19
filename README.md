# freezer-inventory
Track the items in my freezer

# Setup and Startup Instructions
1. Clone the environment
    1. git clone https://github.com/spx1/freezer-inventory.git
1. Create a virtual environment
    1. mkdir venv
    1. python -m venv venv
1. Install requirements
    1. source venv/bin/activate
    1. pip install -r requirements.txt
1. Create the database, database user, and grant privileges to the database
    1. CREATE DATABASE FREEZER;
    1. CREATE USER 'app'@'localhost' IDENTIFIED BY 'a secret password';
    1. GRANT ALL PRIVILEGES ON FREEZER.* TO 'app'@'loclahost';
    1. FLUSH PRIVILEGES;
    1. QUIT
1. Create the tables use alembic
    1. source venv/bin/activate
    1. alembic upgrade head
1. Startup the application
    1. source venv/bin/activate
    1. extern FLASK_APP="wsgi.py"
    1. flask run --host=0.0.0.0 --port=5000

# Startup Script
It is recommended to create a startup script to load all the envrionmental variables required to
connect to the database. This script should also start the application. General flow for the startup script is

1. Export environmental variables
1. Run the flask application