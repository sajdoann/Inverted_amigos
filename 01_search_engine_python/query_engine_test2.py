from query_engine import QueryEngine

if __name__ == '__main__':
    query_engine = QueryEngine()
    query_engine.load_inverted_index_from_file('another_inverted_index.json')
    query_engine.load_metadata_from_file('gutenberg_data.txt')
    word = 'word'
    result = query_engine.get_indexes_of_books_with(word)
    print(f"Documents containing '{word}': {result}")
    field, value = ('author', 'Elizabeth Cleghorn Gaskell')
    result = query_engine.get_indexes_of_books_with_metadata(field, value)
    print(result)