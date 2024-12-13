import sqlite3

# def create_database():
#     connection = sqlite3.connect("cropsList.db")
#     cursor = connection.cursor()

#     # Create crops table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS crops (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         explanation TEXT,
#         trivia TEXT,
#         image_filename TEXT)''')

#     # Insert some sample data
#     crops = [
#         ("Rice", ".", ".", "rice.jpg"),
#         ("Maize", ".", ".", "maize.jpg"),
#         ("Chickpea", ".", ".", ".jpg"),
#         ("Kidneybeans", ".", ".", ".jpg"),
#         ("Pigeonbens", ".", ".", ".jpg"),
#         ("Mothbeans", ".", ".", ".jpg"),
#         ("Mungbeans", ".", ".", ".jpg"),
#         ("Blackgram", ".", ".", ".jpg"),
#         ("Lentil", ".", ".", ".jpg"),
#         ("Pomegranate", ".", ".", ".jpg"),
#         ("Banana", ".", ".", ".jpg"),
#         ("Mango", ".", ".", ".jpg"),
#         ("Grapes", ".", ".", ".jpg"),
#         ("Watermelon", ".", ".", ".jpg"),
#         ("Muskmelon", ".", ".", ".jpg"),
#         ("Apple", ".", ".", ".jpg"),
#         ("Orange", ".", ".", ".jpg"),
#         ("Papaya", ".", ".", ".jpg"),
#         ("Coconut", ".", ".", ".jpg"),
#         ("Cotton", ".", ".", ".jpg"),
#         ("Jute", ".", ".", ".jpg"),
#         ("Coffee", ".", ".", ".jpg"),

#     ]
#     cursor.executemany("INSERT INTO crops (name, explanation, trivia, image_filename) VALUES (?, ?, ?, ?)", crops)

#     connection.commit()
#     connection.close()

# # Create the database
# create_database()


def insert_new_crops():
    connection = sqlite3.connect("cropsList.db")
    cursor = connection.cursor()

    # New crop data to add
    new_crops = [
        ("Bitter Gourd", ".", ".", ".jpg"),
        ("Kangkong", ".", ".", ".jpg"),
        ("String Beans", ".", ".", ".jpg"),
        ("Pechay", ".", ".", ".jpg"),
        ("Okra", ".", ".", ".jpg"),
    ]

    # Insert the new crops into the crops table
    cursor.executemany("INSERT INTO crops (name, explanation, trivia, image_filename) VALUES (?, ?, ?, ?)", new_crops)

    connection.commit()

insert_new_crops()

    # new_crops = [
    #     ("Tomato", ".", ".", "tomato.jpg"),
    #     ("Potato", ".", ".", "potato.jpg"),
    #     ("Onion", ".", ".", "onion.jpg"),
    #     ("Carrot", ".", ".", "carrot.jpg"),
    #     ("Cucumber", ".", ".", "cucumber.jpg"),
    #     ("Lettuce", ".", ".", "lettuce.jpg"),
    #     ("Spinach", ".", ".", "spinach.jpg"),
    #     ("Peas", ".", ".", "peas.jpg"),
    #     ("Broccoli", ".", ".", "broccoli.jpg"),
    #     ("Cauliflower", ".", ".", "cauliflower.jpg")
    # ]