# Stage 1. Create dictionaries
from sys import argv
import sqlite3

conn = sqlite3.connect(argv[1])
cur = conn.cursor()

# Dictionaries for queries and data
dict_queries = {}
data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

# Strings to create tables
dict_queries['meals'] = "CREATE TABLE meals(" \
        "meal_id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "meal_name TEXT NOT NULL UNIQUE);"

dict_queries['ingredients'] = "CREATE TABLE ingredients(" \
              "ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT," \
              "ingredient_name TEXT NOT NULL UNIQUE);"

dict_queries['measures'] = "CREATE TABLE measures(" \
           "measure_id INTEGER PRIMARY KEY AUTOINCREMENT," \
           "measure_name TEXT UNIQUE);"

for key, value in dict_queries.items():
    cur.execute(dict_queries[key])

for key_data, value_data in data.items():
    for values in value_data:
        cur.execute(f"INSERT INTO {key_data} VALUES (?, ?);", (None, values))


conn.commit()

conn.close()

