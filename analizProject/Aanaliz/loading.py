# Модуль 'loading'. Загрузка DataFrame
from tkinter import *
from tkinter import ttk
import pandas as pd

def on_enter(event):  # ввод пути и имени файла
    global data
    path = entry_path.get()  # путь к файлу
    name = entry_file.get()  # имя файла
    # Объединяем путь и имя файла
    patch = path + '\\' + name
    if patch:  # Проверяем, что текст введен
        try:
            simvol = name[-1]  # Последний символ имени файла
            if simvol == 'v':  # файл csv
                data = pd.read_csv(patch)
            elif simvol == 'x':  # файл xlsx
                data = pd.read_excel(patch)
                patch_csv = patch.replace("xlsx", "csv")  # Замена расширения
                data.to_csv(patch_csv, index=False)
            else:
                label = Label(root, text='Ошибка при вводе пути или имени файла', bg='yellow')
                label.pack(anchor=NW)

            # Если фрейм успешно загружен, проверяем наличие данных
            df = pd.DataFrame(data)
            if df.empty:
                label = Label(root, text='Датафрейм пуст', bg='yellow')
                label.pack(anchor=NW)
            else:
                df.to_csv('data.csv', index=False)  # Сохраняем файл в файл data.csv
                label = Label(root, text='Файл успешно загружен', bg='DarkSlateGray2')
                label.pack(anchor=NW)
                return df
        except Exception as e:
            label = Label(root, text=f'{e}', bg='yellow')
            label.pack(anchor=NW)

# def set_style():  # Установка стилей виджетов
#     style = ttk.Style()
#     style.configure('TLabel', font=('Calibri', 12), bg='DarkSlateGray2')
#     style.configure('TEntry', font=('Calibri', 12), bg='DarkSlateGray2')
def create_label(text, color='DarkSlateGray2'):  # параметры виджетов
    return Label(root, text=text, bg=color, font=('Calibri', 12))

# Создание окна
root = Tk()
root.geometry(f'500x200')
root.title("Загрузка данных")
root.iconbitmap("calculator.ico")
root.eval('tk::PlaceWindow . center')  # центрирование окна
root.config(bg='DarkSlateGray2')  # Цвет фона

label = create_label ("Возможна загрузка файлов типа 'csv' и 'xlsx'")
label.pack(anchor=NW, pady=(0, 10) )

# Ввод пути к файлу
label_path = create_label("Вставьте (Ctrl_V) или введите путь к файлу в виде: Диск:\путь\к\файлу")
label_path.pack(anchor=NW, pady=(0, 10))
entry_path = ttk.Entry(root, width=100)
entry_path.pack(anchor=NW, padx=8, pady=(0, 10))

# Ввод имени файла
label_file = create_label("Вставьте или введите имя файла с расширением")
label_file.pack(anchor=NW)
entry_file = ttk.Entry(root, width=100)
entry_file.pack(anchor=NW, padx=8)

# Привязка обработчика к событию нажатия клавиши Enter
entry_file.bind('<Return>', on_enter)

root.mainloop()
