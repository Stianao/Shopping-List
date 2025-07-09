from flask import Flask, request, jsonify, render_template
from database import add_item, get_items, delete_item, update_item_done, update_number_of_items, delete_all_items_in_list
#from flask_cors import CORS

### jsonify converts Python-dictionary to JSON ###

app = Flask(__name__) # Start webserver and handle routes.

# Returns the homepage with the shopping list.
@app.route('/') # Flask route 
def index():
    return render_template('index.html')

# Retrieves entire shopping list from db and returning it as JSON
@app.route('/items', methods=['GET']) # GET /items
def fetch_items():
    items = get_items() # calling function from database_file.db
    return jsonify(items) # returns shopping list.

@app.route('/items', methods=['POST']) # Handle POST-queries to /items. Coresponds with frontend fetch() where method: 'POST'
def create_item():
    data = request.json # reading JSON-data from queries. Flask automatically turns it into a Python-directory
    name = data.get('name') # reading name-field from json-data
    number = data.get('number') # reading number-field from json-data
    if name and number: # check if both fields are sent in (not None or empty)
        add_item(name, number) # if valid - add item to db by calling add_item() function from database.db
        return jsonify({"message": "Item added"}), 201 # JSON-respons -> everything went fine. 201 HTTP-status Created.
    return jsonify({"error": "Missing name or number"}), 400 # JSON-respons -> something is missing, error and HTTP-status (Bad Request).

# Handle DELETE-querie to id-number x. 
@app.route('/item/<int:item_id>', methods=['DELETE']) # DELETE /item/x
def remove_item(item_id): # item_id: the ID to the item that will be deleted. 
    delete_item(item_id) # calling delete_item() function from database.py. SQL: DELETE FROM shopping_list WHERE ID = ?
    return jsonify({"message": "Item deleted"}) # returns a JSON-object to frontend. Confirms deletion.

@app.route('/items/<int:item_id>', methods=['PATCH']) # defines a HTTP PATCH-route in Flask. A querie for items/x, naming it for example 5.
# PATCH is used to update part of an object (done-status).
def mark_done(item_id): # the argument is the ID for the item to be updated in the database.
    data = request.json # reads JSON-data from sent by PATCH-querie from frontend: { "done": true }
    done = data.get('done') # retrieves the value from the key "done" from JSON-data.
    if done is not None: # checks if done is sent. False if valid. None if its not there.
        update_item_done(item_id, done) # calling function from database.py - updating the row with item_id and changes the collumn 'done' to True or False.
        return jsonify({"message": "Item updated"})
    return jsonify({"error": "Missing 'done' status"}), 400

@app.route('/items/<int:item_id>/number', methods=['PATCH']) # example: PATCH /items/7/number
# PATCH updates part of an object - the 'number'.
def update_number(item_id): # which item that will be updated in the database.
    data = request.json # reading JSON-data from request - { "number": 5 }
    number = data.get('number') # retrieves the value from the key "number" from JSON-data.
    if number is not None: # checks if 
        update_number_of_items(item_id, number) # calling function - SQL: UPDATE shopping_list SET number = ? WHERE id = ?.
        return jsonify({"message": "Item number updated"})
    return jsonify({"error": "Missing 'number'"}), 400

@app.route('/items', methods=['DELETE']) # 
def delete_shoppingList():
    delete_all_items_in_list()
    return jsonify({"message": "Shoppinglist deleted"})

if __name__ == "__main__":
    app.run(debug = True) # Errors will show on the webpage