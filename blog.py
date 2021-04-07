# Stage 4. Adding ingredients
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

dict_queries['quantity'] = "CREATE TABLE IF NOT EXISTS quantity(" \
                           "quantity_id INTEGER PRIMARY KEY AUTOINCREMENT," \
                           "quantity INTEGER NOT NULL," \
                           "recipe_id INTEGER NOT NULL," \
                           "measure_id INTEGER NOT NULL," \
                           "ingredient_id INTEGER NOT NULL," \
                           "FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)," \
                           "FOREIGN KEY (measure_id) REFERENCES measures(measure_id)," \
                           "FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id));"

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
    conn.commit()
    rec_result = cur.execute(f"SELECT recipe_id FROM recipes").lastrowid
    served = list(input("When the dish can be served: ").split())
    for _i in served:
        cur.execute(f"INSERT INTO serve VALUES (?, ?, ?);", (None, _i, rec_result))
        conn.commit()

    while True:
        ing = list(input("Input quantity of ingredient <press enter to stop>: ").split())
        if ing == []:
            break
        else:
            mes_id = cur.execute(f"SELECT measure_id FROM measures WHERE measure_name=?", (ing[1],))
            mes_id_value = mes_id.fetchone()
            if ing[2].startswith("black"):
                ing[2] = "blackberry"
            if ing[2].startswith("blue"):
                ing[2] = "blueberry"

            ing_id = cur.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient_name=?", (ing[2],))
            ing_id_value = ing_id.fetchone()

            print(mes_id_value[0])
            print(ing_id_value)
            if mes_id_value == None:
                print("The measure is not conclusive")
            elif ing_id_value == None:
                print("The ingredient is not conclusive")
            else:
                cur.execute(f"INSERT INTO quantity VALUES (?, ?, ?, ?, ?)", (None, ing[0], rec_result, mes_id_value[0], ing_id_value[0]))
                conn.commit()
conn.commit()
conn.close()

