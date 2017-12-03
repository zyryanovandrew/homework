import os
from flask import Flask
from flask import render_template, request, redirect, url_for
import math
import time

stimuli = {'1':'Все гости дружно уселись за',
'2':'Бабушка купила таблетки от головной боли в',
'3':'На экзамене студент допустил досадную',
'4':'Летом мальчик катался на двухколёсном',
'5':'Отправитель наклеил на письмо',
'6':'Кошки превосходно видят в',
'7':'Выпускница надела босоножки на высоких',
'8':'Именинник налил в стакан апельсиновый',
'9':'Художник точил цветной',
'10':'Певица высушила волосы с помощью',
'11':'Крестьянин вчера усердно полол',
'12':'Перед праздником секретарша украсила',
'13':'Консьержка раз в месяц мыла',
'14':'На лугу пастушка неумело стригла',
'15':'Андрей устал нести тяжёлый',
'16':'В сентябре директор школы взял на работу нового',
'17':'Музыкант играл на старинной',
'18':'Сестра волновалась перед важным',
'19':'Отдыхающие загорали и купались в',
'20':'Первоклассник украшал ёлку яркими',
'21':'Моя крестница живёт прямо напротив местного',
'22':'Художник изобразил на картине',
'23':'На праздник мама подарила сыну',
'24':'В командировки военный брал с собой',
'25':'Семейная пара мечтала следующим летом отдохнуть в',
'26':'Из шкафа мама достала старую',
'27':'На рынке фермер недорого продавал',
'28':'Грабители украли из квартиры ценный',
'29':'Депутат обвинил мэра в',
'30':'Открывая дверь, секретарша случайно уронила'}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/json', methods=['GET', 'POST'])
def recorder():
    responses = []
    for i in range (1,30):        
        resp = request.args.get(str(i))
        responses.append(str(resp))
    with open('rawdata.csv', 'a', encoding = 'utf-8') as f:
        text = ''
        for el in responses:
            text += str(el) + ','
        text += '\n'
        f.write(text)
    return render_template('json.html', responses = responses)

def data_analysis():
    with open('rawdata.csv', 'r', encoding = 'utf-8') as f:
        raw = f.read()
        subjects = raw.split('\n')
        sentence_res = {}
        for num in range(1,31):
            sentence_res[str(num)] = []
        for subj in subjects:
            answers = subj.split(',')
            for i,answer in enumerate(answers):
                towrite = str(answer)
                towrite.strip()
                towrite.lower()
                sentence_res[str(i+1)].append(towrite)
        final_output = {}
        for sent_num in sentence_res:
            count_nominations = {}
            for nomination in sentence_res[sent_num]:
                if nomination not in count_nominations:
                    count_nominations[nomination] = 1
                else:
                    count_nominations[nomination] += 1
            percentage, pred = count_predictability(count_nominations)
            final_output[stimuli[sent_num]] = [percentage, pred] 
        return final_output

@app.route('/stats')
def visualize_stats():
    final_output = data_analysis()
    return render_template('stats.html', final_output = final_output)


def count_predictability(count_nominations):
    totalNum = 0.00
    pred = 0.00
    for nom in count_nominations:
        num = float(int(count_nominations[nom]))
        totalNum += num
    percentage = {}
    for nom in count_nominations:
        num = float(int(count_nominations[nom]))
        prob = num/totalNum
        prob_log2prob = prob*math.log2(1/prob)
        pred += prob_log2prob
        pred = round(pred, 4)
        if nom != '':
            percentage[nom] = str(round((num*100/totalNum), 1))
        else:
            percentage['нет ответа'] = str(round((num*100/totalNum), 1))
    return percentage, pred

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    final_output = data_analysis()
    query = request.args.get('query')
    query_str = query.lower()
    for key in stimuli:
        sent = stimuli[key]
        sent = sent.lower()
        if query_str in sent:
            result = final_output[stimuli[key]]
            stimulus = stimuli[key]
            percentage = result[0]
            pred = result[1]
            break
        else:
            stimulus = 'Извините, ничего не найдено'
            percentage = {'':''}
            pred = ''
            continue
    return render_template('results.html', stimulus = stimulus, percentage = percentage, pred = pred)
        
if __name__ == '__main__':
    app.run()
