import sqlite3

def create_connection():
    """Create a database connection."""
    try:
        conn = sqlite3.connect('carbon_footprint.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error creating database connection: {e}")
        return None

def create_table(conn):
    """Create the user_data table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            country TEXT,
            distance REAL,
            electricity REAL,
            waste REAL,
            meals INTEGER,
            water REAL,
            transportation REAL,
            electricity_emission REAL,
            diet_emission REAL,
            waste_emission REAL,
            water_emission REAL,
            total_emission REAL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'user_data' created or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_user_data(conn, user_data):
    """Insert a record into the user_data table."""
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO user_data (
            name, age, gender, country, distance, electricity, waste, meals, water, transportation, 
            electricity_emission, diet_emission, waste_emission, water_emission, total_emission
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, user_data)
        conn.commit()
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

def check_table_exists(conn):
    """Check if the user_data table exists."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data';")
    table_exists = cursor.fetchone()
    if not table_exists:
        print("Table 'user_data' does not exist. Creating table...")
        create_table(conn)

if __name__ == '__main__':
    # Establish database connection
    conn = create_connection()
    if conn is None:
        print("Unable to connect to the database.")
    else:
        # Check if table exists and create it if not
        check_table_exists(conn)

        # Example user data to insert (you can replace this with real data)
        user_data = ('John Doe', 30, 'Male', 'USA', 100.0, 250.0, 50.0, 3, 100.0, 200.0, 120.0, 50.0, 30.0, 10.0, 560.0)

        # Insert the user data into the database
        insert_user_data(conn, user_data)

        # Close the connection
        conn.close()
