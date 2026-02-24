#key : values
#JSON is a syntax for storing and exchanging data.
#JSON is text, written with JavaScript object notation
#Transfers data

import json  # Import the json module to work with JSON files
with open("sample-data.json", "r") as f: # Open the JSON file and load its contents into a Python dictionary
    data = json.load(f)  # Converts JSON data into a Python dictionary
print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':5}") # Print table column headers with fixed widths for alignment
print("-" * 80) # Print a separator line under the headers
for item in data["imdata"]: # Loop through each interface entry in the JSON data
    attrs = item["l1PhysIf"]["attributes"] # Access the attributes dictionary for each physical interface
    # Extract required fields from the attributes
    dn = attrs.get("dn", "")        # Distinguished Name of the interface
    descr = attrs.get("descr", "")  # Description (may be empty)
    speed = attrs.get("speed", "")  # Speed of the interface
    mtu = attrs.get("mtu", "")      # MTU value
    print(f"{dn:50} {descr:20} {speed:7} {mtu:5}")     # Print the extracted data in aligned columns