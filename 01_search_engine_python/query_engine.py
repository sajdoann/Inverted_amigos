import json
import ast
import os


class QueryEngine:
    def get_indexes_of_books_with_metadata(self, field, value) -> list:
        results = [
            entry["ID"]
            for entry in self.metadata
            if entry[field].lower() == value.lower()
        ]
        if results:
            return results
        
    def get_part_of_book_with_word(self, book_id: int, word_id: int) -> tuple[str, int]:
        script_dir = os.path.dirname(__file__)
        file_relative_path = "gutenberg_books/"+str(book_id) + "_.txt"
        file_path = os.path.join(script_dir, file_relative_path)
        with open(file_path, "r", encoding='utf-8') as file:
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
    word = ''
    ind = 0
    while ind < 50:
        line, pos = query_engine.get_part_of_book_with_word(84, ind)
        print(ind, end="\t")
        word = query_engine.print_coloured(line.split(), pos)
        ind += 1
    # ind = 7613
    # line, pos = query_engine.get_part_of_book_with_word(84, 10000)
    # print(ind, end="\t")
    # query_engine.print_coloured(line.split(), pos)
