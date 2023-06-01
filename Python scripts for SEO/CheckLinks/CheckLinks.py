#---------------------------------------------------------------#
#  Script SEO                                                   #
#  Autor: Ignacio Sánchez Gómez                                 #
#  DPTO: BirdCom                                                #
#  Fecha Inicio: 01/06/2023                                     #
#  Versión 0.1                                                  #
#---------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()
broken_links = set()

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def parse_content(response_text):
    parsers = ['html.parser', 'lxml', 'html5lib']
    for parser in parsers:
        try:
            return BeautifulSoup(response_text, parser)
        except Exception as e:
            print(f"Failed to parse using {parser}, trying next parser. Exception: {e}")
    raise ValueError("None of the parsers were able to parse the response")

def crawl(url, root_url):
    global visited_urls, broken_links

    if url in visited_urls or not url.startswith(root_url):
        return

    visited_urls.add(url)
    print("Crawling page:", url)

    try:
        response = requests.get(url)
        if 'text/html' in response.headers.get('Content-Type', ''):
            soup = parse_content(response.text)
            
            for link in soup.find_all(['a', 'link', 'img', 'script', 'iframe']):
                href = link.get('href') or link.get('src')
                if href and not href.startswith('#') and is_valid(href):
                    absolute_url = urljoin(url, href)
                    crawl(absolute_url, root_url)

    except requests.exceptions.RequestException:
        broken_links.add(url)
        print("Broken link:", url)

def print_links(links, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for link in links:
            print(link)
            file.write(link + '\n')

url = input("Enter the URL of the website: ")
parsed_url = urlparse(url)
starting_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

crawl(url, starting_domain)

print("\nCrawling complete. Checking the following links:")
print_links(visited_urls, 'all_links.txt')

if broken_links:
    print("\nThe following links are broken:")
    print_links(broken_links, 'broken_links.txt')
else:
    print("\nAll links are healthy.")
