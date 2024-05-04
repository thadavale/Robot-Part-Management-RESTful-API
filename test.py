import requests

# Code for testing the API's methods and error handling
# Feel free to change arguments as desired to check code functionality!


BASE = "http://127.0.0.1:5000/"

resistorObj = {"sku": 1, "class_name": "resistor", "quantity": 8, "resistance": 3, "tolerance": 5}

resistorObj2 = {"sku": 2, "class_name": "resistor", "quantity": 6, "resistance": 3, "tolerance": 7}

solderObj = {"sku": 3, "class_name": "solder", "quantity": 3, "solder_type": 'lead', "solder_length": 2.2}

wireObj = {"sku": 4, "class_name": "wire", "quantity": 2, "gauge": 1.5, "wire_length": 7}

displayObj = {"sku": 5, "class_name": "display_cable", "quantity": 9, "display_cable_type": "hdmi", "display_cable_length": 4.81, "display_cable_color": "#FFFFFF"}

ethernetObj = {"sku": 6, "class_name": "ethernet_cable", "quantity": 7, "alpha_type": "male", "beta_type": "female", "speed": "100mbps", "ethernet_cable_length": 6.562}

input()
response = requests.put(BASE + "part/", json=resistorObj)         # Adds all parts to the inventory
print(response.json())
print()
response = requests.put(BASE + "part/", json=resistorObj2)
print(response.json())
print()
response = requests.put(BASE + "part/", json=solderObj)
print(response.json())
print()
response = requests.put(BASE + "part/", json=wireObj)
print(response.json())
print()
response = requests.put(BASE + "part/", json=displayObj)
print(response.json())
print()
response = requests.put(BASE + "part/", json=ethernetObj)
print(response.json())

input()                                             # Gets the part with an SKU of 3
response = requests.get(BASE + "part/3")
print(response.json())
print()

input()
response = requests.delete(BASE + "part/4")         # Deletes the part with an SKU of 4
print(response.json())

input()
response = requests.get(BASE + "part/4")            # Tries to get the part with an SKU of 4, throws an error because it doesn't exist anymore
print(response.json())
print()

input()
response = requests.get(BASE + "quantity/3")        # Gets the quantity of the part with an SKU of 3
print(response.json())
print()

input()
response = requests.get(BASE + "inventory/")        # Gets the entire inventory
print(response.json())
print()

patchObj = {"sku": "5", "quantity": 20}

input()
response = requests.patch(BASE + "inventory/", json=patchObj)    # Changes the quantity of the part with an SKU of 5 to 20
print(response.json())
print()

input()
response = requests.get(BASE + "part/5")            # Gets the part with an SKU of 5
print(response.json())
print()

searchObj = {"class_name": "resistor", "resistance": 3, "tolerance": 7}

input()
response = requests.get(BASE + "search/", json=searchObj)       # Searches for and gets all resistors that either have a resistance of 3 or a tolerance of 7
print(response.json())
print()