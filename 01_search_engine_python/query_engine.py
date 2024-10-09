import json
import ast


class QueryEngine:
    def load_inverted_index_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            self.inverted_index = json.load(file)

    def load_metadata_from_file(self, file_path):
        self.metadata = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                entry = ast.literal_eval(line.strip())
                self.metadata.append(entry)

    def get_indexes_of_books_with(self, word: str) -> list:
        word = word.lower()
        if word in self.inverted_index:
            return self.inverted_index[word]
        else:
            return f"'{word}' not found in the index."

    def get_indexes_of_books_with_metadata(self, field, value) -> list:
        results = [
            entry["ID"]
            for entry in self.metadata
            if entry[field].lower() == value.lower()
        ]
        if results:
            return results
        else:
            return f'No matches found for {value} in {field}'


if __name__ == "__main__":
    query_engine = QueryEngine()
    query_engine.load_inverted_index_from_file('inverted_index.json')
    query_engine.load_metadata_from_file('gutenberg_data.txt')
    word = 'word'
    result = query_engine.get_indexes_of_books_with(word)
    print(f"Documents containing '{word}': {result}")
    field, value = ('author', 'Elizabeth Cleghorn Gaskell')
    result = query_engine.get_indexes_of_books_with_metadata(field, value)
    print(result)
