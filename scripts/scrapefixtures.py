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
time.sleep(5)

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

    # Assume the relevant data is in child elements (e.g., divs or spans)
    for i, child in enumerate(div_container.find_all(['div', 'span'])):
        # Extract relevant data from each child
        data.append(child.text.strip())

    # Create a DataFrame using the extracted data
    df = pd.DataFrame(data, columns=['headers'])
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


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # URL of the website to scrape
# url = "https://fulltime.thefa.com/displayTeam.html?divisionseason=734243150&teamID=597757996"

# # Send a GET request to the URL
# response = requests.get(url)

# if response.status_code == 200:
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find the div with the specified class
#     div_container = soup.find("div", class_="fixtures-table.table-scroll")

#     if div_container:
#         # Extract data from the div
#         data = []
#         headers = []

#         # Assume the relevant data is in child elements (e.g., divs or spans)
#         for i, child in enumerate(div_container.find_all(['div', 'span'])):
#             # Extract relevant data from each child
#             data.append(child.text.strip())

#         # Create a DataFrame using the extracted data
#         df = pd.DataFrame(data, columns=['headers'])
#         df = df.dropna()

#         fixtures_html = df.to_html(index=False)

#         file_path = "content/fixtures.html"
#         with open(file_path, "a") as html_file:
#             # Write the styled HTML to the file
#             html_file.write(fixtures_html)
#             html_file.write("\n\n")

#         print(f"\nStyled DataFrame content appended to the HTML file: {file_path}")
#     else:
#         print("Div container not found with the specified class.")
# else:
#     print(f"Failed to fetch the page. Status code: {response.status_code}")
