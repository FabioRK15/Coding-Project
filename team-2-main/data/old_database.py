import flet as ft
import sqlite3

#DB_NAME = r"C:\Users\tobru\Documents\GitHub\Programming Project\kategorien.db"
DB_NAME= r"C:\Users\Ritus\wellbeing\data\wellbeing.db" 


# SQLite DATABASE SETUP
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    #habits table
    sql_habits = "CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY, name TEXT NOT NULL, habit_type TEXT NOT NULL)"
    c.execute(sql_habits)

    #habit logs
    sql_logs = "CREATE TABLE IF NOT EXISTS habit_logs (id INTEGER PRIMARY KEY, habit_id INTEGER, completed_at DATE, FOREIGN KEY(habit_id) REFERENCES habits(id))"
    c.execute(sql_logs)

    conn.commit()
    
    #check if table is empty, populate defaults
    try:
        c.execute("SELECT count(*) FROM habits")
        if c.fetchone()[0] == 0:
            _populate_defaults(conn)
    except sqlite3.OperationalError:
        pass
        
        
    conn.close()
    
def _populate_defaults(conn):
    defaults = [
        ("Gym", "Good"),
        ("Meditation", "Good"),
        ("Drink Water", "Good"),
        ("Smoking", "Bad"),
        ("Social Media", "Bad"),
        ("Sugar", "Bad")
    ]
    c = conn.cursor()
    c.executemany("INSERT INTO habits (name, habit_type) VALUES (?, ?)", defaults)
    conn.commit()
    print("Defaults added.")
    
# -----------------------------------------------------------------------------    
    
# CORE FUNCTIONS (READ, ADD, DELETE)
def get_habits_by_type(habit_type):
    """Returns simple list of dicts: [{'id': 1, 'name': 'Gym', 'habit_type': 'Good'}, ...]"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM habits WHERE habit_type = ?", (habit_type,))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows


def add_habit(name, habit_type):
    """Simple add: just name and type."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO habits (name, habit_type) VALUES (?, ?)", (name, habit_type))
    conn.commit()
    conn.close()

def delete_habit(habit_id):
    """Deletes habit and its history."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM habit_logs WHERE habit_id = ?", (habit_id,))
    c.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()
    
    
def update_habit_name(habit_id, new_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE habits SET name = ? WHERE id = ?", (new_name, habit_id))
    conn.commit()
    conn.close()
    


