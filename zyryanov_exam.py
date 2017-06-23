import os
import re

def count_sent():
    sent_num = {}
    w = open('results.txt', 'w', encoding = 'utf-8')
    for el in os.listdir('news'):
        with open(os.path.join('news',el), 'r', encoding = 'Windows-1251') as f:
            article = f.read()
            sentences = re.findall(r'<se>', article)
            sent_num[el] = len(sentences)
            template = '{}   {}\n'
            w.write(template.format(el, len(sentences)))
    w.close()
count_sent()
        
