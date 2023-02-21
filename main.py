import os
import PySimpleGUI as sg
from news_parsers import get_parser
from data_prep import prep_text, prep_data, isValid, list_to_str, del_duplicates, prep_data_for_save
from pipeline import create_pipeline

_PATH = 'data/'
_FILES = ['keywords.txt', 'verbs.txt', 'keyphrases.txt']

_LANGUAGES = ['ru', 'en']
_METHODS = ['Method 1', 'Method 2']

_TMPLST = []

_VARS = {'window': False,
         'url': '',
         'method': _METHODS[0],
         'lang': _LANGUAGES[0],
         'kp_count': 1,
         'title': '',
         'text': '',
         'tags': []}

AppFont = ('Roboto', 12)
sg.theme('black')

layout = [[sg.Text(text="\n",
                   key='title',
                   font=('Roboto', 14),
                   background_color='#FDF6E3',
                   pad=((0, 0), (10, 0)),
                   text_color='Black')],
          [sg.Text(text="Enter url",
                   key='text',
                   font=('Roboto', 32),
                   background_color='#FDF6E3',
                   pad=((0, 0), (10, 0)),
                   text_color='Black')],
          [sg.Text(text="",
                   key='tags',
                   font=('Roboto', 10),
                   background_color='#FDF6E3',
                   pad=((0, 0), (10, 0)),
                   text_color='Black')],
          [sg.Input(key='-IN-', pad=((0, 0), (10, 0)), size=(40, 0),
                    text_color='Black', background_color='Grey',
                    font=AppFont),
           sg.Combo(_METHODS, size=(10, 0),
                    enable_events=True, key='-METHOD-',
                    default_value=_METHODS[0],
                    background_color='Grey',
                    text_color='Black',
                    pad=((20, 0), (10, 0)),
                    readonly=True,
                    font=AppFont,
                    visible=False),
           sg.Combo(_LANGUAGES, size=(10, 0),
                    enable_events=True, key='-LANGUAGE-',
                    default_value=_LANGUAGES[0],
                    background_color='Grey',
                    text_color='Black',
                    pad=((20, 0), (10, 0)),
                    readonly=True,
                    font=AppFont,
                    visible=False)],
          [sg.Button('Load URL', key='LoadURL', font=AppFont,
                     pad=((0, 0), (10, 0)), size=(10, 0)),
           sg.Button('Exit', key='Exit1', font=AppFont,
                     pad=((168, 0), (10, 0)), size=(10, 0), visible=True),
           sg.Button('Process text', key='ProcText', font=AppFont,
                     pad=((286, 0), (10, 0)), size=(25, 0), visible=False)],
          [sg.Button('Save results', key='SaveRes', font=AppFont, disabled=True,
                     pad=((384, 0), (10, 0)), size=(12, 0), visible=False),
           sg.Button('Exit', key='Exit2', font=AppFont,
                     pad=((1, 0), (10, 0)), size=(12, 0), visible=False)]]

_VARS['window'] = sg.Window('Keyword extractor',
                            layout,
                            finalize=True,
                            resizable=False,
                            location=(0, 0),
                            element_justification="left",
                            background_color='#FDF6E3')


def _onKeyRelease(key_event):
    ctrl = (key_event.state & 0x4) != 0
    if key_event.keycode == 88 and ctrl and key_event.keysym.lower() != "x":
        key_event.widget.event_generate("<<Cut>>")

    if key_event.keycode == 86 and ctrl and key_event.keysym.lower() != "v":
        key_event.widget.event_generate("<<Paste>>")

    if key_event.keycode == 67 and ctrl and key_event.keysym.lower() != "c":
        key_event.widget.event_generate("<<Copy>>")

    if key_event.keycode == 65 and ctrl and key_event.keysym.lower() != "a":
        key_event.widget.event_generate("<<SelectAll>>")


def updateMethod(method: str):
    _VARS['method'] = method
    _VARS['window'].Element('SaveRes').Update(disabled=True)


def updateLanguage(language: str):
    _VARS['window'].Element('SaveRes').Update(disabled=True)
    _VARS['lang'] = language


def updateInterface(mode: int, any_=None):
    if mode == 0:
        _VARS['window'].Element("title").Update(prep_text(any_[0]))
        if len(prep_text(any_[1])) > 1500:
            _VARS['window'].Element("text").Update(prep_text(any_[1])[:1497] + '...')
        else:
            _VARS['window'].Element("text").Update(prep_text(any_[1]))
        _VARS['window'].Element("tags").Update(prep_text(list_to_str(any_[2]) + '\n'))
        _VARS['window'].Element('-METHOD-').Update(visible=True)
        _VARS['window'].Element('-LANGUAGE-').Update(visible=True)
        _VARS['window'].Element('ProcText').Update(visible=True)
        _VARS['window'].Element('Exit1').Update(visible=False)
        _VARS['window'].Element('SaveRes').Update(visible=True)
        _VARS['window'].Element('Exit2').Update(visible=True)
        _VARS['window'].Element('text').Update(font=AppFont)
        _VARS['title'] = any_[0]
        _VARS['text'] = any_[1]
        _VARS['tags'] = any_[2]

    elif mode == 1 or mode == 2:
        _VARS['window'].Element("title").Update('\n')
        _VARS['window'].Element("tags").Update('')
        _VARS['window'].Element('-METHOD-').Update(visible=False)
        _VARS['window'].Element('-LANGUAGE-').Update(visible=False)
        _VARS['window'].Element('ProcText').Update(visible=False)
        _VARS['window'].Element('Exit1').Update(visible=True)
        _VARS['window'].Element('SaveRes').Update(visible=False)
        _VARS['window'].Element('Exit2').Update(visible=False)
        _VARS['window'].Element('text').Update(font=('Roboto', 32))
        if mode == 2:
            _VARS['window'].Element("text").Update('Invalid url')
        else:
            _VARS['window'].Element("text").Update('This source has no\nparsers')

    elif mode == 3:
        _VARS['window'].Element('title').Update(font=('Roboto', 12))
        _VARS['window'].Element('text').Update(font=('Roboto', 12))
        _VARS['window'].Element('tags').Update(font=('Roboto', 12))
        _VARS['window'].Element("title").Update(prep_text('Keyphrases: ' + list_to_str(any_['keyphrases'])))
        if _VARS['method'] == 'Method 2':
            _VARS['window'].Element("text").Update(prep_text('Keywords: ' + list_to_str(prep_data(any_['keywords']))))
        else:
            _VARS['window'].Element("text").Update(
                prep_text('Keywords: ' + list_to_str(del_duplicates(any_['keywords']))))
        _VARS['window'].Element("tags").Update(prep_text('Verbs: ' + list_to_str(any_['verbs'])))


def updateURL(url: str):
    _VARS['window'].Element('SaveRes').Update(disabled=True)
    flag = True
    if isValid(url):
        _VARS['url'] = url
    elif isValid('https://' + url):
        _VARS['url'] = 'https://' + url
    else:
        _VARS['url'] = ''
        flag = False

    if flag:
        parsed_news = get_parser(url)
        if parsed_news is None:
            updateInterface(1)
        elif parsed_news == '':
            updateInterface(2)
        else:
            updateInterface(0, parsed_news)
    else:
        updateInterface(2)


def saveResults(lst: list):
    _VARS['window'].Element('SaveRes').Update(disabled=True)
    try:
        with open('data/result.txt', 'a') as f:
            tmp_arr = [_VARS['url'], _VARS['method'], _VARS['title'],
                       _VARS['text'], _VARS['tags']]

            for item in lst:
                tmp_arr.append(item[0])

            save = prep_data_for_save(tmp_arr)
            for item in save:
                f.write(item + '\n\n')
            f.write('\n')
        f.close()
    except FileNotFoundError:
        os.mkdir('data')
        saveResults(lst)

    return []


def processText():
    pipe = create_pipeline(text=_VARS['text'], method=_VARS['method'],
                           lang=_VARS['lang'], kp_count=_VARS['kp_count'])

    for i in range(len(_FILES)):
        tmp = list(dict.fromkeys(pipe[i]))
        tmp_arr = []
        if _FILES[i] == 'keywords.txt' and _VARS['method'] == _METHODS[1]:
            tmp = prep_data(pipe['keywords'])
        for item in tmp:
            if isinstance(item, tuple):
                tmp_arr.append(item[0])
            else:
                tmp_arr.append(item)
        _TMPLST.append((tmp_arr, _FILES[i]))

    _VARS['window'].Element('SaveRes').Update(disabled=False)
    updateInterface(3, pipe)


_VARS['window'].TKroot.bind_all("<Key>", _onKeyRelease, "+")

while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED or event == 'Exit1' or event == 'Exit2':
        break
    elif event == 'LoadURL':
        updateURL(values['-IN-'])
    elif event == '-METHOD-':
        updateMethod(values['-METHOD-'])
    elif event == '-LANGUAGE-':
        updateLanguage(values['-LANGUAGE-'])
    elif event == 'ProcText':
        processText()
    elif event == 'SaveRes':
        _TMPLST = saveResults(_TMPLST)

_VARS['window'].close()
