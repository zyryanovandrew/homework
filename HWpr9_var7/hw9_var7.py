import re
def print_forms():
    with open('rudin.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        wordarr = text.split()
        sit_arr = []
        for word in wordarr:
            word.lower()
            word.strip(',...!?-–— :,')
            t = re.match('си(жу|д(е(ть|в((ши)?й?)?|л(а|о|и)?)|и(те?|м|шь)?|я(т|щий)?))', word)
            if (t != None) and (word not in sit_arr):
                sit_arr.append(word)
        for el in sit_arr:
            print (el)


print_forms()
