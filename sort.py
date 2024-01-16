import os
import shutil
import time
import json
import tkinter as tk
from tkinter import filedialog
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading

def create_image(path):
    # Load an image file
    image = Image.open(path)
    return image

def exit_action(icon, item):
    icon.stop()

def run_icon(icon):
    icon.run()

# Замените 'path_to_your_icon.png' на путь к вашему файлу иконки
image_path = 'icon.png'
image = create_image(image_path)
menu = (item('Exit', exit_action),)
icon = pystray.Icon("name", image, "sort by rubik", menu)

# Запускаем иконку в отдельном потоке
threading.Thread(target=run_icon, args=(icon,)).start()

# Определите расширения для каждой категории
extensions = {
    'аудио': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'],
    'видео': ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.m4v', '.webm', '.vob', '.ogv', '.qt', '.yuv', '.rm', '.asf', '.amv', '.mpg', '.mpeg', '.m2v'],
    'фотки': ['.jpg', '.jpeg', '.png', '.gif', '.ico', '.tiff', '.bmp', '.svg', '.webp', '.heif', '.bat', '.indd', '.ai', '.eps', '.pdf', '.psd', '.cdr'],
    'документы': ['.doc', '.docx', '.pdf', '.txt', '.ppt', '.pptx', '.xls', '.xlsx', '.csv', '.md', '.odt', '.ods', '.odp', '.odg', '.odf'],
    'образы': ['.iso', '.img', '.vcd'],
    'программы': ['.exe', '.msi', '.jar', '.bat', '.sh', '.py', '.js', '.html', '.css', '.php', '.apk', '.deb', '.pkg', '.rpm'],
    'торренты': ['.torrent'],
    'архивы': ['.rar', '.zip', '.7z', '.tar', '.gz', '.bz2', '.lz', '.z', '.xz'],
    'файлы данных': ['.xml', '.json', '.csv', '.dat', '.db', '.log', '.sql', '.ini', '.dbf', '.mdb', '.sav', '.tar', '.xml', '.kml', '.gpx'],
    'файлы кода': ['.c', '.cpp', '.h', '.java', '.py', '.js', '.html', '.css', '.php', '.go', '.rs', '.swift', '.kt', '.m', '.mm', '.cs', '.fs', '.vb', '.lua', '.asm', '.sh', '.bat', '.pl', '.rb', '.yml', '.json', '.xml', '.sql', '.sln', '.pro', '.makefile', '.r', '.groovy', '.ps1'],
#    'шрифты': ['.ttf', '.otf', '.fon', '.fnt', '.woff', '.woff2', '.eot', '.svg'],
    'апк': ['.apk', '.xapk', '.apks', '.aab'],
    'для кастома': ['.rmskin', '.themepack', '.deskthemepack'],
#    '3D файлы': ['.3ds', '.obj', '.fbx', '.dae', '.max', '.c4d', '.blend', '.ma', '.mb', '.lwo', '.lws', '.lxo', '.stl', '.xsi', '.x', '.dwg', '.skp', '.scad'],
#   'векторные': ['.eps', '.ai', '.sk', '.sk1', '.svg'],
#    'электронные книги': ['.epub', '.mobi', '.azw3', '.pdf', '.lit', '.pdb', '.fb2', '.xeb', '.ceb', '.inf', '.pdg', '.xml', '.tcg', '.azw', '.azw4', '.azw1', '.azw2', '.txt'],
    'диск образы': ['.iso', '.bin', '.img', '.nrg', '.cdi', '.b6i', '.b5i', '.pdi', '.isz', '.ccd', '.sub', '.img', '.dmg', '.toast', '.vcd', '.cif', '.nri', '.gi', '.daa', '.uif', '.dmg', '.ashdisc', '.bwt', '.bwi', '.b5t', '.lcd', '.img', '.cdi', '.c2d', '.p01', '.mds', '.mdx', '.ape', '.flac', '.wav', '.mp3'],
#    'другие': ['.yuv', '.csv', '.dat', '.f4v', '.h264', '.jpeg', '.m4v', '.3g2', '.3gp', '.mkv', '.mod', '.mpg', '.rm', '.rmvb', '.srt', '.swf', '.vob', '.wmv']
}



def sort_files(directory):
    for category, exts in extensions.items():
        # Создать папку для категории, если она еще не существует
        cat_dir = os.path.join(directory, category)
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)

        for file in os.listdir(directory):
            # Если это файл и его расширение соответствует категории, переместите его
            if os.path.isfile(os.path.join(directory, file)):
                file_ext = os.path.splitext(file)[1]
                if file_ext in exts:
                    shutil.move(os.path.join(directory, file), os.path.join(cat_dir, file))
            
# Путь к файлу, в котором будет храниться путь к директории
path_file = 'path.json'

if os.path.isfile(path_file):
    # Если файл уже существует, загрузите путь из него
    with open(path_file, 'r') as f:
        directory = json.load(f)
else:
    # Если файла нет, покажите окно выбора директории и сохраните выбранный путь в файле
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    directory = filedialog.askdirectory()  # Открываем диалог выбора директории
    with open(path_file, 'w') as f:
        json.dump(directory, f)


# Бесконечный цикл, который выполняет функцию sort_files каждые 20 секунд
while True:
    sort_files(directory)
    time.sleep(20)  # Пауза в 20 секунд
