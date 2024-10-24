# life_cycle_processor.py
import pandas as pd
import numpy as np
from work_calendar import WorkCalendar

class LifeCycleProcessor:
    def __init__(self, timezone='Europe/Moscow'):
        self.timezone = timezone
        self.calendar = WorkCalendar(timezone)

    def process_life_cycle_data(self, df):
        """Обрабатывает данные жизненного цикла."""
        print("Запускаем обработку файла...")
        life_cycle_df = df.copy()

        # Преобразуем 'ChangedDate' в datetime и локализуем в московское время
        life_cycle_df['ChangedDate'] = pd.to_datetime(life_cycle_df['ChangedDate'], format='%Y-%m-%d %H:%M:%S')
        life_cycle_df['ChangedDate'] = life_cycle_df['ChangedDate'].dt.tz_localize(self.timezone, nonexistent='shift_forward')

        # Сортируем по ID и дате
        life_cycle_df = life_cycle_df.sort_values(by=['ID', 'ChangedDate'])

        # Добавляем следующий ChangedDate и State
        life_cycle_df['nextChangedDate'] = life_cycle_df.groupby('ID')['ChangedDate'].shift(-1)
        life_cycle_df['nextChangedDate'] = life_cycle_df['nextChangedDate'].fillna(pd.Timestamp.now(tz=self.timezone))

        # Рассчитываем рабочие минуты между 'ChangedDate' и 'nextChangedDate'
        life_cycle_df['working_minutes'] = life_cycle_df.apply(
            lambda row: self.calculate_working_minutes(row['ChangedDate'], row['nextChangedDate']), axis=1)

        # Округляем рабочие минуты и приводим к целому числу
        life_cycle_df['working_minutes'] = life_cycle_df['working_minutes'].round(0).astype(int)

        # Убираем временную зону, делая даты "наивными"
        life_cycle_df['ChangedDate'] = life_cycle_df['ChangedDate'].dt.tz_localize(None)
        life_cycle_df['nextChangedDate'] = life_cycle_df['nextChangedDate'].dt.tz_localize(None)

        # Преобразуем nextChangedDate в строковый формат для отображения
        life_cycle_df['nextChangedDate'] = life_cycle_df['nextChangedDate'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Заполняем NaN для nextState
        life_cycle_df['nextState'] = life_cycle_df.groupby('ID')['State'].shift(-1)
        life_cycle_df['nextState'] = life_cycle_df['nextState'].fillna(life_cycle_df['State'])

        print("Первичная обработка завершена")
        return life_cycle_df

    def calculate_working_minutes(self, start_time, end_time):
        """Рассчитывает рабочие минуты между двумя датами."""
        total_minutes = 0
        current_time = start_time

        while current_time < end_time:
            if self.calendar.is_working_day(current_time):
                work_start, work_end = self.calendar.get_working_hours(current_time)
                if current_time < work_start:
                    current_time = work_start
                if current_time < work_end:
                    end_of_day = min(work_end, end_time)
                    total_minutes += (end_of_day - current_time).total_seconds() / 60
                    current_time = end_of_day
            current_time += pd.Timedelta(days=1)
            current_time = current_time.replace(hour=0, minute=0, second=0)

        return total_minutes

    def calculate_transitions_and_rollback(self, life_cycle_df, df_roll):
        """Рассчитывает общее число переходов и проверяет совпадение с ...."""
        # Подсчет общего числа переходов из '' в ''
        total_transitions = life_cycle_df.groupby('ID').apply(self.count_transitions).sum()
        
        # Суммируем столбец '...' из второго DataFrame
        rollback = df_roll['...'].sum()
        
        # Проверка на совпадение сумм
        if total_transitions == total_rollback:
            print("Расчёт корректен")
        else:
            print("Расчёт не совпадает")
        
        # Возвращаем результат в виде словаря с заголовками
        return {
            'Общая сумма переходов': total_transitions,
            'Общая сумма Rollback': total_rollback
        }

    def count_transitions(self, group):
        """Подсчитывает переходы из '...' в '...'."""
        transitions = 0
        for i in range(len(group) - 1):
            if group.iloc[i]['...'] == '...' and group.iloc[i + 1]['...'] == '...':
                transitions += 1
        return transitions

    def calculate_status_duration_with_filter(self, column, status, df, apply_filter=False, col_time=''):
        """Фильтрует данные по указанному столбцу и статусу, применяет дополнительный фильтр по совпадению аналитика и исполнителя,
        и затем суммирует рабочее время."""
        # Фильтруем по указанному столбцу и статусу
        filtered_df = df[df[column] == status]
        # Применяем фильтр по совпадению ... и ..., если apply_filter == True
        if apply_filter:
            filtered_df = filtered_df[filtered_df['...'] == filtered_df['...']]
        
        # Если есть совпадающие ID, применяем summarize_working_time
        if not filtered_df.empty:
            filtered_df = self.summarize_working_time(filtered_df)
            filtered_df['working_time'] = filtered_df['working_minutes'].apply(self.minutes_to_ddhhmm)
            
            # Переименовываем столбцы с подстановкой значений column и status
            filtered_df = filtered_df.rename(columns={
                'working_minutes': col_time + ', mm', 
                'working_time': col_time + ', ddhhmm'
            })
        
        return filtered_df

    def summarize_working_time(self, df):
        """Суммирует рабочее время для каждого ID."""
        return df.groupby('ID').agg({
            'working_minutes': 'sum'
        }).reset_index()

    def minutes_to_ddhhmm(self, minutes):
        """Преобразует минуты в формат ddhhmm."""
        days = minutes // (24 * 60)
        hours = (minutes % (24 * 60)) // 60
        mins = minutes % 60
        return f"{days}d{hours}h{mins}m"