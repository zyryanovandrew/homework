import re
import os
import urllib
import codecs
import json
from flask import Flask
from flask import render_template, request, redirect, url_for

Tables = re.compile('<table.*?Page [0-9].*?<\/table>', re.DOTALL)
WordLines = re.compile('<tr>.*?th.*?pos.*?<\/tr>', re.DOTALL)
FindThai = re.compile('class="?th"?.*?<\/td>', re.DOTALL)
FindTransl = re.compile('class="?pos"?>.*?<td>.*?<\/td>', re.DOTALL)
CleanTag = re.compile('<.*?>', re.DOTALL)
CleanThai = re.compile('class.*?><a href=\'.*?\'>', re.DOTALL)
CleanTransl = re.compile('class.*?<\/td><td>', re.DOTALL)

def dictionary_parser():
    pages = os.listdir('thai_pages')
    full_dict = ''
    for page in pages:
        with codecs.open(os.path.join('thai_pages', page), 'r', encoding = 'UTF-8') as f:
            source_code = f.read()
            source_code += '\n'
            full_dict += source_code
    word_tables = Tables.findall(full_dict)
    words = []
    for table in word_tables: ##находим в таблицах строки со словами
        words_temp = WordLines.findall(table)
        for el in words_temp:
            if 'example' in el:
                continue
            else:
                if 'interjection' in el:
                    continue
                else:
                    if 'abbreviation' in el:
                        continue
                    else:
                        words.append(el)
    dictionary_raw = {}
    dictionary_thai = {}
    dictionary_eng = {}
    for word in words:
        thai_temp = FindThai.findall(word)
        transl_temp = FindTransl.findall(word)
        if (len(thai_temp) == 1) and (len(transl_temp) == 1):
            dictionary_raw[thai_temp[0]] = transl_temp[0]
    for key in dictionary_raw:
        thai_clean = CleanThai.sub('', key)
        thai_clean = CleanTag.sub('', thai_clean)
        transl_clean = CleanTransl.sub('', dictionary_raw[key])
        transl_clean = CleanTag.sub('', transl_clean)
        dictionary_thai[thai_clean] = transl_clean
    for key in dictionary_thai:
        dictionary_eng[dictionary_thai[key]] = key
    with open('dictionary_thai.json', 'w', encoding = 'utf-8') as f:
        json.dump(dictionary_thai, f)
    with open('dictionary_eng.json', 'w', encoding = 'utf-8') as f:
        json.dump(dictionary_eng, f)

dictionary_parser()
