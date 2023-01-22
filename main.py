from data_prep import get_data
from pipeline import create_pipeline


_PATH = 'data/'
_FILENAME = 'text.txt'
_FILES = ['keywords.txt', 'verbs.txt', 'keyphrases.txt']

lang = 'ru'
kp_count = 1

title, text = get_data(_PATH + _FILENAME)
pipe = create_pipeline(text=text, title=title, lang=lang, kp_count=kp_count)

for i in range(len(_FILES)):
    with open(_PATH + _FILES[i], 'w', encoding='utf-8') as fout:
        for item in pipe[i]:
            if isinstance(item, tuple):
                fout.write(str(item[0]) + '\n')
            else:
                fout.write(str(item) + '\n')
    fout.close()
