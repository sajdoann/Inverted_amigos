"""
Here is another way of doing the inerted index.
This code also removes stopwords and punctuation from the text (including underscores and numbers).
It also saves the position of the word in the given text.
"""

from nltk.corpus import stopwords
import re
import os
import json
import hashlib
import pickle

def remove_punctuation(text):
    text = re.sub(r'[^\w\s]', ' ', text).replace("_", " ")
    return re.sub(r'\d+', ' ', text)

def to_lower_case(text):
    return text.lower()

def tokenize(text):
    counter = 1
    phrase = dict()
    for word in text:
        if word == '|':
            pass
        else:
            if word in phrase:
                phrase[word].append(counter)
            else:
                phrase[word] = [counter]
        counter += 1
    return phrase

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    result = []
    for word in text.split():
        if word in stop_words:
            result.append("|")
        else:
            result.append(word)
    return result

def get_hash(word, num_buckets):
    # Usamos hashlib para generar un hash de la palabra
    hash_object = hashlib.sha1(word.encode())
    hex_dig = hash_object.hexdigest()

    # Convertimos a un entero y lo usamos para distribuir en los "buckets"
    return int(hex_dig, 16) % num_buckets

def save_word_to_hashed_file(word, data, base_dir, num_buckets=10):
    bucket = get_hash(word, num_buckets)
    path = os.path.join(base_dir, f'bucket_{bucket}.pkl')

    # Si el archivo no existe, crearlo
    if os.path.exists(path):
        with open(path, 'rb') as f:
            file_data = pickle.load(f)
    else:
        file_data = {}

    # Añadir o actualizar la palabra
    if word not in file_data:
        file_data[word] = data
    else:
        file_data[word].extend(data)

    # Escribir de nuevo al archivo usando pickle
    with open(path, 'wb') as f:
        pickle.dump(file_data, f)


def insert_document(doc_ID: int, text: dict, directory) -> dict:
    for word in text:
        save_word_to_hashed_file(word, [(doc_ID, text[word])], directory)


if __name__ == '__main__':
    # Load documents from the gutenberg_books folder
    documents = {}
    current_dir = os.path.dirname(__file__)
    folder = 'dummy_books'
    datamart = os.path.join(current_dir, 'Datamart')
    folder_path = os.path.join(current_dir, folder)
    inverted_index = dict()

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                doc_id = int(filename.split('_')[0])  # Extract the doc number before the underscore and convert to int
                content = file.read()
                documents[doc_id] = content
        
    for doc_id, content in documents.items():
        print(doc_id)
        content = remove_punctuation(content)
        content = to_lower_case(content)
        content = remove_stopwords(content)
        content = tokenize(content)
        inverted_index = insert_document(doc_id, content, datamart)