import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "https://fulltime.thefa.com/index.html?selectedSeason=403346465&selectedFixtureGroupAgeGroup=0&selectedDivision=962266925&selectedCompetition=0"  # noqa: E501

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
            {'selector': 'th', 'props': [('text-align', 'centre')]},  # Align titles left  # noqa: E501
            {'selector': '.col1', 'props': [('font-weight', 'bold')]},  # Bold 'Team' column  # noqa: E501
            {'selector': '.col9', 'props': [('font-weight', 'bold')]},  # Bold 'PTS' column  # noqa: E501
            {'selector': 'td, th', 'props': [('padding', '10px')]}  # Add space between columns  # noqa: E501
        ]) \
        .set_table_attributes('class="dataframe"')  # Add a class to the table

    # Convert the styled DataFrame to HTML
    styled_df.hide(axis="index")
    styled_html = styled_df.to_html(index=False)
    styled_html = styled_html.replace('<table', '<table style="max-width: 100%;"')


    # Append HTML content to an existing HTML file
    html_file_path = "content/table.html"

    with open(html_file_path, "r") as html_file:
        existing_content = html_file.read()

    # Identify the start and end positions based on the markers
    start_marker = '<!-- scrape from here onwards -->'
    end_marker = '<!-- end -->'
    start_index = existing_content.find(start_marker)
    end_index = existing_content.find(end_marker) + len(end_marker)

    # Write the new content, replacing the existing content between the markers
    with open(html_file_path, "w") as html_file:
        html_file.write(existing_content[:start_index])
        html_file.write(start_marker)
        html_file.write(" ")
        html_file.write(styled_html)
        html_file.write("<br> <br> <!-- end -->")
        html_file.write(existing_content[end_index:])

    print(f"\nStyled DataFrame content appended to the HTML file: {html_file_path}")  # noqa: E501

else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")

