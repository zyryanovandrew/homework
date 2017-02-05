import re
def search():
    with open('chuvash.html', 'r', encoding = 'utf-8') as f:
        source = f.read()
        search_arr = source.split('<a')
        for el in search_arr:
            match = re.search('.*iso639\-3\/documentation\.asp\?id\=.*', el)
            if match != None:
                el = re.split('id\=...\">', el)
                codearr = re.split('</a>', el[1])
                result = codearr[0]
    return result
                
def record(result):
    with open('blank.txt', 'w', encoding = 'utf-8') as f:
        f.write(result)
        f.close()
        print('Трехбуквенный код языка записан в файл blank.txt')

result = search()
record(result)
