import sqlite3

from nltk.corpus import stopwords
import re
import os
import json

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

def create_index_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inverted_index (
            word TEXT,
            book_id TEXT,
            position TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_to_db(book_id, content, cursor):
    for word in content:
        cursor.execute('''
            INSERT INTO inverted_index (word, book_id, position)
            VALUES (?, ?, ?)
        ''', (word, book_id, json.dumps(content[word])))
        conn.commit()
    conn.close()

if __name__ == '__main__':
    # Load documents from the gutenberg_books folder
    documents = {}
    current_dir = os.path.dirname(__file__)
    folder = 'dummy_books'
    datamart = os.path.join(current_dir, 'Datamart')
    folder_path = os.path.join(current_dir, folder)
    # Crear una conexión a SQLite
    conn = sqlite3.connect(os.path.join(datamart, 'datamart.db'))
    cursor = conn.cursor()
    create_index_table(os.path.join(datamart, 'datamart.db'))
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
        print(doc_id)
        inverted_index = add_to_db(doc_id, content, cursor)
