import os
def mostfiles():
    number = {root : len(files) for root, dirs, files in os.walk('.')}
    c = 0
    folder = ''
    for root in number:
        if number[root] > c:
            c = number[root]
            folder = root
    print('Количество файлов в папке по адресу', folder, ':', c)

mostfiles()
    
