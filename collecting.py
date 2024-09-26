import os
import json
from bs4 import BeautifulSoup

def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr', role='row')
    
    data = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 15:  # Ensure we have enough columns
            project = {
                'Index': cols[0].text.strip(),
                'Acknowledgement Number': cols[1].text.strip(),
                'Registration Number': cols[2].text.strip(),
                'Developer': cols[4].text.strip(),
                'Project Name': cols[5].text.strip(),
                'Status': cols[6].text.strip(),
                'District': cols[7].text.strip(),
                'Taluk': cols[8].text.strip(),
                'Registration Date': cols[9].text.strip(),
                'Completion Date': cols[10].text.strip(),
                'Valid Till': cols[11].text.strip()
            }
            data.append(project)
    
    return data

# Directory containing HTML files
html_dir = 'new_pages'

all_data = []

# Process each HTML file in the directory
for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(html_dir, filename)
        all_data.extend(parse_html_file(file_path))

# Save all data to a single JSON file
with open('all_real_estate_projects.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=2)

print(f"Total projects processed: {len(all_data)}")
print("Data saved to all_real_estate_projects.json")