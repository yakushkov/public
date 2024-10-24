# csv_loader.py
import os
import re
import pandas as pd

class CSVLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_csv_file(self, file_name):
        """Загружает CSV-файл в DataFrame."""
        file_path = os.path.join(self.folder_path, file_name)
        df = pd.read_csv(file_path, sep=';')
        print(f"Loaded file: {file_name}")
        return df

    def find_files_by_pattern(self, pattern):
        """Находит файлы в папке по заданному шаблону."""
        files = [f for f in os.listdir(self.folder_path) if re.match(pattern, f)]
        print(f"Found files by pattern: {files}")
        return files