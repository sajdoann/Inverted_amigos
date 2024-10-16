import os
from collections import defaultdict

# Tries (Prefix Trees)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.doc_info = defaultdict(int)  # To store (book_id, count) pairs, using defaultdict to count occurrences

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, book_id):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        # Increment the count of occurrences of the word in the given book
        node.doc_info[book_id] += 1
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.doc_info

# Function to read the content of all text files in the directory along with their IDs and titles
def read_documents_from_directory(directory):
    documents = []
    book_metadata = {}  # To store book_id -> book_title mapping

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            # Extract book ID and title from the filename
            book_id, book_title = extract_id_and_title(filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                documents.append(content)
                book_metadata[book_id] = book_title  # Save the book's ID and title
    return documents, book_metadata

# Helper function to extract the book ID and title from filename
def extract_id_and_title(filename):
    # Assume the filename format is "12345_title.txt", where "12345" is the ID
    # Split by underscore and remove the '.txt' extension
    book_id = filename.split('_')[0]  # Get the ID (part before the underscore)
    book_title = filename.split('_')[1].replace(".txt", "")  # Get the title (part after the underscore)
    return book_id, book_title

# Function to create the inverted index using Trie
def create_inverted_index(documents, book_metadata):
    trie = Trie()
    
    for text, book_id in zip(documents, book_metadata.keys()):
        words = text.lower().split()
        
        for word in words:
            trie.insert(word, book_id)
    
    return trie

# Specify the directory where the books are stored
directory = r"C:\University\Big Data\Inverted Amigos\Inverted_amigos\01_search_engine_python\gutenberg_books"

# Read the documents from the specified directory and get their IDs and titles
documents, book_metadata = read_documents_from_directory(directory)

# Create the inverted index
inverted_index = create_inverted_index(documents, book_metadata)

# Example of searching for a word in the Trie
word_to_search = "stop"  # You can change the search term as needed
book_info = inverted_index.search(word_to_search)

if book_info:
    print(f"The word '{word_to_search}' is found in the following books:")
    for book_id, count in book_info.items():
        book_title = book_metadata[book_id]
        print(f"Book ID: {book_id}, Book Title: {book_title}, Occurrences: {count}")
else:
    print(f"'{word_to_search}' not found in the documents.")
