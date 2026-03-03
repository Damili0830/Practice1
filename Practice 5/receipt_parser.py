import re
import json

# Read receipt text from file
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Regex pattern to extract:
# - product number
# - product name
# - quantity
# - unit price
# - total price per item
item_pattern = re.compile(
    r"\d+\.\n"                          # item number (e.g. 1.)
    r"(.+?)\n"                          # product name
    r"([\d,]+)\s*x\s*([\d ]+,\d{2})\n"  # quantity x unit price
    r"([\d ]+,\d{2})",                  # total price
    re.MULTILINE
)

items = []
calculated_total = 0

# Loop through all found items
for name, qty, unit_price, total_price in item_pattern.findall(text):

    # Convert quantity to float
    quantity = float(qty.replace(",", "."))

    # Convert prices to float (remove spaces, replace comma with dot)
    unit_price = float(unit_price.replace(" ", "").replace(",", "."))
    total_price = float(total_price.replace(" ", "").replace(",", "."))

    # Add item total price to calculated total
    calculated_total += total_price

    # Store item data
    items.append({
        "product": name.strip(),
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price
    })

# Extract TOTAL from receipt
total_match = re.search(r"ИТОГО:\n([\d ]+,\d{2})", text)
receipt_total = (
    float(total_match.group(1).replace(" ", "").replace(",", "."))
    if total_match else None
)

# Extract date and time
datetime_match = re.search(
    r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text
)
date_time = datetime_match.group() if datetime_match else None

# Final structured result
result = {
    "date_time": date_time,
    "items": items,
    "calculated_total": round(calculated_total, 2),
    "receipt_total": receipt_total
}

# Print result in readable JSON format
print(json.dumps(result, indent=4, ensure_ascii=False))