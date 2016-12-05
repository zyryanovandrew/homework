text = open('exomars.txt','r',encoding='utf-8')
arr = []
countline = 0 ## кол-во строк длиной больше 5
countall = 0 ## кол-во всех строк
symb = 0 ## кол-во тире
for line in text:
    countall += 1
    arr = line.split( )
    for el in arr:
        if el == '—':
            symb += 1
    countwords = len(arr) - symb
    if countwords > 5:
        countline += 1
text.close()
print('Всего строк:', countall,'Строк с числом слов больше 5:', countline, 'Процент:', round(countline*100/countall), '%')
