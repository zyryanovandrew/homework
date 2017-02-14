import re
def opencount():
    with open('corp.xml', 'r', encoding = 'utf-8') as f:
        text = f.readlines()
        c = 0
        for line in text:
            line.strip('\s')
            if '</teiHeader>' not in line:
                c += 1
            else:
                break
        numheader = str(c) + '\n'
    return numheader, text 

def create_dict(text):
    newdict = {}
    typearr = []
    allmorphs = []
    for line in text:
        if '<w' in line:
            morph = line.split('type="')
            typeraw = morph[1]
            morph1 = typeraw.split('">')
            allmorphs.append(morph1[0])
    keys = []
    for el in allmorphs:
        if el not in keys:
            keys.append(el)
    for key in keys:
        num = allmorphs.count(key)
        newdict[key] = num
    return newdict


def writenum(c, newdict, neutrum, csvarr):
    with open('result.txt', 'w', encoding = 'utf-8') as f:
        f.write(c)
        for key, freq in newdict.items():
            string = str(key) + ':' + str(freq) + '\n'
            f.write(string)
        line = ''
        for el in neutrum:
            line += el + ', '
        line += '\n'
        f.write(line)
        for el in csvarr:
            f.write(el)
        print('Записано.')

def search_pro_n(text):
    neutrum = []
    for line in text:
        q = re.search('type="f.h', line)
        if q != None:
            form1 = line.split('">')
            form2 = form1[1].split('</')
            neutrum.append(form2[0])
    return neutrum

def wholecorpora():
    csvarr = []
    with open('corp.xml', 'r', encoding = 'utf-8') as f:
        text = f.read()
        arr = text.split('<body>')
        arr1 = arr[1].split('</body>')
        arrlines = arr1[0].split('\n')
        for line in arrlines:
            if '<w' in line:
                line = re.sub('<w lemma="', '', line)
                line = re.sub('" type="', ', ', line)
                line = re.sub('">', ', ', line)
                line = re.sub('</w>', '\n', line)
                csvarr.append(line)
    return csvarr

c, text = opencount()
newdict = create_dict(text)
neutrum = search_pro_n(text)
csvarr = wholecorpora()
writenum(c, newdict, neutrum, csvarr)
