Inventory Management API Documentation:

This API provides functionalities to manage an inventory system for electronic 
parts. It allows users to add, retrieve, update, and delete parts. Users can also 
check quantities and search for parts based on specific characteristics.

Please download the requirements in requirements.txt before running main.py and test.py

1. Adding a Part
Method: PUT

Endpoint: /part/

Request Parameters:

sku (int, required): Stock Keeping Unit, the part's unique id

class_name (str, required): Class of part. Valid values are 'resistor', 'solder', 'wire', 'display_cable', and 'ethernet_cable'.

quantity (int, required): Quantity of the part.

Additional parameters depend on the type of part being added.

Examples:

# Adding a resistor
import requests
url = 'http://127.0.0.1:5000/part/'     # 'http://127.0.0.1:5000' can be replaced by your specific API's url
data = {
    "sku": 12345,
    "class_name": "resistor",
    "quantity": 100,
    "resistance": 100,    # Specific to resistors
    "tolerance": 5        # Specific to resistors
}
response = requests.put(url, json=data)
print(response.status_code)  # Expected: 201

# Adding a solder
data = {
    "sku": 54321,
    "class_name": "solder",
    "quantity": 50,
    "solder_type": "lead",       # Specific to solders
    "solder_length": 1.5         # Specific to solders
}
response = requests.put(url, json=data)
print(response.status_code)  # Expected: 201


2. Getting a Part
Method: GET

Endpoint: /part/<int:sku>

Path Parameter:

sku (int, required): Stock Keeping Unit of the part.

Example:

import requests
url = 'http://127.0.0.1:5000/part/12345'
response = requests.get(url)
print(response.status_code)  # Expected: 200
print(response.json())        # Returns details of the part with SKU 12345


3. Deleting a Part
Method: DELETE

Endpoint: /part/<int:sku>

Path Parameter:

sku (int, required): Stock Keeping Unit of the part to be deleted.

Example:

import requests
url = 'http://127.0.0.1:5000/part/12345'
response = requests.delete(url)
print(response.status_code)  # Expected: 204 (No Content)


4. Getting Quantity of a Part
Method: GET

Endpoint: /quantity/<int:sku>

Path Parameter:

sku (int, required): Stock Keeping Unit of the part.

Example:

import requests
url = 'http://127.0.0.1:5000/quantity/12345'
response = requests.get(url)
print(response.status_code)  # Expected: 200
print(response.json())        # Returns {"sku": 12345, "quantity": <quantity>}


5. Updating Quantity of a Part
Method: PATCH

Endpoint: /inventory/

Request Parameters:

sku (int, required): Stock Keeping Unit of the part.
quantity (int, required): New quantity of the part.

Example:

import requests
url = 'http://127.0.0.1:5000/inventory/'
data = {
    "sku": 12345,
    "quantity": 150  # New quantity
}
response = requests.patch(url, json=data)
print(response.status_code)  # Expected: 200


6. Getting Inventory
Method: GET

Endpoint: /inventory/

Example:

import requests
url = 'http://127.0.0.1:5000/inventory/'
response = requests.get(url)
print(response.status_code)  # Expected: 200
print(response.json())        # Returns details of all parts in inventory


7. Searching for Parts
Method: GET

Endpoint: /search/

Request Parameters:

Parameters depend on the type of part being searched for.

Example:

import requests
url = 'http://127.0.0.1:5000/search/'
params = {
    "class_name": "resistor",
    "resistance": 100,    # Specific to resistor
    "tolerance": 5        # Specific to resistor
}
response = requests.get(url, params=params)
print(response.status_code)  # Expected: 200
print(response.json())        # Returns list of resistors with resistance 100 and tolerance 5



Overall Design:

This API is a REST API designed using Flask and Flask-RESTful for creating RESTful endpoints. 
I chose to create a REST API because REST APIs are quite lightweight and commonly used,
so there is lots of documentation on how to create one. 

Regarding the tools and libraries used to create this API, Flask-RESTful allows for easy error handling 
through the use of its abort statement. SQLAlchemy is used for database management.
Each type of part is modeled as a subclass of a common PartModel, enabling polymorphic behavior and 
efficient querying. Request parsing is done using reqparse to ensure valid input data. Responses are 
formatted using fields and marshal to maintain consistency. The API has a modular design 
with separate resources for different operations. This makes the code simpler to read, thus
making it more maintainable. 
