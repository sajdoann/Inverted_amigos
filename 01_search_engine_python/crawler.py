"""
simple crawler that downloads a $num_books books
might not work for bigger downloads
"""
# TODO Store the books in Apache Parquet Format

import requests
from bs4 import BeautifulSoup
import os


def download_gutenberg_books(num_books=30, id=0):
    id += 1
    base_url = "https://www.gutenberg.org"
    search_url = f"{base_url}/ebooks/search/?query=&submit_search=Go&sort_order=downloads"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    book_links = []
    for link in soup.select('li.booklink a'):
        if len(book_links) < num_books:
            book_links.append(link['href'])
        else:
            break

    for book_link in book_links:
        book_page = requests.get(f"{base_url}{book_link}")
        book_soup = BeautifulSoup(book_page.content, 'html.parser')

        title = book_soup.find('h1').text.strip()

        print(f"Downloading: {title}")
        download_link = book_soup.find('a', string='Plain Text UTF-8')[
            'href']  # Updated to use 'string' instead of 'text'

        # Ensure the download link is complete
        if not download_link.startswith('http'):
            download_link = f"{base_url}{download_link}"

        book_content = requests.get(download_link).text

        # Extract title, author, release date, and language from the book content
        metadata_section, content_section = book_content.split('*** START OF THE PROJECT GUTENBERG EBOOK')

        title = None
        author = None
        release_date = None
        language = None

        for line in metadata_section.splitlines():
            if line.startswith("Title:"):
                title = line.split("Title:")[1].strip() if "Title:" in line else None
            elif line.startswith("Author:"):
                author = line.split("Author:")[1].strip() if "Author:" in line else None
            elif line.startswith("Release date:"):
                release_date = line.split("Release date:")[1].strip() if "Release date:" in line else None
            elif line.startswith("Language:"):
                language = line.split("Language:")[1].strip() if "Language:" in line else None

        # Create a metadata dictionary with the extracted information
        data = {
            'ID': id,
            'title': title if title else "Unknown Title",
            'author': author if author else "Unknown Author",
            'release_date': release_date if release_date else "Unknown Release Date",
            'language': language if language else "Unknown Language"
        }

        # Save the book content
        filename = f"{id}_{title}.txt"
        with open(os.path.join('gutenberg_books', filename), 'w', encoding='utf-8') as f:
            f.write(content_section)

        # Save metadata
        with open('gutenberg_data.txt', 'a', encoding='utf-8') as meta_file:
            meta_file.write(f"{data}\n")

        id += 1


if not os.path.exists('gutenberg_books'):
    os.makedirs('gutenberg_books')

last_book_id = 0
download_gutenberg_books(25, last_book_id)
