import sqlite3
import random
import os

#DB_NAME = r"C:\Users\tobru\Documents\GitHub\Programming Project\kategorien.db"
#DB_NAME= r"C:\Users\Ritus\wellbeing\data\wellbeing.db" 
base_dir = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(base_dir, "wellbeing.db")
print(f"DEBUG: Database path set to: {DB_NAME}") 

#database setup
def init_db():
    print(f"DEBUG: Initializing database...") 
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
    
    #add mushroom fields 
    add_mushroom_fields(conn)
    add_flower_fields(conn)
    
    c.execute("SELECT count(*) FROM good_habit_icons")
    if c.fetchone()[0] == 0:
        _populate_icons(conn)
        print("DEBUG: Icons populated.")
        
    
    c.execute("SELECT count(*) FROM habits")
    if c.fetchone()[0] == 0:
        _populate_defaults(conn)
        print("DEBUG: Default habits populated.")
        
    conn.close()
    print(f"DEBUG: Database initialization complete.")  

def add_mushroom_fields(conn):
    """Add mushroom tracking fields to database"""
    c = conn.cursor()
    
    #add mushroom_active column to habits table (1 = active, 0 = removed)
    try:
        c.execute("ALTER TABLE habits ADD COLUMN mushroom_active INTEGER DEFAULT 1")
        print("DEBUG: Added mushroom_active column")
    except sqlite3.OperationalError:
        print("DEBUG: mushroom_active column already exists")
    
    #add mushroom_position column (x, y coordinates on tree)
    try:
        c.execute("ALTER TABLE habits ADD COLUMN mushroom_position TEXT DEFAULT '0,0'")
        print("DEBUG: Added mushroom_position column")
    except sqlite3.OperationalError:
        print("DEBUG: mushroom_position column already exists")

    #add last_checked column for daily reset
    try:
        c.execute("ALTER TABLE habits ADD COLUMN last_checked DATE DEFAULT NULL")
        print("DEBUG: Added last_checked column")
    except sqlite3.OperationalError:
        print("DEBUG: last_checked column already exists")
    
    conn.commit()

def add_flower_fields(conn):
    """Add flower tracking fields to database"""
    c = conn.cursor()
    
    # add flower_active column (0 = not grown, 1 = grown)
    try:
        c.execute("ALTER TABLE habits ADD COLUMN flower_active INTEGER DEFAULT 0")
        print("DEBUG: Added flower_active column")
    except sqlite3.OperationalError:
        print("DEBUG: flower_active column already exists")
    
    conn.commit()

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
    print("DEBUG: Habit icons added.")
    
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
    print("DEBUG: Default habits added.")

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
    print(f"DEBUG: Getting habits of type: {habit_type}")  
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM habits WHERE habit_type = ?", (habit_type,))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    print(f"DEBUG: Found {len(rows)} habits of type {habit_type}") 
    return rows

def get_habits_and_icons(habit_type):
    print(f"DEBUG: Getting habits with icons for type: {habit_type}") 
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    query = """
        SELECT 
            h.id, 
            h.name, 
            h.habit_type, 
            COALESCE(f.flower, m.mushroom) AS display_name,
            COALESCE(f.img_file, m.img_file) AS file_name,
            h.mushroom_active
        FROM habits h
        LEFT JOIN good_habit_icons f ON h.icon_id = f.id AND h.habit_type = 'Good'
        LEFT JOIN bad_habit_icons m ON h.icon_id = m.id AND h.habit_type = 'Bad'
        WHERE h.habit_type = ?
    """
    c.execute(query, (habit_type,))
    
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    print(f"DEBUG: Found {len(rows)} habits with icons")  
    return rows

def add_habit(name, habit_type):
    print(f"DEBUG: Adding habit - Name: '{name}', Type: '{habit_type}'")  
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    
    if habit_type == "Bad":
        c.execute("SELECT COUNT(*) FROM habits WHERE habit_type = 'Bad'")
        bad_count = c.fetchone()[0]
        
        if bad_count >= 5:
            conn.close()
            raise Exception("Maximum 5 bad habits allowed (5 mushrooms max)! Delete an existing bad habit first.")
    
    random_icon_id = random.randint(1,5)
    print(f"DEBUG: Random icon ID: {random_icon_id}")  
    
    try:
        c.execute("INSERT INTO habits (name, habit_type, icon_id) VALUES (?, ?, ?)", (name, habit_type, random_icon_id))
        conn.commit()
        print(f"DEBUG: Habit '{name}' added successfully with ID {c.lastrowid}")  
    except Exception as e:
        print(f"ERROR adding habit: {e}")  
        raise e
    finally:
        conn.close()

def delete_habit(habit_id):
    """Deletes habit and its history."""
    print(f"DEBUG: Deleting habit ID: {habit_id}")  
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM habit_logs WHERE habit_id = ?", (habit_id,))
    c.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()
    print(f"DEBUG: Habit ID {habit_id} deleted")  
    
def update_habit_name(habit_id, new_name):
    print(f"DEBUG: Updating habit ID {habit_id} to name: '{new_name}'")  
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE habits SET name = ? WHERE id = ?", (new_name, habit_id))
    conn.commit()
    conn.close()
    print(f"DEBUG: Habit updated")  


def update_mushroom_status(habit_id, active):
    """Update mushroom active status (1 = active, 0 = removed)"""
    print(f"DEBUG: Updating mushroom status for habit {habit_id} to active={active}")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE habits SET mushroom_active = ? WHERE id = ?", (1 if active else 0, habit_id))
    conn.commit()
    conn.close()

def update_flower_status(habit_id, active):
    """Update flower active status (1 = grown, 0 = not grown)"""
    print(f"DEBUG: Updating flower status for habit {habit_id} to active={active}")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE habits SET flower_active = ? WHERE id = ?",
        (1 if active else 0, habit_id)
    )
    conn.commit()
    conn.close()


def get_active_flower_count():
    """Get count of grown flowers (good habits)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM habits WHERE habit_type = 'Good' AND flower_active = 1"
    )
    count = c.fetchone()[0]
    conn.close()
    return count

def get_active_mushroom_count():
    """Get count of active mushrooms (bad habits)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM habits WHERE habit_type = 'Bad' AND mushroom_active = 1")
    count = c.fetchone()[0]
    conn.close()
    return count

def reset_all_mushrooms():
    """Reset all mushrooms to active (for daily reset)"""
    print(f"DEBUG: Resetting all mushrooms to active")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE habits SET mushroom_active = 1 WHERE habit_type = 'Bad'")
    conn.commit()
    conn.close()

def reset_all_flowers():
    """Reset all flowers (for daily reset)"""
    print("DEBUG: Resetting all flowers")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE habits SET flower_active = 0 WHERE habit_type = 'Good'"
    )
    conn.commit()
    conn.close()

def get_bad_habits_with_mushrooms():
    """Get bad habits with mushroom status (MAX 5)"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    query = """
        SELECT 
            h.id, 
            h.name, 
            h.habit_type, 
            m.mushroom AS display_name,
            m.img_file AS file_name,
            h.mushroom_active
        FROM habits h
        LEFT JOIN bad_habit_icons m ON h.icon_id = m.id
        WHERE h.habit_type = 'Bad'
        ORDER BY h.id  -- Get oldest 5 habits
        LIMIT 5
    """
    c.execute(query)
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def get_good_habits_with_flowers():
    """Get good habits with flower status (MAX 5)"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = """
        SELECT 
            h.id,
            h.name,
            h.habit_type,
            f.flower AS display_name,
            f.img_file AS file_name,
            h.flower_active
        FROM habits h
        LEFT JOIN good_habit_icons f ON h.icon_id = f.id
        WHERE h.habit_type = 'Good'
        ORDER BY h.id
        LIMIT 5
    """
    c.execute(query)
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def get_bad_habit_count():
    """Get count of bad habits"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM habits WHERE habit_type = 'Bad'")
    count = c.fetchone()[0]
    conn.close()
    return count