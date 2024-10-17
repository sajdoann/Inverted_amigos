import pytest
import os
from hashed_index import index_all_books

def read_and_index_books():
    current_dir = os.path.dirname(__file__)
    books = 'gutenberg_books'
    datamart = 'Datamart'
    indexed = 'indexed_docs.txt'
    index_all_books(current_dir, books, indexed, datamart)
    

def test_my_function(benchmark):
    benchmark.pedantic(read_and_index_books, iterations=5, rounds=1)