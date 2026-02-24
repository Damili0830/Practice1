#key : values
#JSON is a syntax for storing and exchanging data.
#JSON is text, written with JavaScript object notation

import json  # Import the json module to work with JSON files

# Open the JSON file and load its contents into a Python dictionary
with open("sample-data.json", "r") as f:
    data = json.load(f)  # Converts JSON data into a Python dictionary

# Print the table title
print("Interface Status")

# Print a separator line
print("=" * 80)

# Print table column headers with fixed widths for alignment
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':5}")

# Print a separator line under the headers
print("-" * 80)

# Loop through each interface entry in the JSON data
for item in data["imdata"]:

    # Access the attributes dictionary for each physical interface
    attrs = item["l1PhysIf"]["attributes"]

    # Extract required fields from the attributes
    dn = attrs.get("dn", "")        # Distinguished Name of the interface
    descr = attrs.get("descr", "")  # Description (may be empty)
    speed = attrs.get("speed", "")  # Speed of the interface
    mtu = attrs.get("mtu", "")      # MTU value

    # Print the extracted data in aligned columns
    print(f"{dn:50} {descr:20} {speed:7} {mtu:5}")