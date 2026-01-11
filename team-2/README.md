# Self-management Toolkit
### By Team 2

### Team Members
* Ahmad Hassan
* Consti
* Fabio Kurz
* Rita Kerkovits
* Tobi

## 1. Project Overview
The Self-management Toolkit is a desktop/web application designed to support daily routines and mental well-being. It combines gamified habit tracking with accessible stress-relief tools.

The core interface features a dynamic "Habit Tree":
* Flowers: Represent positive habits (e.g., exercise, hydration).
* Mushrooms: Represent negative habits (e.g., smoking). Mushrooms disappear as bad habits are avoided.

## Key Features
### 1. Habit Tracking & Visualization
* Gamified Dashboard: Visualizes user progress as additional flowers or eliminated mushrooms
* Database: Uses SQLite to store predefined (Good/Bad) and custom user habits.
* Quick Logging: Simple checkbox interaction for daily logging
* Statistics: specific view for habit streaks, number of habits etc.

### 2. Breathing Studio
Guided Sessions: Integrated visual guide to assist users with timing and rhythm
Techniques Included:
* 4-7-8 Relaxation breathing
* Box (Focus) breathing
* Smooth balanced Breathing

## Tech Stack
* Language: Python 3.x
* UI Framework: Flet 
* Database: SQLite
* Assets: Local image assets for breathing exercises, and habit icons

## Project structure
```/
├── assets/              # Images for habits
├── database/            # SQLite connection and schema logic
├── pages/               # Flet UI pages (Dashboard, Habits, Breathing)
├── main.py              # Application entry point
└── README.md            # Project documentation
```

