print('Введите три числа')
a,b,c=float(input()), float(input()), float(input())
div=a/b
deg=a**b
if div==c:
    print ('Результат деления А на B равен С')
else:
    print ('Результат деления А на B НЕ равен С')
if deg==c:
    print ('А в степени B равно С')
else:
    print ('А в степени B НЕ равно С')
