import pytest
from query_engine import QueryEngine, Indexer

@pytest.fixture
def engine():
    return QueryEngine()

@pytest.mark.benchmark
def test_search_trie(engine, benchmark):
    word = "house"
    results = benchmark(engine.search, word, Indexer.TRIE)

@pytest.mark.benchmark
def test_search_hashed(engine, benchmark):
    word = "test"
    results = benchmark(engine.search, word, Indexer.HASHED)

@pytest.mark.benchmark
def test_search_multiple_words_trie(engine, benchmark):
    words = ["example", "test"]
    results = benchmark(engine.search_multiple_words, words, Indexer.TRIE)

@pytest.mark.benchmark
def test_search_multiple_words_hashed(engine, benchmark):
    words = ["search", "word"]
    results = benchmark(engine.search_multiple_words, words, Indexer.HASHED)
