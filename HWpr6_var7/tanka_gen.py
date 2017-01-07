import random

def adj():
    adj_arr = []
    contadj = open('esenin_adj_pl.txt', 'r', encoding='utf-8')
    for line in contadj:
        line_lc = line.capitalize().strip()
        adj_arr.append(line_lc)
    contadj.close()
    return random.choice(adj_arr)

def noun():
    noun = []
    contnoun = open('spi_noun_pl.txt', 'r', encoding='utf-8')
    for line in contnoun:
        line_lc = line.lower().strip()
        noun.append(line_lc)
    contnoun.close()
    return random.choice(noun)

def verb():
    verbs = []
    contverbs = open('majakovsky_verbs.txt', 'r', encoding='utf-8')
    for line in contverbs:
        line_lc = line.capitalize().strip()
        verbs.append(line_lc)
    contverbs.close()
    return random.choice(verbs)

def adv():
    adv = []
    contadverb = open('pushkin_adverbs.txt', 'r', encoding='utf-8')
    for line in contadverb:
        line_lc = line.lower().strip()
        adv.append(line_lc)
    contadverb.close()
    return random.choice(adv)

def prop():
    prop = []
    contprop = open('properties.txt', 'r', encoding='utf-8')
    for line in contprop:
        line_lc = line.lower().strip()
        prop.append(line_lc)
    contprop.close()
    return random.choice(prop)


def line1():
    syll = 0
    while syll != 5:
        syll = 0
        first = adj() + ' ' + noun()
        for letter in first:
            if letter in 'АЕЁИОУЫЭЮЯаеёиоуыэюя':
                syll += 1
    return first

def line2():
    syll = 0
    while syll != 7:
        syll = 0
        second = verb() + ' ' + adv() + ' ' + adv() + random.choice(['!','?','.','...'])
        for letter in second:
            if letter in 'АЕЁИОУЫЭЮЯаеёиоуыэюя':
                syll += 1
    return second

def line4():
    syll = 0
    while syll != 7:
        syll = 0
        fourth = verb() + ' ' + adv() + random.choice(['!','?','.','...'])
        for letter in fourth:
            if letter in 'АЕЁИОУЫЭЮЯаеёиоуыэюя':
                syll += 1
    return fourth

def line5():
    syll = 0
    person=['Я','Ты']
    while syll != 7:
        syll = 0
        fifth = random.choice(person) + ' ' + prop() + ' ' + adv() + random.choice(['!','?','.','...'])
        for letter in fifth:
            if letter in 'АЕЁИОУЫЭЮЯаеёиоуыэюя':
                syll += 1
    return fifth
    
print(line1())
print(line2())
print(line1())
print(line4())
print(line5())




