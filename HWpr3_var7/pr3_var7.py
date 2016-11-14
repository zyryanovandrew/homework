arr = []
arr1 = []
i = 0
print('Пожалуйста, введите 8 слов')
while i != 8:
    word = input()
    arr.append(word)
    i += 1
i = 0
while i <= 6:
    pair = arr[i] + arr[i+1]
    arr1.append(pair)
    i += 2
for el in arr1:
    print (el)
