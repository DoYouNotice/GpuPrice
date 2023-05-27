import requests
from bs4 import BeautifulSoup
import re
import locale
import json
from decimal import Decimal

# Set the appropriate locale for number formatting
locale.setlocale(locale.LC_ALL, '')

graphics_cards = {
    "GeForce RTX 3060 Ti": "GeForce+RTX+fuer+Gaming/RTX+3060+Ti",
    # Add other graphics card entries here
}

url = "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html"

# Function to scrape the data and return it as a JSON string
def scrape_graphics_card_data():
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

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
        except (Decimal.InvalidOperation, TypeError):
            # Handle conversion errors by setting a default cost value
            cost = Decimal(0)

        # Check if the graphics card is in our dictionary
        if name in graphics_cards:
            # Add the graphics card and its cost per frame to the dictionary
            cost_per_frame[name] = float(cost)

    # Convert the data to JSON format
    json_data = json.dumps(cost_per_frame)
    
    return json_data

# Generate the HTML code with JavaScript to scrape the data when the page is loaded
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Graphics Card Data</title>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
    $(document).ready(function() {{
      // Function to handle the click event
      function handleClick() {{
        $.ajax({{
          type: "GET",
          url: "{url}",
          success: function(response) {{
            var data = $(response).find("table tr:has(td)").map(function(i, v) {{
              var $td = $(this).find("td");
              var name = $td.eq(0).text().trim();
              var cost = parseFloat($td.eq(2).text().trim().replace("$", "").replace(",", ""));
              return {{ name: name, cost: cost }};
            }}).get();
            
            var html = "";
            for (var i = 0; i < data.length; i++) {{
              var card = data[i];
              html += "<p>" + card.name + ": Cost per frame - " + card.cost + "</p>";
            }}
            
            $("#data-container").html(html);
          }}
        }});
      }}
      
      // Bind the click event to the button
      $("#scrape-button").click(handleClick);
    }});
  </script>
</head>
<body>
  <h1>Graphics Card Data</h1>
  <button id="scrape-button">Scrape Data</button>
  <div id="data-container"></div>
</body>
</html>
"""

# Save the HTML code to a file
with open('index.html', 'w') as file:
    file.write(html_code)
