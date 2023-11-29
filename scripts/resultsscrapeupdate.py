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

    # Manually specify column headers based on your knowledge of the table structure
    headers = ["Competition", "Date & Time", "Home", " ", "Result", " ", "Away", "Status"]

    # Create a DataFrame using the extracted data
    df = pd.DataFrame(data, columns=headers)
    df['Date & Time'] = df['Date & Time'].str.replace('\n', ' ')

    df = df.dropna()

    fixtures_html = df.to_html(index=False)

    # File path
    file_path = "content/fixtures.html"

    # Read the existing content from the file
    with open(file_path, "r") as html_file:
        existing_content = html_file.read()

    # Identify the start and end positions based on the markers
    start_marker = "<h2 align=center> This Season's Results... </h2> <br>"
    end_marker = '</table>'
    start_index = existing_content.find(start_marker)
    end_index = existing_content.find(end_marker) + len(end_marker)

    # Write the new content, replacing the existing content from the identified point
    with open(file_path, "w") as html_file:
        html_file.write(existing_content[:start_index])
        html_file.write("<h2 align=center> This Season's Results... </h2> <br>")
        html_file.write(fixtures_html)
        html_file.write(existing_content[end_index:])
        html_file.write("<br/>")

    print(f"\nStyled DataFrame content appended to the HTML file: {file_path}")
else:
    print("Div container not found with the specified class.")
