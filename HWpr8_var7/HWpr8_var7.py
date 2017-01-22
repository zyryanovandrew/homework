import random 
def create_dict():
    with open('db.txt', 'r', encoding = 'utf-8') as f:
        db = f.read()
        phrases = db.split('\n')
    clues = dict()
    keys = []
    phrase_split = []
    for phrase in phrases:
        phrase_split = phrase.split()
        clues[phrase_split[len(phrase_split) - 1]] = phrase_split[0:len(phrase_split) - 1]
        keys.append(phrase_split[len(phrase_split) - 1])
    return clues, keys

def show(clues, keys, shown):
    key = random.choice(keys)
    while key in shown:
        key = random.choice(keys)    
    clue_arr = clues[key]
    for el in clue_arr:
        print(el, end = ' ')
    guess = input()
    if guess.lower() == key:
        check = True
    else:
        check = False
    return check, key

def result(check):
    congrats = ['Поздравляю!', 'horoshego dnya!', 'Угадали!', 'Верно!', 'Хорошо сработано!']
    condolences = ['Попробуйте еще раз!', 'Не отчаивайтесь, продолжайте!', 'Почти в точку... у вас есть еще попытка!', 'nichego, zavtra otgadaete!', 'escho chut-chut...']
    if check == True:
        print(random.choice(congrats))
    else:
        print(random.choice(condolences))

def run():
    shown = []
    for i in range (10):
        clues, keys = create_dict()
        check, key = show(clues, keys, shown)
        result(check)
        if check == True:
            shown.append(key)


run()
print('Всего доброго!')
    
    
