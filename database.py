import sqlite3
from sqlite3 import Error

#database = r"./database_file.db"

def connect_to_database(): # opens a connection ("a session") to the database
    try:
        conn = sqlite3.connect("database_file.db") # creates or opens database file.
        print("Connected to database")
        return conn # returns the connection (conn) so other functions can use it.
    except Error as err:
        print("Connection error: ", err)
        return None
    
def init_db(): # creates the table in the database if not already existing
    conn = sqlite3.connect('database_file.db') # 
    cursor = conn.cursor() # a pointer to the database - can use SQL queries
    # creates the table 
    # automatic ID - unique for every item
    # name on the item
    # how many items to buy
    # is the item "lined out" in the table - when the item is bought
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL,
                number INTEGER NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )        
   ''')
    
    conn.commit() # stores the changes in the database
    conn.close() # closes the database connection
    
def add_item(name, number): # adds a new item to the database
    conn = connect_to_database() # maintans a connection to SQLite-database.
    cursor = conn.cursor() # pointer to the database so SQL-qureries can be used.
    cursor.execute("INSERT INTO shopping_list (name, number, done) VALUES (?, ?, ?)", (name, number, False)) # sends the queries to the database. ? are placeholders instead of actual values. Safer.
    # questionmarks is replaced by the actual values - protection against sql-injection
    conn.commit() # save changes
    conn.close() # close connection
     
def get_items(): 
    conn = connect_to_database() # maintans a connection to SQLite-database.
    if conn: # if there is a connection...
        conn.row_factory = sqlite3.Row # row_factory - insted of tuples - used to have columnnames as keys (dictionary) row["name"] instead of row[1]
        cursor = conn.cursor() # creates a marker that can send SQL-queries to db. Cursor is the object used to send SQL-queries.
        cursor.execute("SELECT * FROM shopping_list") # runs the SQL-querie.
        rows = cursor.fetchall() # retrieves every row as result from the querie - like a list of rows.
        conn.close() # close connection.
        return [{"id": row[0], "name": row[1], "number": row[2], "done": bool(row[3])} for row in rows] # list comprehension to build a list of dictionaries. Each dict represents one item. SQL stores BOOLEAN as 0 or 1 (not True/False)
    return [] # returns an empty list in case connection to db failed - prevents application to crash.

def update_item_done(item_id, done):
    conn = connect_to_database() # maintans a connection to SQLite-database.
    if conn:
        cursor = conn.cursor() # talk with the database - a pointer to a location in database being worked with
        cursor.execute("UPDATE shopping_list SET done = ? WHERE id = ?", (done, item_id)) # sends the querie to the database
        conn.commit() # saves changes
        conn.close() # close connection
        
def delete_item(item_id):
    conn = connect_to_database() # maintans a connection to SQLite-database.
    if conn: # if there is a connection...
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shopping_list WHERE id = ?", (item_id,)) # ? = placeholder instead of placing values directly. 
        conn.commit() # save changes
        conn.close() # close connection
        
def update_number_of_items(item_id, number):
    conn = connect_to_database() # maintans a connection to SQLite-database.
    if conn: # if there is a connection...
        cursor = conn.cursor() # object used to send SQL-queries
        cursor.execute("UPDATE shopping_list SET number = ? WHERE id = ?", (number, item_id)) # the method used to run the queries
        conn.commit() # save changes
        conn.close() # close connection
        
def delete_all_items_in_list():
    conn = connect_to_database() # maintans a connection to SQLite-database.
    if conn: # if there is a connection...
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shopping_list")
        conn.commit() # save changes
        conn.close() # close connection
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# conn = er restauranten jeg går inn i
# cursor = servitøren som tar bestilligen - peker og kommuniserer med kjøkkenet
# cursor.execute(...) = meg som gir servitør bestilling