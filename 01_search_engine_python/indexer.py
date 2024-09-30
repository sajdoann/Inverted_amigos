""" 
TODO: make index also for metadata from gutenbergdata file
simple indexer
you need to pip install nltk

"""

import os
import json

from collections import defaultdict
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def index_document(doc_id, content, index):
    tokens = word_tokenize(content.lower())
    unique_tokens = set(tokens)  # Use a set to avoid duplicate words in the same document
    for token in unique_tokens:
        index[token].append(doc_id)

# Initialize the index
inverted_index = defaultdict(list)

# Load documents from the gutenberg_books folder
documents = {}
folder_path = 'gutenberg_books'

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            doc_id = int(filename.split('_')[0])  # Extract the doc number before the underscore and convert to int
            content = file.read()
            documents[doc_id] = content

# Index all documents
for doc_id, content in documents.items():
    index_document(doc_id, content, inverted_index)

with open('inverted_index.json', 'w', encoding='utf-8') as json_file:
    json.dump(dict(inverted_index), json_file, ensure_ascii=False, indent=4)
