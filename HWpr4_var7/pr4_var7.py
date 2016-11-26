w=input('Введите слово: ')
while w == '':
    w=input('Попробуйте еще раз: ')
border = 1
for i in range (len(w) // 2):
    print (w[border:len(w) - border])
    border += 1
