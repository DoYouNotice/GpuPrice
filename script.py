import requests
from bs4 import BeautifulSoup
import re
import locale
import json
from decimal import Decimal


locale.setlocale(locale.LC_ALL, '')

graphics_cards = {
    "GeForce RTX 3060 Ti": "GeForce+RTX+fuer+Gaming/RTX+3060+Ti",
    "GeForce RTX 4090": "GeForce+RTX+fuer+Gaming/RTX+4090",
    "Radeon RX 7900 XTX": "Radeon+RX+Serie/RX+7900+XTX",
    "GeForce RTX 4080": "GeForce+RTX+fuer+Gaming/RTX+4080",
    "Radeon RX 7900 XT": "Radeon+RX+Serie/RX+7900+XT",
    "Radeon RX 6950 XT": "Radeon+RX+Serie/RX+6950+XT",
    "GeForce RTX 4070 Ti": "GeForce+RTX+fuer+Gaming/RTX+4070+Ti",
    "GeForce RTX 3090 Ti": "GeForce+RTX+fuer+Gaming/RTX+3090+Ti",
    "Radeon RX 6900 XT": "Radeon+RX+Serie/RX+6900+XT",
    "GeForce RTX 3090": "GeForce+RTX+fuer+Gaming/RTX+3090",
    "Radeon RX 6800 XT": "Radeon+RX+Serie/RX+6800+XT",
    "GeForce RTX 3080 Ti": "GeForce+RTX+fuer+Gaming/RTX+3080+Ti",
    "GeForce RTX 3080 12GB": "GeForce+RTX+fuer+Gaming/RTX+3080+12GB",
    "GeForce RTX 4070": "GeForce+RTX+fuer+Gaming/RTX+4070",
    "GeForce RTX 3080": "GeForce+RTX+fuer+Gaming/RTX+3080",
    "Radeon RX 6800": "Radeon+RX+Serie/RX+6800",
    "GeForce RTX 3070 Ti": "GeForce+RTX+fuer+Gaming/RTX+3070+Ti",
    "Radeon RX 6750 XT": "Radeon+RX+Serie/RX+6750+XT",
    "Radeon RX 6700 XT": "Radeon+RX+Serie/RX+6700+XT",
    "GeForce RTX 3060": "GeForce+RTX+fuer+Gaming/RTX+3060",
    "Radeon RX 6600 XT": "Radeon+RX+Serie/RX+6600+XT",
    "Radeon RX 6500 XT": "Radeon+RX+Serie/RX+6500+XT",
    "Radeon RX 7600": "Radeon+RX+Serie/RX+7600",
    "GeForce RTX 4060 Ti": "GeForce+RTX+fuer+Gaming/RTX+4060+TI",
    "Radeon RX 6650 XT": "Radeon+RX+Serie/RX+6650+XT",    
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

    # Convert the cost to a Decimal object
    cost = Decimal(cost)

    # Check if the graphics card is in our dictionary
    if name in graphics_cards:
        # Add the graphics card and its cost per frame to the dictionary
        cost_per_frame[name] = cost

# Convert Decimal values to float before serializing
serialized_results = {card: float(cost) for card, cost in cost_per_frame.items()}

# Save results to JSON file
with open('results.json', 'w') as file:
    json.dump(serialized_results, file)
