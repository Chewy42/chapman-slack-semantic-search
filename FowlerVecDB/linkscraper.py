import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_text_and_links_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ')
    text = ' '.join(text.split())

    links = [link.get('href') for link in soup.find_all('a')]
    absolute_links = [urljoin(url, link) for link in links]

    return text, absolute_links


def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def save_links_to_file(links, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')


def web_crawler(url):
    text, links = get_text_and_links_from_url(url)
    save_text_to_file(text, 'output.txt')
    save_links_to_file(links, 'links.txt')


web_crawler('https://catalog.chapman.edu/content.php?catoid=42&navoid=2235')
