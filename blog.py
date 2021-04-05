# Stage 1. Create dictionaries
from sys import argv
import sqlite3

conn = sqlite3.connect(argv[1])
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

# Dictionaries for queries and data
dict_queries = {}
data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

# Strings to create tables
dict_queries['meals'] = "CREATE TABLE IF NOT EXISTS meals(" \
        "meal_id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "meal_name TEXT NOT NULL UNIQUE);"

dict_queries['ingredients'] = "CREATE TABLE IF NOT EXISTS ingredients(" \
              "ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT," \
              "ingredient_name TEXT NOT NULL UNIQUE);"

dict_queries['measures'] = "CREATE TABLE IF NOT EXISTS measures(" \
           "measure_id INTEGER PRIMARY KEY AUTOINCREMENT," \
           "measure_name TEXT UNIQUE);"

dict_queries['recipes'] = "CREATE TABLE IF NOT EXISTS recipes(" \
                          "recipe_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                          "recipe_name TEXT NOT NULL," \
                          "recipe_description TEXT);"

dict_queries['serve'] = "CREATE TABLE IF NOT EXISTS serve(" \
                        "serve_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                        "meal_id INTEGER NOT NULL," \
                        "recipe_id INTEGER NOT NULL," \
                        "FOREIGN KEY (meal_id) REFERENCES meals(meal_id)," \
                        "FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id));"

for key, value in dict_queries.items():
    cur.execute(dict_queries[key])

for key_data, value_data in data.items():
    for values in value_data:
        cur.execute(f"INSERT INTO {key_data} VALUES (?, ?);", (None, values))

conn.commit()
print("Pass the empty recipe name to exit.")

while True:
    rec_name = input("Recipe name: ")
    if rec_name == "":
        break
    rec_desc = input("Recipe description: ")
    cur.execute(f"INSERT INTO recipes VALUES (?, ?, ?);", (None, rec_name, rec_desc))
    rec_result = cur.execute(f"SELECT recipe_id FROM recipes").lastrowid
    served = list(input("When the dish can be served: ").split())
    for _i in served:
        cur.execute(f"INSERT INTO serve VALUES (?, ?, ?);", (None, _i, rec_result))
conn.commit()
conn.close()

