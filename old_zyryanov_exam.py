import os
import re

def preprocessing():
    all_meta = []
    w = open('results.txt', 'w', encoding = 'utf-8')
    for el in os.listdir('news'):
        with open(os.path.join('news',el), 'r', encoding = 'Windows-1251') as f:
            article = f.read()
            ## подсчет числа предложений
            sentences = re.findall(r'<se>', article)
            template = '{}   {}\n'
            w.write(template.format(el, len(sentences)))

            ## получение нужных метаданных
            author = re.findall(r'<meta content=".+" name="author"></meta>', article)
            authorstr = author[0]
            authorstr = re.sub('<meta content="', '', authorstr)
            authorstr = re.sub('" name="author"></meta>', '', authorstr)
            topic = re.findall(r'<meta content=".+" name="topic"></meta>', article)
            topicstr = topic[0]
            topicstr = re.sub('<meta content="', '', topicstr)
            topicstr = re.sub('" name="topic"></meta>', '', topicstr)
            meta = el+','+authorstr+','+topicstr+'\n'
            all_meta.append(meta)

            ## создание списка слов, а затем биграм
            words = []
            wordsraw = re.findall('<w><ana lex=".+" gr=".+"></ana>.+</w>', article)
            for el in wordsraw:
                wordsrawstr = el
                wordsrawstr = re.sub('<w><ana lex=".+" gr=".+"></ana>', '', wordsrawstr)
                wordsrawstr = re.sub('</w>', '', wordsrawstr)
                wordsrawstr = re.sub('`', '', wordsrawstr)
                wordsrawstr = wordsrawstr.lower()
                words.append(wordsrawstr)
            bigrams = []
            for ind in range(1, len(words) - 1):
                bigrams.append(' '.join([words[ind - 1], words[ind]]))           
    w.close()
    return bigrams, all_meta

def data(all_meta):
    w = open('metadata.csv', 'w', encoding = 'utf-8')
    w.write('Название файла,Автор,Тематика текста\n')
    for el in all_meta:
        w.write(el)
    w.close()
        
def bigram_processing(bigrams):
    w = open('bigrams_res.txt', 'w', encoding = 'utf-8')
    for el in bigrams:
        if re.match(r'(в|на|о|об|обо|при|по) .+(е|и|ах|ях)', el) != None:
            bigram = el + '\n'
            w.write(bigram)
    w.close()

bigrams, all_meta = preprocessing()
bigram_processing(bigrams)
data(all_meta)

        
