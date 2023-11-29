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

# Allow more time for the dynamic content to load (adjust as needed)
time.sleep(10)

# Get the page source after dynamic content has loaded
html_content = driver.page_source

# Close the webdriver
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the div with the specified class
div_container = soup.find("div", class_="results-table table-scroll")

if div_container:
    # Extract data from the table
    data = []
    max_columns = 0

    for row in div_container.find_all("tr"):
        row_data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
        data.append(row_data)
        max_columns = max(max_columns, len(row_data))

    # Create a DataFrame using the extracted data
    headers = ["Competition", "Date & Time", "Home", " ", "Result", " ", "Away"]
    df = pd.DataFrame(data, columns=headers)
    df = df.dropna()

    fixtures_html = df.to_html(index=False)

    file_path = "content/fixtures.html"
    with open(file_path, "a") as html_file:
        # Write the styled HTML to the file
        html_file.write("<h2 align=center> This Season's Results... </h2> <br>")
        html_file.write(fixtures_html)
        html_file.write("<br>")

    print(f"\nStyled DataFrame content appended to the HTML file: {file_path}")
else:
    print("Div container not found with the specified class.")
