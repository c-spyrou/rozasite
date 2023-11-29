import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "https://fulltime.thefa.com/displayTeam.html?divisionseason=734243150&teamID=597757996"

# Set up the selenium webdriver (make sure you have the appropriate webdriver installed)
driver = webdriver.Chrome()

# Send a GET request to the URL using selenium
driver.get(url)

# Allow some time for the dynamic content to load (adjust as needed)
time.sleep(15)

# Get the page source after dynamic content has loaded
html_content = driver.page_source

# Close the webdriver
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the div with the specified class
div_container = soup.find("div", class_="fixtures-table table-scroll")

if div_container:
    # Extract data from the div
    data = []
    headers = []

    for row in div_container.find_all("tr"):
        row_data = []
        # Find all cells in the row
        for cell in row.find_all(['td', 'th']):
            row_data.append(cell.text.strip())
        
        if len(row_data) == len(headers) or not headers:
            if not headers:
                headers = row_data
            else:
                data.append(row_data)
        else:
            print(f"Skipping row with unexpected number of columns: {row_data}")

    # Create a DataFrame using the extracted data
    df = pd.DataFrame(data, columns=headers)
    df = df.dropna()

    fixtures_html = df.to_html(index=False)

    file_path = "content/fixtures.html"
    with open(file_path, "a") as html_file:
        # Write the styled HTML to the file
        html_file.write(fixtures_html)
        html_file.write("\n\n")

    print(f"\nStyled DataFrame content appended to the HTML file: {file_path}")
else:
    print("Div container not found with the specified class.")

