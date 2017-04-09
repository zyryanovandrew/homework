import re
def preproc():
    with open('text.txt', 'r', encoding = 'utf-8') as f:
        text = f.read()
        allsent = re.split(r'[\.\?\!]', text)
        allsent = [sent.lower() for sent in allsent]
        allsent = [re.sub(r'[,—“\':”\(\)]', '', sent) for sent in allsent]
    return allsent

def count(sent):
    num = {word : sent.count(word) for word in sent}
    several = {word : num[word] for word in num if num[word]>1}
    if several == {}:
        several = {'Повторяющихся слов' : '0'}
    return several

def display(several):
    print('Следующее предложение: ')
    template = '{:^10} {:^10}'
    for keyword in several:
        print(template.format(keyword, several[keyword]))

allsent = preproc()
for sentence in allsent:
    arr = re.split(r' ', sentence)
    several = count(arr)
    display(several)
