def opentext (title):
    with open(title, 'r', encoding='utf-8') as f:
        text = f.read()
        arr = []
        arr = text.split()
        for elem in arr:
            elem.lower()
            elem.strip('!-./?"", ')
    return arr

def firstletter(letter, arr):
    wordsarr = []
    for elem in arr:
        if letter == elem[0:2]:
            wordsarr.append(elem)
    return wordsarr

def questions():
    file_name = input('Введите путь к файлу: ')
    minlen = int(input('Введите минимальную длину слова: '))
    arr = opentext(file_name)
    un_words = firstletter('un', arr)
    return minlen, un_words

def count(minlen, un_words):
    wordslen = []
    n = 0
    for elem in un_words:
        for letter in elem:
            n += 1
        if n > minlen:
            wordslen.append(elem)
        n = 0
    print('Количество слов, начинающихся с un:', len(un_words))
    print('Процент слов длинее', minlen, ':', len(wordslen)/len(un_words)*100)

minlen, un_words = questions()
count(minlen, un_words)                
