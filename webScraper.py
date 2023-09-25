import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re  # Import the regular expressions module

# Function to sanitize filenames
def sanitize_filename(filename):
    # Remove characters that are not allowed in filenames
    return re.sub(r'[\\/:"*?<>|]', '_', filename)

# URL of the main page with the list of subpage links
base_url = 'https://www.lagboken.se/Lagboken/start/skatteratt/?s=0&sort=Relevance&q='
url = 'https://www.lagboken.se/Lagboken/start/skatteratt/?s=0&sort=Relevance&q='  # The same URL as base_url initially

# Create a directory to save the text files
if not os.path.exists('subpage_texts'):
    os.mkdir('subpage_texts')

# Send an HTTP GET request to the main page
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the main page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the unordered list with id "paging-list"
    paging_list = soup.find('ul', id='paging-list')

    # Find all the links to subpages within the unordered list
    subpage_links = paging_list.find_all('a', href=True)

    # Loop through the subpage links and scrape text from each subpage
    for link in subpage_links:
        subpage_url = urljoin(base_url, link['href'])
        subpage_response = requests.get(subpage_url)
        
        if subpage_response.status_code == 200:
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')
            
            # Find the div with class "o-layout__content" and scrape its text
            content_div = subpage_soup.find('div', class_='o-layout__content')
            
            if content_div:
                text = content_div.get_text()
                
                # Sanitize the filename
                sanitized_filename = sanitize_filename(link.text.strip())
                
                # Create the filename for each subpage
                filename = f'subpage_texts/{sanitized_filename}.txt'
                
                # Write the text to the file
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(text)
        else:
            print(f"Failed to retrieve subpage {subpage_url}. Status code: {subpage_response.status_code}")
else:
    print(f"Failed to retrieve the main page. Status code: {response.status_code}")