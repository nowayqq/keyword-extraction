from data_prep import get_data
from data_prep import prep_data
from news_parsers import get_parser
from pipeline import create_pipeline


method = int(input('Choose method: '))

_PATH = 'data/'
_FILENAME = 'example4.txt'
_FILES = ['keywords.txt', 'verbs.txt', 'keyphrases.txt']

lang = 'ru'
kp_count = 1

title, text = get_data(_PATH + _FILENAME)
pipe = create_pipeline(text=text, method=method, title=title, lang=lang, kp_count=kp_count)

q = []

for i in range(len(_FILES)):
    with open(_PATH + _FILES[i], 'w', encoding='utf-8') as fout:
        tmp = list(dict.fromkeys(pipe[i]))
        if _FILES[i] == 'keywords.txt' and method == 2:
            tmp = prep_data(pipe['keywords'])
        for item in tmp:
            if isinstance(item, tuple):
                fout.write(str(item[0]) + '\n')
            else:
                fout.write(str(item) + '\n')
    fout.close()

url = ''
parsed_news = get_parser(url)

if parsed_news is not None:
    print(parsed_news[0] + '\n\n' +
          parsed_news[1] + '\n')
    tmp_str = ''
    for item in parsed_news[2]:
        tmp_str += item + ', '
    print(tmp_str)
else:
    print('Invalid url')
