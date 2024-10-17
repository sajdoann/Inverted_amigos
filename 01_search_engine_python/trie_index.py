import os
import json
from collections import defaultdict

from nltk.corpus import stopwords
import re


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    result = []
    for word in text.lower().split():
        if word in stop_words:
            result.append('|')
        else :
            result.append(word.replace("_", "").replace(".", "").replace(",", "").replace(";", "").replace("\u2019", "'"))
    return result

# Tries (Prefix Trees)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.doc_info = defaultdict(list)  # To store (book_id, positions) pairs, using defaultdict to store positions

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, book_id, position):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        # Append the position of the occurrence of the word in the given book
        node.doc_info[book_id].append(position)
        
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.doc_info

    def serialize(self):
        """Serialize the Trie to a dictionary for JSON storage."""
        def serialize_node(node):
            return {
                'children': {char: serialize_node(child) for char, child in node.children.items()},
                'doc_info': dict(node.doc_info)  # Convert defaultdict to regular dict for JSON serialization
            }
        return serialize_node(self.root)

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
                documents.append(preprocess_text(content))  # Use preprocess_text here
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
    
    for book_id, words in zip(book_metadata.keys(), documents):
        for position, word in enumerate(words):
            trie.insert(word, book_id, position)  # Pass the position of the word
    
    return trie

# Specify the directory where the books are stored
directory = r"01_search_engine_python/gutenberg_books"

# Read the documents from the specified directory and get their IDs and titles
documents, book_metadata = read_documents_from_directory(directory)


# Create the inverted index
inverted_index = create_inverted_index(documents, book_metadata)

# Delete trie_index.json file if it exists
if os.path.exists("trie_index.json"):
    os.remove("trie_index.json")
with open("trie_index.json", "w", encoding="utf-8") as json_file:
    json.dump(inverted_index.serialize(), json_file, ensure_ascii=False, indent=4)

# Load the Trie from the JSON file
def load_trie_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        trie_data = json.load(json_file)
    
    def deserialize_node(data):
        node = TrieNode()
        node.doc_info = defaultdict(list, data['doc_info'])  # Convert back to defaultdict
        for char, child_data in data['children'].items():
            node.children[char] = deserialize_node(child_data)
        return node
    
    trie = Trie()
    trie.root = deserialize_node(trie_data)
    return trie

# Example of searching for a word in the Trie
word_to_search = "house"  # You can change the search term as needed

# Load the inverted index from the file
inverted_index = load_trie_from_file("trie_index.json")

book_info = inverted_index.search(word_to_search)

if book_info:
    print(f"The word '{word_to_search}' is found in the following books:")
    for book_id, positions in book_info.items():
        book_title = book_metadata[book_id]
        print(f"Book ID: {book_id}, Book Title: {book_title}, Positions: {positions}")
else:
    print(f"'{word_to_search}' not found in the documents.")
