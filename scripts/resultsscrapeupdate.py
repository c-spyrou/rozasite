import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "https://fulltime.thefa.com/displayTeam.html?divisionseason=734243150&teamID=597757996"  # noqa: E501

# Set up the selenium webdriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

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

    # Columns
    headers = ["Competition", "Date & Time", "Home", " ", "Result", " ", "Away", "Status"]  # noqa: E501

    # Create a DataFrame using the extracted data
    df = pd.DataFrame(data, columns=headers)
    df['Date & Time'] = df['Date & Time'].str.replace('\n', ' ')
    df['Result'] = df['Result'].str.replace('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\n', ' ')  # noqa: E501

    df = df.dropna()

    fixtures_html = df.to_html(index=False)

    # File path
    file_path = "content/fixtures.html"

    # Read the existing content from the file
    with open(file_path, "r") as html_file:
        existing_content = html_file.read()

    # Identify the start and end positions based on the markers
    start_marker = "<h2 align=center> This Season's Results... </h2> <br>"
    end_marker = '<!-- end -->'
    start_index = existing_content.find(start_marker)
    end_index = existing_content.find(end_marker) + len(end_marker)

    with open(file_path, "w") as html_file:
        html_file.write(existing_content[:start_index])
        html_file.write("<h2 align=center> This Season's Results... </h2> <br>")  # noqa: E501
        html_file.write(fixtures_html)
        html_file.write("<br> <!-- end -->")
        html_file.write(existing_content[end_index:])

    print(f"\nStyled DataFrame content appended to the HTML file: {file_path}")
else:
    print("Div container not found with the specified class.")
