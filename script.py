import requests
from bs4 import BeautifulSoup
import re
import locale
from decimal import Decimal
import json

# Set the appropriate locale for number formatting
locale.setlocale(locale.LC_ALL, '')

graphics_cards = {
    "GeForce RTX 3060 Ti": "GeForce+RTX+fuer+Gaming/RTX+3060+Ti",
    "GeForce RTX 4090": "GeForce+RTX+fuer+Gaming/RTX+4090",
    # Add more graphics cards here...
}

url = "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all table rows within the desired section
table_rows = soup.select('#slice-container-L8SfcAV5o28ayEFjzq6cfX-table-10 > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(3) > tr')

# Create a dictionary to store the FPS data
fps_data = {}

# Loop through the table rows and extract FPS and name values
for row in table_rows:
    fps_percentage = row.select_one('td:nth-child(2)').text.strip()
    fps_match = re.findall(r'([\d.]+)fps', fps_percentage)  # Extract the FPS value using regex

    if fps_match:  # Check if FPS value is found
        fps = Decimal(fps_match[0])  # Get the first element from the list and convert to Decimal
    else:
        fps = None  # Set fps as None if no value is found

    name = row.select_one('td:nth-child(1) > strong:nth-child(1) > a:nth-child(1)').text.strip()

    # Store the FPS data in the dictionary
    fps_data[name] = fps

base_url = "https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/"
cheapest_prices = {}
cost_per_frame = {}

for card, card_url in graphics_cards.items():
    url = base_url + card_url + ".html/listing_sort/6"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the desired element using CSS selector
    element = soup.select_one("div.p:nth-child(6) > div:nth-child(1) > div:nth-child(9)")

    if element:
        price_text = element.text.strip()
        price_text = re.sub(r"[^\d.,]", "", price_text)  # Remove non-digit characters
        price_text = price_text.replace(".", "").replace(",", ".")  # Replace decimal separator
        price = Decimal(price_text.strip())
        cheapest_prices[card] = price
        cost_per_frame[card] = price / (fps_data.get(card) or 1)  # Assign 1 if fps_data[card] is None

# Sort the graphics cards by cost per frame (lowest to highest)
sorted_cards = sorted(cost_per_frame.items(), key=lambda x: x[1])

# Store the results in a JSON file
results = []
for card, cost in sorted_cards:
    price = cheapest_prices[card]
    formatted_price = locale.format_string("%.2f", price, grouping=True)
    cost_per_frame_value = locale.format_string("%.2f", cost)
    fps_value = fps_data.get(card, "N/A")
    
    result = {
        "card": card,
        "cheapest_price": formatted_price,
        "cost_per_frame": cost_per_frame_value,
        "fps": fps_value
    }
    results.append(result)

with open("results.json", "w") as file:
    json.dump(results, file)

# Print the results to the console
for card, cost in sorted_cards:
    price = cheapest_prices[card]
    formatted_price = locale.format_string("%.2f", price, grouping=True)
    cost_per_frame_value = locale.format_string("%.2f", cost)
    fps_value = fps_data.get(card, "N/A")
    print(f"{card}:")
    print(f"Cheapest price: {formatted_price} €")
    print(f"Cost per frame: {cost_per_frame_value} € per frame")
    print(f"FPS: {fps_value} (Ultra 1080p)")
    print()
