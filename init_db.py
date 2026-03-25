import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("database.db")

# Create a cursor object
cursor = connection.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Create patients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    diagnosis TEXT,
    treatment TEXT
)
""")

print("Database and users table created successfully.")

connection.commit()
connection.close()