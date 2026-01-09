import flet as ft
import sqlite3

DB_NAME = r"C:\Users\tobru\Documents\GitHub\Programming Project\kategorien.db"

# ------------------------------------------------------
# SQLite SETUP
# ------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Kategorien
    c.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Tabellenzeilen
    c.execute("""
        CREATE TABLE IF NOT EXISTS table_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            checked INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def load_categories():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name FROM categories ORDER BY name")
    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return rows

def load_table_entries():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, category, checked FROM table_entries")
    rows = c.fetchall()
    conn.close()
    return rows

def add_category_to_db(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Kategorie existiert schon
    conn.close()

def add_table_entry(category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO table_entries (category, checked) VALUES (?, 0)", (category,))
    conn.commit()
    conn.close()

def update_checkbox_state(entry_id, state):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE table_entries SET checked = ? WHERE id = ?", (1 if state else 0, entry_id))
    conn.commit()
    conn.close()

# ------------------------------------------------------
# FLET APP
# ------------------------------------------------------
def main(page: ft.Page):
    page.title = "Tabelle + Kategorien + Checkbox + SQLite"
    init_db()

    # -----------------------------
    # Dropdown Kategorien
    # -----------------------------
    categories = load_categories()
    category_dropdown = ft.Dropdown(
        label="Kategorie wählen",
        options=[ft.dropdown.Option(cat) for cat in categories],
        width=300
    )

    # Eigene Kategorie
    custom_category = ft.TextField(label="Eigene Kategorie", width=300)

    # -----------------------------
    # Tabelle aufbauen
    # -----------------------------
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Kategorie")),
            ft.DataColumn(ft.Text("✓")),
        ],
        rows=[]
    )

    # -----------------------------
    # Checkbox-Aktualisierungsfunktion
    # -----------------------------
    def checkbox_changed(e, entry_id):
        update_checkbox_state(entry_id, e.control.value)

    # -----------------------------
    # Tabelle aus DB laden
    # -----------------------------
    def load_table():
        table.rows.clear()
        for entry_id, category, checked in load_table_entries():
            chk = ft.Checkbox(value=bool(checked))
            chk.on_change = lambda e, row_id=entry_id: checkbox_changed(e, row_id)

            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(category)),
                        ft.DataCell(chk),
                    ]
                )
            )
        page.update()

    load_table()

    # -----------------------------
    # Eintrag hinzufügen
    # -----------------------------
    def add_row(e):
        # Kategorie bestimmen
        if custom_category.value.strip():
            category = custom_category.value.strip()
            add_category_to_db(category)

            # Dropdown neu laden
            cats = load_categories()
            category_dropdown.options = [ft.dropdown.Option(c) for c in cats]

        else:
            category = category_dropdown.value

        if not category:
            return

        # In DB speichern
        add_table_entry(category)

        # Tabelle neu laden
        load_table()

        # Eingabefelder leeren
        custom_category.value = ""
        page.update()

    # -----------------------------
    # Layout
    # -----------------------------
    page.add(
        ft.Text("Kategorieverwaltung", size=22, weight="bold"),
        category_dropdown,
        custom_category,
        ft.ElevatedButton("Zur Tabelle hinzufügen", on_click=add_row),
        ft.Divider(),
        table
    )

ft.app(target=main)

#this is a test and I want to try things