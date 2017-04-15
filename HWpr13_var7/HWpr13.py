import os
import shutil
import re

def countfolders():
    obj = os.listdir()
    folders = [el for el in obj if os.path.isdir(el)]
    result = []
    for folder in folders:
        if r'[a-z]|[A-Z]' and r'[а-яё]|[А-ЯЁ]' in folder:
            result.append(folder)
            print(folder)
    print('Всего папок, удовлетворяющих условию:', len(result))

countfolders()
