import urllib.request
import re
import os
import shutil
import time

cleanTag = re.compile('<.*?>\t*?', re.DOTALL)
cleanNewLine = re.compile('\n', re.DOTALL)
cleanProbel = re.compile('	', re.DOTALL)
## clean1-5 - регулярки для очистки строк в базе данных материалов
clean1 = re.compile('<h2>.*?<a href=\"', re.DOTALL) ## почистить еще от кавычек, процентов и тд
clean2 = re.compile('">', re.DOTALL)
clean3 = re.compile('<\/a>.*?<\/h2>', re.DOTALL)
clean4 = re.compile('<dd.*?Опубликовано ', re.DOTALL)
clean5 = re.compile(' *?[0-9][0-9]:[0-9][0-9].*?</dd>', re.DOTALL)
##регулярки для перевода исходного кода в plain text
findPar = re.compile('<div class=\"item-page\">.*?jlvkcomments.*?>', re.DOTALL)
cleanMeta = re.compile('.*?Social Like', re.DOTALL)
##регулярки для удаления не ascii символов
notSlash = re.compile('/', re.DOTALL)
notWeirdLines = re.compile('\\n', re.DOTALL)
notASCII1 = re.compile('&nbsp;', re.DOTALL)
notBackSlashT = re.compile('\\t', re.DOTALL)
notASCII2 = re.compile('&quot;', re.DOTALL)
##регулярки для базы данных
regItem = re.compile('<div class=\"leading-.\">.*?<\/dd>', re.DOTALL)
regUrlName = re.compile('<h2>.*?</h2>', re.DOTALL)
regDate = re.compile('<dd class="published">.*?</dd>', re.DOTALL)
##регулярка для создания путей в майстеме
regMystem = re.compile('plain', re.DOTALL)

def create_database(folder): ##создаем csv-файл, содержащий: 1) ссылку на каждую статью 2) название статьи 3) дату публикации
    if folder == 'novosti':
        v = 1101
    if folder == 'stati':
        v = 761
    for page_num in range (0,v,10): ## поменять на v. для тестирования вместо v написано 11
        try:
            time.sleep(2)
            req = urllib.request.Request('http://noviput.info/' + folder + '?start=' + str(page_num))
            print(page_num)
            with urllib.request.urlopen(req) as response:
               page_code = response.read().decode('utf-8')
               UrlName = regUrlName.findall(page_code)
               Date = regDate.findall(page_code)
            with open('database.csv', 'a', encoding = 'utf-8') as result: ##поменять w на а, чтобы не переписывать файл, а добавлять строки в конец
                for n in range(0,10):
                    cleanUrlName, cleanDate = clean_database(UrlName[n], Date[n])
                    result.write(cleanUrlName + '   ' + cleanDate + '\n')
            UrlName.clear()
            Date.clear()
        except:
            print('No such page')
            
def clean_database(UrlName, Date): ## чистим базу данных
    cleanUrlName = cleanProbel.sub('', UrlName)
    cleanUrlName = clean1.sub('', cleanUrlName)
    cleanUrlName = clean2.sub('', cleanUrlName)
    cleanUrlName = clean3.sub('', cleanUrlName)
    cleanUrlName = cleanNewLine.sub('   ', cleanUrlName)
    cleanUrlName = notASCII2.sub('', cleanUrlName)
    cleanDate = clean4.sub('', Date)
    cleanDate = clean5.sub('', cleanDate)
    cleanDate = re.sub('    ', '    ', cleanDate)
    return cleanUrlName, cleanDate

def extract_cat_author(article_code): ##выделяем и чистим категорию и автора текста
    regCat = re.compile('<a href="/stati/.*?" class="pathway">.*?</a>', re. DOTALL)
    regAuthor = re.compile('<dd class=\"createdby\">.*?</dd>', re.DOTALL)
    cleanAuthor = re.compile('<dd class=\"createdby\">.*?Автор:[ ]*?', re.DOTALL)
    catlist = regCat.findall(article_code)
    authorlist = regAuthor.findall(article_code)
    cat = cleanTag.sub('', catlist[1])
    author = cleanAuthor.sub('', authorlist[0])
    author = cleanTag.sub('', author)
    author = notBackSlashT.sub('', author)
    return cat, author

def crowler(database, folder): ## главная функция. Получает на вход базу данных и тип материала (novosti или stati), запускает все функции
    with open(database, 'r', encoding = 'utf-8') as source:
        for info in source: ## проходимся по каждой ссылке в БД
            ## для каждой статьи/новости формируем массив articleData:
            ## 0)ссылка 1)название 2)день 3) месяц 4)год 5)категория (если нет - пустой элемент) 6)имя автора (если нет - пустой элемент)
            articleData = info.split('   ')
            dataSplit = articleData[2].split('.')
            articleData[2:3] = dataSplit
            try:
                time.sleep(2)
                req = urllib.request.Request('http://noviput.info/' + str(articleData[0]))
                with urllib.request.urlopen(req) as response: ##получаем исходный код каждой статьи/новости
                    article_code = response.read().decode('utf-8')
                    if folder == 'stati': 
                        cat, author = extract_cat_author(article_code)
                        articleData.append(cat)
                        articleData.append(author)
                    if folder == 'novosti':
                        articleData.append('')
                        articleData.append('')
            except:
                print('No such page')
            ## Итак, имеем: 1) массив articleData со всеми метаданными 2) исходный код статьи/новости
            pathToDir, filename = text_processing(article_code,articleData) ##обрабатываем исходный код, записываем обработанную новость в текстовый файл и записываем путь к нему в перем. path
            path = os.path.join(pathToDir, filename)
            mystem_processing(pathToDir, filename)
            record_meta(articleData, path) ##записываем все нужные метаданные в файл с метаданными
            articleData.clear()
            ##чистим массив articleData, открываем следующую статью и повторяем с ней все нужные операции



def text_processing(article_code,articleData):
    ##получает на вход исходный код, далее чистит его от тэгов и не-ascii символов, создает директорию для записи и записывает plain text
    raw_text = findPar.findall(article_code)
    text = ''
    for el in raw_text:
        text += cleanTag.sub('', el)
    text = cleanProbel.sub('', text)
    text = cleanNewLine.sub(' ', text)
    text = cleanMeta.sub('', text)
    text = notASCII1.sub('', text)
    month = notWeirdLines.sub('', articleData[3])
    year = notWeirdLines.sub('', articleData[4])
    pathToDir = os.path.join('plain', year, month)
    filename = notSlash.sub('', articleData[0])
    filename.strip(' ')
    if os.path.exists(pathToDir):
        with open(os.path.join(pathToDir, filename + '.txt'), 'w', encoding = 'utf-8') as dest:
                dest.write(text)
    else:
                os.makedirs(pathToDir)
                with open(os.path.join(pathToDir, filename), 'w', encoding = 'utf-8') as dest:
                    dest.write(text)
    return pathToDir, filename


def mystem_processing(pathToDir, filename):
    filename = filename + '.txt'
    dest_txt = regMystem.sub('mystem-plain', pathToDir)
    dest_xml = regMystem.sub('mystem-xml', pathToDir)
    if os.path.exists(dest_txt) != True:
        os.makedirs(dest_txt)
    if os.path.exists(dest_xml) != True:
        os.makedirs(dest_xml)
    inp = os.path.join(pathToDir, filename)
    outp_txt = os.path.join(dest_txt, filename)
    outp_xml = os.path.join(dest_xml, filename)
    os.system(r'C:\mystem.exe ' + inp + ' ' + outp_txt)
    os.system(r'C:\mystem.exe --format xml ' + inp + ' ' + outp_xml)


def record_meta(articleData, path):
    try:
        with open('metadata.csv', 'a', encoding = 'utf-8') as meta:
            meta.write(path +'	author	sex	birthday	'+articleData[1]+'	'+articleData[2] + '\.'+ articleData[3]+'\.'+articleData[4]+'	публицистика	genre_fi	type	topic	chronotop	нейтральный	н-возраст	н-уровень	районная	'+'http://noviput.info/'+str(ArticleData[0])+'	'+'Новый путь'+'	publisher	'+articleData[4]+'	газета	Россия	Дебесск	ru')
    except:
        print('Could not write metadata')
                
create_database('novosti')
crowler('database.csv', 'novosti')







