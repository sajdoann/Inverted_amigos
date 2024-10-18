import pytest
import os
from hashed_index import index_all_books

current_dir = os.path.dirname(__file__)
books = 'gutenberg_books'
datamart = 'Datamart'
indexed = 'indexed_docs.txt'
datamart_path = os.path.join(current_dir, datamart)
indexed_path = os.path.join(current_dir, indexed)

def remove_datamart_files(datamart_path):
    for filename in os.listdir(datamart_path):
        os.remove(os.path.join(datamart_path, filename))

def remove_indexed_docs_file(indexed_path):
    if os.path.exists(indexed_path):
        os.remove(indexed_path)

@pytest.fixture
def setup_benchmark_remove_all():
    remove_datamart_files(datamart_path)
    remove_indexed_docs_file(indexed_path)
    return current_dir, books, indexed, datamart

@pytest.fixture
def setup_benchmark_remove_all_and_index_25_books():
    remove_datamart_files(datamart_path)
    remove_indexed_docs_file(indexed_path)
    # Indexar los 25 libros
    index_all_books(current_dir, books, indexed, datamart)
    remove_indexed_docs_file(indexed_path)
    return current_dir, books, indexed, datamart

@pytest.fixture
def setup_benchmark_remove_all_and_index_50_books():
    remove_datamart_files(datamart_path)
    remove_indexed_docs_file(indexed_path)
    # Indexar los 50 libros
    index_all_books(current_dir, books, indexed, datamart)
    remove_indexed_docs_file(indexed_path)
    index_all_books(current_dir, books, indexed, datamart)
    remove_indexed_docs_file(indexed_path)
    return current_dir, books, indexed, datamart

@pytest.fixture
def setup_benchmark_remove_all_and_index_75_books():
    remove_datamart_files(datamart_path)
    remove_indexed_docs_file(indexed_path)
    # Indexar los 50 libros
    index_all_books(current_dir, books, indexed, datamart)
    remove_indexed_docs_file(indexed_path)
    index_all_books(current_dir, books, indexed, datamart)
    remove_indexed_docs_file(indexed_path)
    index_all_books(current_dir, books, indexed, datamart)
    remove_indexed_docs_file(indexed_path)
    return current_dir, books, indexed, datamart

def read_and_index_books(current_dir, books, indexed, datamart):
    index_all_books(current_dir, books, indexed, datamart)
    

def test_my_function(benchmark, setup_benchmark_remove_all):
    # Test 1: Reeding and Indexing all the books
    data = setup_benchmark_remove_all
    benchmark.pedantic(read_and_index_books, args=data, iterations=1, rounds=5, warmup_rounds=0)

def test_my_function_25_books(benchmark, setup_benchmark_remove_all_and_index_25_books):
    # Test 2: Indexing 25 books when 25 books are already indexed
    data = setup_benchmark_remove_all_and_index_25_books
    benchmark.pedantic(read_and_index_books, args=data, iterations=1, rounds=5, warmup_rounds=0)

def test_my_function_50_books(benchmark, setup_benchmark_remove_all_and_index_50_books):
    data = setup_benchmark_remove_all_and_index_50_books
    benchmark.pedantic(read_and_index_books, args=data, iterations=1, rounds=5, warmup_rounds=0)

def test_my_function_75_books(benchmark, setup_benchmark_remove_all_and_index_75_books):
    data = setup_benchmark_remove_all_and_index_75_books
    benchmark.pedantic(read_and_index_books, args=data, iterations=1, rounds=5, warmup_rounds=0)