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
            raise ValueError('There are no available indexers with this name.')
        
    def load_metadata_from_file(self, file_path):
        self.metadata = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                entry = ast.literal_eval(line.strip())
                self.metadata.append(entry)

    def filter_with_metadata(
        self, field: Field, value: str, results: list[tuple[int, list]]
    ) -> list[tuple[int, list]]:
        """
        for now we just check if the field contains the value
        @TODO
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
                if int(book["ID"]) == book_id:
                    if book[field.value] == value:
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


if __name__ == "__main__":
    query_engine = QueryEngine()
    res = query_engine.search('clock', Indexer.HASHED)
    field = Field.LANGUAGE
    fil_res = query_engine.filter_with_metadata(field, 'Gibberish', res)
    print(len(res))
    print(res)
    print(fil_res)
    # word = ""
    # ind = 0
    # while ind < 50:
    #     line, pos = query_engine.get_part_of_book_with_word(84, ind)
    #     print(ind, end="\t")
    #     word = query_engine.print_coloured(line.split(), pos)
    #     ind += 1
    # ind = 7613
    # line, pos = query_engine.get_part_of_book_with_word(84, 10000)
    # print(ind, end="\t")
    # query_engine.print_coloured(line.split(), pos)
