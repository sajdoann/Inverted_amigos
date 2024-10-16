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
from concurrent.futures import ThreadPoolExecutor

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'[^\w\s]', ' ', text).replace("_", " ")  # Eliminar puntuación
    text = re.sub(r'\d+', ' ', text)  # Eliminar números
    result = []
    for word in text.lower().split():  # Convertir a minúsculas y dividir en palabras
        if word not in stop_words:
            result.append(word)
    return result

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

def get_hash(word, num_buckets):
    # Usamos hashlib para generar un hash de la palabra
    hash_object = hashlib.sha1(word.encode())
    hex_dig = hash_object.hexdigest()

    # Convertimos a un entero y lo usamos para distribuir en los "buckets"
    return int(hex_dig, 16) % num_buckets

def save_word_to_hashed_file(word, data, file_data):
    if word not in file_data:
        file_data[word] = data
    else:
        file_data[word].extend(data)

def safe_pickle_load(filepath):
    # Verificar si el archivo existe y tiene contenido
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def save_bucket_to_file(bucket_data, bucket_id, base_dir):
    path = os.path.join(base_dir, f'bucket_{bucket_id}.pkl')

    # Cargar los datos actuales del archivo si existe
    if os.path.exists(path):
        with open(path, 'rb') as f:
            file_data = pickle.load(f)
    else:
        file_data = {}

    # Actualizar el archivo con los nuevos datos del bucket
    for word, data in bucket_data.items():
        if word in file_data:
            file_data[word].extend(data)
        else:
            file_data[word] = data

    # Guardar los cambios en el archivo
    with open(path, 'wb') as f:
        pickle.dump(file_data, f)

def process_buckets(batch_data, base_dir, num_buckets=10):
    # Crear un pool de hilos
    with ThreadPoolExecutor(max_workers=num_buckets) as executor:
        futures = []
        for bucket_id in range(num_buckets):
            # Filtrar las palabras que pertenecen a este bucket
            bucket_data = {word: data for word, data in batch_data.items() if get_hash(word, num_buckets) == bucket_id}
            # Guardar los datos del bucket en su archivo correspondiente
            futures.append(executor.submit(save_bucket_to_file, bucket_data, bucket_id, base_dir))

        # Esperar a que todos los hilos terminen
        for future in futures:
            future.result()

# Clasificación previa de palabras en buckets
def classify_words_in_buckets(text, doc_ID, num_buckets=10):
    batch_data = {}
    for word, positions in text.items():
        bucket_id = get_hash(word, num_buckets)
        if word not in batch_data:
            batch_data[word] = [(doc_ID, positions)]
        else:
            batch_data[word].extend([(doc_ID, positions)])
    return batch_data

# Función principal para insertar documentos
def insert_document(doc_ID, text, directory, num_buckets=10):
    batch_data = classify_words_in_buckets(text, doc_ID, num_buckets)
    process_buckets(batch_data, directory, num_buckets)

def load_bucket(bucket_id, base_dir):
    path = os.path.join(base_dir, f'bucket_{bucket_id}.pkl')

    # Si el archivo existe, cargar los datos, si no, devolver diccionario vacío
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return {}

# Función para buscar una palabra
def search_word(word, base_dir, num_buckets=10):
    # Determinar el bucket correspondiente a la palabra
    bucket_id = get_hash(word, num_buckets)
    
    # Cargar los datos del bucket correspondiente
    bucket_data = load_bucket(bucket_id, base_dir)
    
    # Buscar la palabra en el bucket
    if word in bucket_data:
        return bucket_data[word]  # Retorna las ocurrencias de la palabra
    else:
        return None  # Si no se encuentra la palabra, devolver None

if __name__ == '__main__':

     # Load documents from the gutenberg_books folder
    documents = {}
    current_dir = os.path.dirname(__file__)
    folder = 'gutenberg_books'
    folder_path = os.path.join(current_dir, folder)
    inverted_index = dict()

    datamart = os.path.join(current_dir, 'Datamart')

    if not os.path.exists(datamart):
        os.makedirs(datamart)
    else:
        for filename in os.listdir(datamart):
            file_path = os.path.join(datamart, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                doc_id = int(filename.split('_')[0])  # Extract the doc number before the underscore and convert to int
                content = file.read()
                documents[doc_id] = content
        
    for doc_id, content in documents.items():
        print(doc_id)
        content = preprocess_text(content)
        content = tokenize(content)
        inverted_index = insert_document(doc_id, content, datamart)
    
    print(search_word('house', datamart))