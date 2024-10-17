from query_engine import QueryEngine, Indexer, Field


def one_word_search_filter_print(query_engine: QueryEngine):
    """
    This example shows searching for a text with some word
    using chosen indexer, and than filtring based on metadata
    and printing the first line containing the word from each book
    """
    indexer = Indexer.TRIE
    word = "winter"
    results = query_engine.search(word, indexer)

    field = Field.LANGUAGE
    value = "English"
    filtered_results = query_engine.filter_with_metadata(field, value, results)

    for result in filtered_results:
        book_id, positions = result
        line, pos = query_engine.get_part_of_book_with_word(book_id, positions[0])
        print(book_id, end='\t')
        query_engine.print_coloured(line.split(), pos)


def multiple_word_search_filter_print(query_engine: QueryEngine):
    """
    This example shows dearching for books that contain both words
    and filtering based on the author with printing from each book
    two lines each with the first occurence of one of given words
    """
    words = ["winter", "summer"]
    indexer = Indexer.HASHED
    results = query_engine.search_multiple_words(words, indexer)

    field = Field.AUTHOR
    value = "William Shakespeare"
    filtered_results = query_engine.filter_with_metadata(field, value, results)

    for result in filtered_results:
        book_id = result[0]
        print(book_id)
        word1_positions = result[1][0]
        word2_positions = result[1][1]
        line, pos = query_engine.get_part_of_book_with_word(book_id, word1_positions[0])
        query_engine.print_coloured(line.split(), pos)
        line, pos = query_engine.get_part_of_book_with_word(book_id, word2_positions[0])
        query_engine.print_coloured(line.split(), pos)

if __name__ == "__main__":
    query_engine = QueryEngine()
    # one_word_search_filter_print(query_engine)
    multiple_word_search_filter_print(query_engine)
