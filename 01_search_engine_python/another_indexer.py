"""
Here is another way of doing the inerted index.
This code also removes stopwords and punctuation from the text (including underscores and numbers).
It also saves the position of the word in the given text.
"""

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


def insert_document(doc_ID: int, text: dict, dictionary: dict) -> dict:
    for word in text:
        if word in dictionary:
            print(word)
            print(dictionary[word])
            dictionary[word] = dictionary[word].append((doc_ID, text[word]))
        else:
            dictionary[word] = [(doc_ID, text[word])]
    return dictionary

def search_word(word, dictionary):
    if word in dictionary:
        return dictionary[word]
    else:
        return None

if __name__ == '__main__':
    # Load documents from the gutenberg_books folder
    documents = {}
    current_dir = os.path.dirname(__file__)
    folder = 'gutenberg_books'
    folder_path = os.path.join(current_dir, folder)
    inverted_index = dict()

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                doc_id = int(filename.split('_')[0])  # Extract the doc number before the underscore and convert to int
                content = file.read()
                documents[doc_id] = content
        
    for doc_id, content in documents.items():
        content = remove_punctuation(content)
        content = to_lower_case(content)
        content = remove_stopwords(content)
        content = tokenize(content)
        inverted_index = insert_document(doc_id, content, inverted_index)
        with open('another_inverted_index.json', 'a', encoding='utf-8') as json_file:
            json.dump(dict(inverted_index), json_file, ensure_ascii=False, indent=4)