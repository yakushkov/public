# main.py
from csv_loader import CSVLoader
from life_cycle_processor import LifeCycleProcessor
import pandas as pd
import re

# Заданные области
specified_areas = [
    r'Tele2....
]


def check_date(df):
    """Проверяет, что все элементы в столбце 'Created Date' меньше '2024-01-09 00:00'."""
    df = df[df['Created Date'] < '2024-01-09 00:00']
    return len(df)

def check_area(df, areas):
    """Проверяет, что все элементы в столбце 'Areapath' находятся в заданных областях."""
    incorrect_areas_df = df[~df['Areapath'].isin(specified_areas)]
    return incorrect_areas_df['Areapath'].unique()

def check_uniqueness(df, column_name):
    """Проверяет уникальность столбца 'ID'."""
    if df[column_name].is_unique:
        return True
    else:
        return False

def extract_base_name(col):
    """Извлекает базовое имя столбца без суффиксов 'mm' и 'Minutes'."""
    return re.sub(r'(, mm| Minutes)$', '', col)


def main():
    
    folder_path = './csv'
    loader = CSVLoader(folder_path)
    processor = LifeCycleProcessor()

    # Находим файлы по шаблону
    file_pattern = r'....csv'
    files = loader.find_files_by_pattern(file_pattern)

    # Обрабатываем каждый файл
    for file_name in files:
        df = loader.load_csv_file(file_name)
        processed_df = processor.process_life_cycle_data(df)
        print(f"Processed file: {file_name}")

        # Проверка областей
        incorrect_areas = check_area(processed_df, specified_areas)
        if len(incorrect_areas) > 0:
            print(f"Найдены другие области в файле {file_name}: {incorrect_areas}")
        else:
            print(f"Области корректные в файле")

        # Загружаем второй df
        df_roll_pattern = r'...csv'
        df_roll_files = loader.find_files_by_pattern(df_roll_pattern)

        if len(df_roll_files) > 0:
            df_roll_name = df_roll_files[0]
            df_roll = loader.load_csv_file(df_roll_name)

            # Проверка дат в df_roll
            if check_date(df_roll) > 0:
                print(f"Найдены элементы, созданные ранее 2024-01-09")
            else:
                print(f"Условие по созданию элемента выполняются (позднее 2024-01-09)'")

            # Рассчитываем переходы и проверяем совпадение с колонкой
            processor.calculate_transitions_and_rollback(processed_df, df_roll)

            # Рассчитываем статусную длительность с фильтром
            df_new_state = processor.calculate_status_duration_with_filter('State', 'New', processed_df, apply_filter=False, col_time='...')
            ...
            # Список новых DataFrame, созданных с помощью calculate_status_duration_with_filter
            dataframes = [
                df_new_state,
                ...
            ]

            # Проверка уникальности столбца 'ID' во всех датафреймах
            column_to_check = 'ID'
            for i, df in enumerate(dataframes):
                if not check_uniqueness(df, column_to_check):
                    raise ValueError(f"В DataFrame {i+1} найдены неуникальные значения в столбце '{column_to_check}'")

            # Объединяем все датафреймы по 'ID'
            df_combined = dataframes[0]
            for df in dataframes[1:]:
                df_combined = df_combined.merge(df, on='ID', how='outer')

            # Проверяем наличие столбцов 'ID' или 'Id' в обоих датафреймах
            if 'ID' in df_combined.columns and 'Id' in df_roll.columns:
                # Преобразуем названия столбцов для корректного объединения
                df_combined = df_combined.rename(columns={'ID': 'Id'})  # Переименуем 'ID' в 'Id'
                
                # Объединяем df_combined и df_roll по столбцу 'Id'
                df_final_combined = df_combined.merge(df_roll, on='Id', how='outer')
                
                # Сравниваем столбцы 'mm' и 'minutes'
                columns_mm = [col for col in df_final_combined.columns if col.endswith('mm') and 'ddhhmm' not in col]

                for col_mm in columns_mm:
                    base_name = extract_base_name(col_mm)
                    col_minutes = f"{base_name} Minutes"
                    if col_minutes in df_final_combined.columns:
                        # Вычисляем числовую разницу между столбцами
                        df_final_combined[f'Difference {col_mm} vs {col_minutes}'] = df_final_combined.apply(
                            lambda row: row[col_mm] - row[col_minutes] if pd.notna(row[col_mm]) and pd.notna(row[col_minutes]) else None,
                            axis=1
                        )

                # Сохраняем результат в Excel
                df_final_combined.to_excel('final_comparison_difference_mm_minutes.xlsx', index=False)
                print("Файл с VAR создан")

                # Создаем DataFrame только с разницей
                difference_columns = [col for col in df_final_combined.columns if col.startswith('Difference')]
                df_difference_only = df_final_combined[['Id'] + difference_columns]

                # Сохраняем DataFrame с разницей в Excel
                df_difference_only.to_excel('final_comparison_difference_only.xlsx', index=False)

            else:
                print("Столбец 'Id' отсутствует в одном из датафреймов")

        else:
            print(f"No matching file found for pattern: {df_roll_pattern}")

if __name__ == "__main__":
    main()