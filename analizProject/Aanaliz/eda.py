# Модуль для разведывательного анализа DataFrames
import sweetviz as sv
import pandas as pd

try:
    df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)

# генерация отчета
report = sv.analyze(df)

#Вывод отчета в браузер
report.show_html('Разведывательный анализ data.html')