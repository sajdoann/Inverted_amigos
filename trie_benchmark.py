import os
import json
from collections import defaultdict
import pytest

# Trie (Prefix Tree) classes and methods
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
    
    for book_id, text in zip(book_metadata.keys(), documents):
        words = text.lower().split()
        
        for position, word in enumerate(words):
            trie.insert(word, book_id, position)  # Pass the position of the word
    
    return trie

# Benchmarking function using pytest-benchmark
@pytest.mark.benchmark
def test_create_and_save_inverted_index(benchmark):
    # Specify the directory where the books are stored
    directory = r"C:\University\Big Data\Inverted Amigos\Inverted_amigos\01_search_engine_python\gutenberg_books"
    documents, book_metadata = read_documents_from_directory(directory)

    def create_and_save_index():
        # Create the inverted index
        inverted_index = create_inverted_index(documents, book_metadata)
        # Serialize and save the trie structure to "trie_index.json"
        with open("trie_index.json", "w", encoding="utf-8") as json_file:
            json.dump(inverted_index.serialize(), json_file, ensure_ascii=False, indent=4)

    # Benchmark the entire process
    benchmark(create_and_save_index)
