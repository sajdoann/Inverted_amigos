import os
import json
from collections import defaultdict

# Tries (Prefix Trees)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.doc_info = defaultdict(list)

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return list(node.doc_info.items())

# Load the Trie from the JSON file
def load_trie_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        trie_data = json.load(json_file)
    
    def deserialize_node(data):
        node = TrieNode()
        node.doc_info = defaultdict(list, data['doc_info'])
        for char, child_data in data['children'].items():
            node.children[char] = deserialize_node(child_data)
        return node
    
    trie = Trie()
    trie.root = deserialize_node(trie_data)
    return trie


if __name__ == '__main__':
    # Example of searching for a word in the Trie
    word_to_search = "house"  # You can change the search term as needed

    # Load the inverted index from the file
    inverted_index = load_trie_from_file("trie_index.json")

    book_info = inverted_index.search(word_to_search)

    if book_info:
        print(f"The word '{word_to_search}' is found in the following books:")
        for book_id, positions in book_info.items():
            print(f"Book ID: {book_id}, Positions: {positions}")
    else:
        print(f"'{word_to_search}' not found in the documents.")
