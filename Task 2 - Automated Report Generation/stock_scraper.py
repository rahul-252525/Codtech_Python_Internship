import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
# openpyxl engine automatically use hota hai pandas ke through, alag se import zaroori nahi

# URL for NIFTY 50 Companies on Wikipedia
url = "https://en.wikipedia.org/wiki/NIFTY_50"

# User-Agent header to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Fetch page content
    response = requests.get(url, headers=headers)
    response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the NIFTY 50 companies table
    table = soup.find('table', {'class': 'wikitable sortable'})

    if table:
        # Extract table headers
        table_headers = [th.get_text(strip=True) for th in table.find_all('th') if th.get_text(strip=True)]

        # Extract data rows
        data = []
        for row in table.find_all('tr')[1:]: # Skip the header row
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            data.append(row_data)

        # Ensure data rows match the number of headers
        if table_headers:
            num_expected_cols = len(table_headers)
            filtered_data = [row[:num_expected_cols] for row in data if len(row) >= num_expected_cols]
        else:
            # Fallback if headers are not found or empty
            num_expected_cols = 4 
            filtered_data = [row[:num_expected_cols] for row in data if len(row) >= num_expected_cols]
            table_headers = [f"Column {i+1}" for i in range(num_expected_cols)]

        # Create a Pandas DataFrame
        df = pd.DataFrame(filtered_data, columns=table_headers)

        # Generate a timestamp for the report filename
        report_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"nifty_50_companies_report_{report_timestamp}.xlsx"

        # Create a Pandas Excel writer object
        # openpyxl engine automatically use hoga
        writer = pd.ExcelWriter(report_filename, engine='openpyxl')
        df.to_excel(writer, sheet_name='NIFTY 50 Companies', index=False)

        # Access the worksheet object to apply formatting
        worksheet = writer.sheets['NIFTY 50 Companies']

        # --- Formatting ---

        # 1. Headers ko Bold karna
        # openpyxl ke styles se Font import karna padega for bolding
        from openpyxl.styles import Font 

        header_font = Font(bold=True)
        for col_num, column_title in enumerate(table_headers, 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.font = header_font

        # 2. Columns ko Auto-fit karna
        for column in worksheet.columns:
            max_length = 0
            column_name = column[0].column_letter # Get the column name (e.g., 'A', 'B')
            for cell in column:
                try: # Handle non-string values
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) # Thodi extra space for padding
            worksheet.column_dimensions[column_name].width = adjusted_width

        # Save the Excel file
        writer.close() # writer.save() is deprecated, use .close()

        print(f"Report successfully saved to {report_filename} with formatting.")

    else:
        print("Error: Could not find the NIFTY 50 companies table on the page.")

except requests.exceptions.RequestException as e:
    print(f"Network or HTTP error: {e}")
except Exception as e:
    print(f"An unexpected error occurred during scraping or report generation: {e}")