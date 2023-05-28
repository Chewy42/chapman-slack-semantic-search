import requests
from bs4 import BeautifulSoup
import time
import os

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError) as err:
        print(f"Error: {err}")
        return None

    return BeautifulSoup(response.text, 'html.parser')

def extract_links(soup, base_url):
    return [base_url + link.get('href') for link in soup.select('a') if link.get('href') and link.get('href').startswith('/')]

def extract_text(soup):
    return soup.get_text()

def write_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def scrape_site(base_url, output_dir):
    visited_links = set()
    to_visit = [base_url]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while to_visit:
        url = to_visit.pop(0)
        if url in visited_links:
            continue

        print(f"Visiting: {url}")
        soup = get_page_content(url)
        if soup:
            visited_links.add(url)
            to_visit.extend(extract_links(soup, base_url))

            text = extract_text(soup)
            filename = os.path.join(output_dir, f"{len(visited_links)}.txt")
            write_to_file(filename, text)

        time.sleep(1)  # Delay to prevent overloading the server !!

    print(f"Visited {len(visited_links)} pages.")

base_url = "https://catalog.chapman.edu"
output_dir = "./catalog_text_files"
scrape_site(base_url, output_dir)
