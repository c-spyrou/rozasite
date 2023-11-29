import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "https://fulltime.thefa.com/index.html?selectedSeason=403346465&selectedFixtureGroupAgeGroup=0&selectedDivision=962266925&selectedCompetition=0"

# Send a GET request to the URL
response = requests.get(url)

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
    df = df.dropna()

    # Apply styling to the DataFrame
    styled_df = df.style \
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'left')]},  # Align titles left
            {'selector': '.col1', 'props': [('font-weight', 'bold')]},  # Bold 'Team' column
            {'selector': '.col9', 'props': [('font-weight', 'bold')]},  # Bold 'PTS' column
            {'selector': 'td, th', 'props': [('padding', '10px')]}  # Add space between columns
        ]) \
        .set_table_attributes('class="dataframe"')  # Add a class to the table

    # Convert the styled DataFrame to HTML
    styled_df.hide(axis="index")
    styled_html = styled_df.to_html(index=False)

    # Append HTML content to an existing HTML file
    html_file_path = "content/table.html"
    with open(html_file_path, "w") as html_file:
        # Write the styled HTML to the file
        html_file.write(styled_html)
        html_file.write("<br/>")

    print(f"\nStyled DataFrame content appended to the HTML file: {html_file_path}")

else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")