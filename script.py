import requests
from bs4 import BeautifulSoup
import re
import locale
import json
from decimal import Decimal
import decimal

locale.setlocale(locale.LC_ALL, '')

graphics_cards = {
    "GeForce RTX 3060 Ti": "GeForce+RTX+fuer+Gaming/RTX+3060+Ti",
    # Add other graphics card entries here
}

url = "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table rows containing graphics card information
rows = soup.find_all("tr")

# Create a dictionary to store the cost per frame for each graphics card
cost_per_frame = {}

# Iterate over the rows, skipping the header row
for row in rows[1:]:
    # Find the columns in the row
    columns = row.find_all("td")

    # Extract the graphics card name and cost per frame
    name = columns[0].text.strip()
    cost = columns[2].text.strip().replace("$", "").replace(",", "")

    try:
        # Convert the cost to a Decimal object
        cost = Decimal(cost)
    except (decimal.InvalidOperation, TypeError):
        # Handle conversion errors by setting a default cost value
        cost = Decimal(0)

    # Check if the graphics card is in our dictionary
    if name in graphics_cards:
        # Add the graphics card and its cost per frame to the dictionary
        cost_per_frame[name] = cost

# Convert Decimal values to float before serializing
serialized_results = {card: float(cost) for card, cost in cost_per_frame.items()}

# Save results to JSON file
with open('results.json', 'w') as file:
    json.dump(serialized_results, file)
