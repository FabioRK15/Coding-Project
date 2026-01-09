import flet as ft
import sqlite3
import random
import os

#DB_NAME = r"C:\Users\tobru\Documents\GitHub\Programming Project\kategorien.db"
#DB_NAME= r"C:\Users\Ritus\wellbeing\data\wellbeing.db" 
base_dir = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(base_dir, "wellbeing.db")


# SQLite DATABASE SETUP
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    #habits table
    sql_habits = "CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY, name TEXT NOT NULL, habit_type TEXT NOT NULL, icon_id INTEGER)" 
    c.execute(sql_habits)

    #habit logs
    sql_logs = "CREATE TABLE IF NOT EXISTS habit_logs (id INTEGER PRIMARY KEY, habit_id INTEGER, completed_at DATE, FOREIGN KEY(habit_id) REFERENCES habits(id))"
    c.execute(sql_logs)

    # good habit icons (flowers)
    sql_flowers = "CREATE TABLE IF NOT EXISTS good_habit_icons (id INTEGER PRIMARY KEY, flower TEXT NOT NULL, img_file TEXT NOT NULL)"
    c.execute(sql_flowers)

    # bad habit icons (mushrooms)
    sql_mushrooms = "CREATE TABLE IF NOT EXISTS bad_habit_icons (id INTEGER PRIMARY KEY, mushroom TEXT NOT NULL, img_file TEXT NOT NULL)"
    c.execute(sql_mushrooms)

    conn.commit()
    
    c.execute("SELECT count(*) FROM good_habit_icons")
    if c.fetchone()[0] == 0:
        _populate_icons(conn)
        print("Icons populated.")
        
    
    c.execute("SELECT count(*) FROM habits")
    if c.fetchone()[0] == 0:
        _populate_defaults(conn)
        print("Habits populated.")
        
    conn.close()

        

    
    
def _populate_icons(conn):
    flowers = [
        ("Rose", "flower_1"), 
        ("Sunflower", "flower_2"), 
        ("Tulip", "flower_3"), 
        ("Daisy", "flower_4"), 
        ("Lavender", "flower_5")
    ]
    mushrooms = [
        ("Fly Agaric", "mushroom_1"), 
        ("Death Cap", "mushroom_2"), 
        ("Destroying Angel", "mushroom_3"), 
        ("Webcap", "mushroom_4"), 
        ("False Morel", "mushroom_5")
    ]
    
    c = conn.cursor()
    c.executemany("INSERT INTO good_habit_icons (flower, img_file) VALUES (?, ?)", flowers)
    c.executemany("INSERT INTO bad_habit_icons (mushroom, img_file) VALUES (?, ?)", mushrooms)
    conn.commit()
    print("Habit icons added.")
    
def _populate_defaults(conn):
    defaults = [
        ("Gym", "Good", 1),
        ("Meditation", "Good", 2),
        ("Drink Water", "Good", 3),
        ("Smoking", "Bad", 1),
        ("Social Media", "Bad", 2),
        ("Sugar", "Bad", 3)
    ]
    c = conn.cursor()
    c.executemany("INSERT INTO habits (name, habit_type, icon_id) VALUES (?, ?, ?)", defaults)
    conn.commit()
    print("Defaults added.")



def get_flowers():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM good_habit_icons")
    rows = c.fetchall()
    conn.close()
    return rows

def get_mushrooms():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM bad_habit_icons")
    rows = c.fetchall()
    conn.close()
    return rows
    
# -----------------------------------------------------------------------------    
    
#functions: list habits, add new, delete habit, and edit habit name
def get_habits_by_type(habit_type):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM habits WHERE habit_type = ?", (habit_type,))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def get_habits_and_icons(habit_type):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    query = """
        SELECT 
            h.id, 
            h.name, 
            h.habit_type, 
            COALESCE(f.flower, m.mushroom) AS display_name,
            COALESCE(f.img_file, m.img_file) AS file_name
        FROM habits h
        LEFT JOIN good_habit_icons f ON h.icon_id = f.id AND h.habit_type = 'Good'
        LEFT JOIN bad_habit_icons m ON h.icon_id = m.id AND h.habit_type = 'Bad'
        WHERE h.habit_type = ?
    """
    c.execute(query, (habit_type,))
    
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows


def add_habit(name, habit_type):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    random_icon_id = random.randint(1,5)
    
    c.execute("INSERT INTO habits (name, habit_type, icon_id) VALUES (?, ?, ?)", (name, habit_type, random_icon_id))
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
    


