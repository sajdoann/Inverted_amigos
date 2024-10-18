import os
import ast
from enum import Enum
from trie_searcher import load_trie_from_file
from hashed_index import search_word

# These paths are relative from this script directory
PATH_TO_TRIE_INDEXER_FILE = "trie_index.json"
PATH_TO_DATAMART = "Datamart"


class Indexer(Enum):
    TRIE = 0
    HASHED = 1


class Field(Enum):
    ID = "ID"
    TITLE = "title"
    AUTHOR = "author"
    RELEASE_DATE = "release_date"
    LANGUAGE = "language"


class QueryEngine:
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.metadata = None

    def search(self, word, indexer: Indexer):
        if indexer == Indexer.TRIE:
            path = os.path.join(self.script_dir, PATH_TO_TRIE_INDEXER_FILE)
            inverted_index = load_trie_from_file(path)
            results = inverted_index.search(word)
            return results
        elif indexer == Indexer.HASHED:
            datamart_path = os.path.join(self.script_dir, PATH_TO_DATAMART)
            results = search_word(word, datamart_path)
            return results
        else:
            raise ValueError("There are no available indexers with this name.")

    def search_multiple_words(self, words: list, indexer: Indexer) -> list[tuple]:
        all_results = [self.search(word, indexer) for word in words]
        return self._compile_results_for_many_words(all_results)
        
    def _compile_results_for_many_words(self, results : list[list[tuple]]) -> list[tuple]:
        compiled_results = []
        different_words_number = len(results)
        for book_1 in results[0]:
            book_1_id = book_1[0]
            occurence_count = 1
            positions = [book_1[1]]
            for word in results[1:]:
                for book_2 in word:
                    book_2_id = book_2[0]
                    if book_2_id == book_1_id:
                        occurence_count += 1
                        positions.append(book_2[1])
                        break
            if occurence_count == different_words_number:
                compiled_results.append((book_1_id, positions))
        return compiled_results

    def load_metadata_from_file(self, file_path):
        self.metadata = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                entry = ast.literal_eval(line.strip())
                self.metadata.append(entry)

    def filter_with_metadata(self, field: Field, value: str, results: list) -> list:
        """
        for now we just check if the field contains the value
        but the field can contain more than just the value
        so we can also look with part of the title, or only name/surname of author
        """
        if not self.metadata:
            metadata_file_name = "gutenberg_data.txt"
            metadata_file_path = os.path.join(self.script_dir, metadata_file_name)
            self.load_metadata_from_file(metadata_file_path)

        filtered_results = []
        for r in results:
            book_id = r[0]
            for book in self.metadata:
                if int(book["ID"]) == int(book_id):
                    if value.lower() in book[field.value].lower():
                        filtered_results.append(r)
                    break
        return filtered_results

    def get_part_of_book_with_word(self, book_id: int, word_id: int) -> tuple[str, int]:
        file_relative_path = "gutenberg_books/" + str(book_id) + "_.txt"
        file_path = os.path.join(self.script_dir, file_relative_path)
        with open(file_path, "r", encoding="utf-8") as file:
            curr_pos = 0
            while True:
                line = file.readline()
                if not line:
                    break
                line = line.split()
                curr_pos += len(line)
                if curr_pos > word_id:
                    position = word_id - curr_pos
                    return " ".join(line), position

    def print_coloured(self, line_list: list, position: int) -> str:
        GREEN = "\33[32m"
        RESET = "\033[0m"
        word = line_list[position]
        line_list[position] = f"{GREEN}{line_list[position]}{RESET}"
        print(" ".join(line_list))
        return word
