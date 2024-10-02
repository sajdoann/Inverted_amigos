import pandas as pd


def txt_to_parquet(txt_file_path, parquet_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    df = pd.DataFrame({'content': lines})

    df.to_parquet(parquet_file_path, index=False)


txt_file_path = 'gutenberg_books/1_Frankenstein; Or, The Modern Prometheus.txt'
parquet_file_path = 'gutenberg_books'
txt_to_parquet(txt_file_path, parquet_file_path)
