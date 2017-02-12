import re
def change():
    with open('aves.txt', 'r', encoding = 'utf-8') as f:
        text = f.read()
        text = re.sub(r'\bптице.\b', r'рыбо.', text)
        text = re.sub(r'\bПтице.\b', r'Рыбо.', text)
        text = re.sub(r'\bптиц', r'\bрыб', text)
        text = re.sub(r'\bПтиц', r'\bРыб', text)
    with open('fish.txt', 'w', encoding = 'utf-8') as f:
        f.write(text)
        print('Текст записан в файл fish.txt')

change()
