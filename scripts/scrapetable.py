import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "https://fulltime.thefa.com/index.html?selectedSeason=403346465&selectedFixtureGroupAgeGroup=0&selectedDivision=962266925&selectedCompetition=0"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the specified class
    table = soup.find("table", class_="cell-dividers")

    # Extract data from the table
    data = []
    headers = []
    for i, row in enumerate(table.find_all('tr')):
        cols = row.find_all(['th', 'td'])
        if i == 0:  # Assume the first row contains headers
            headers = [col.text.strip() for col in cols]
        else:
            data.append([col.text.strip() for col in cols])

    # Create a DataFrame using the extracted data and headers
    df = pd.DataFrame(data, columns=headers)

    # Append DataFrame content to an existing markdown file
    markdown_file_path = "content/table.md"
    with open(markdown_file_path, "a") as markdown_file:
        # Add a header for the table
        markdown_file.write("\n## League Table\n\n")
        # Convert the DataFrame to markdown and write to the file
        markdown_file.write(df.to_html(index=False))
        markdown_file.write("\n\n")

    print(f"\nDataFrame content appended to the markdown file: {markdown_file_path}")

else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
