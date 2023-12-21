import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_emails_from_url(url, visited_urls, emails):
    if url in visited_urls:
        return

    response = requests.get(url)
    if response.status_code == 200:
        visited_urls.add(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all anchor tags
        links = soup.find_all('a', href=True)

        for link in links:
            new_url = urljoin(url, link['href'])
            # Check if the URL is not visited and starts with the base URL
            if new_url not in visited_urls and new_url.startswith(url):
                fetch_emails_from_url(new_url, visited_urls, emails)

        # Find emails using regex
        new_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', response.text)
        for email in new_emails:
            emails.add(email)
    else:
        print("Failed to retrieve the website. Status code:", response.status_code)

if __name__ == '__main__':
    urls = ['https://www.acebattery.com', 'https://www.evermorelight.com']  # Add more URLs here
    
    visited_urls = set()
    emails = set()
    for url in urls:
        fetch_emails_from_url(url, visited_urls, emails)
    print(emails)
