# Stage 4. Adding ingredients
from sys import argv
import sqlite3
import argparse

# Arguments to look for recipes
parser = argparse.ArgumentParser(description="Ingredients and meals")
parser.add_argument("database")
parser.add_argument("-i1", "--ingredients")
parser.add_argument("-i2", "--meals")
args = parser.parse_args()

conn = sqlite3.connect(args.database)
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

if not args.ingredients:
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
            cur.execute(f"INSERT OR IGNORE INTO {key_data} VALUES (?, ?);", (None, values))

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

            if len(ing) == 2:
                ing_new = ing[1]
                meas_new = ""
            else:
                ing_new = ing[2]
                meas_new = ing[1]

            mes_id = cur.execute(f"SELECT measure_id FROM measures WHERE measure_name=?", (meas_new,))
            mes_id_value = mes_id.fetchone()
            if ing_new.startswith("black"):
                ing_new = "blackberry"
            if ing_new.startswith("blue"):
                ing_new = "blueberry"

            ing_id = cur.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient_name=?", (ing_new,))
            ing_id_value = ing_id.fetchone()

            if mes_id_value == None:
                print("The measure is not conclusive")
            elif ing_id_value == None:
                print("The ingredient is not conclusive")
            else:
                cur.execute(f"INSERT INTO quantity VALUES (?, ?, ?, ?, ?)", (None, ing[0], rec_result, mes_id_value[0], ing_id_value[0]))
                conn.commit()
else:
    ing_list_id = []
    mea_list_id = []
    no_rec = False
    # Look for recipes
    ing_list = args.ingredients.split(',')
    mea_list = args.meals.split(',')

    # To get ingredients id
    for ing_it in ing_list:
        print(ing_it)
        rec_ing = cur.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient_name='{ing_it}'")
        ingrediente = rec_ing.fetchone()
        if not ingrediente:
            no_rec = True
        else:
            ing_list_id.append(ingrediente[0])

    # To get meals id
    for mea_it in mea_list:
        rec_mea = cur.execute(f"SELECT meal_id FROM meals WHERE meal_name='{mea_it}'")
        mea_list_id.append(rec_mea.fetchone()[0])

    recipes_id = []
    for mea_it in mea_list_id:
        for ing_it in ing_list_id:
            query_recipe_id = cur.execute(f"SELECT DISTINCT recipe_id FROM quantity WHERE recipe_id IN (SELECT recipe_id FROM serve WHERE meal_id = {mea_it}) AND ingredient_id = {ing_it};")

            for row in query_recipe_id.fetchall():
                recipes_id.append(row[0])

    print(recipes_id)
    set_recipes = set([id for id in recipes_id if recipes_id.count(id) > 1])
    if not set_recipes:
        set_recipes = set(recipes_id)
    print(set_recipes)
    recipes_names = []
    for _i in set_recipes:
        recipes_final = cur.execute(f"SELECT recipe_name FROM recipes WHERE recipe_id={_i}")
        recipes_names.append(recipes_final.fetchone()[0])

    if not no_rec:
        print(f"Recipes selected for you: {recipes_names}")
    else:
        print("There are no such recipes in the database.")


conn.commit()
conn.close()

