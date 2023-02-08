import PySimpleGUI as sg
from data_prep import isValid
from data_prep import tags_to_str
from news_parsers import get_parser
from data_prep import prep_text


_LANGUAGES = ['ru', 'en']
_METHODS = ['Method 1', 'Method 2']

_VARS = {'window': False,
         'url': '',
         'method': _METHODS[0],
         'lang': _LANGUAGES[0]}

AppFont = ('Roboto', 12)
sg.theme('black')

_TITLE = ''
_TEXT = ''
_TAGS = []

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
          [sg.Button('Load URL', key='LoadURL', font=AppFont, pad=((0, 0), (10, 0)), size=(10, 0)),
           sg.Button('Exit', key='Exit1', font=AppFont, pad=((168, 0), (10, 0)), size=(10, 0), visible=True),
           sg.Button('Process text', key='ProcText', font=AppFont, pad=((286, 0), (10, 0)), size=(25, 0),
                     visible=False)],
          [sg.Button('Exit', key='Exit2', font=AppFont, pad=((501, 0), (10, 0)), size=(12, 0), visible=False)]]

_VARS['window'] = sg.Window('Keyword extractor',
                            layout,
                            finalize=True,
                            resizable=False,
                            location=(0, 0),
                            element_justification="left",
                            background_color='#FDF6E3')


def updateMethod(method: str):
    _VARS['method'] = method


def updateLanguage(language: str):
    _VARS['lang'] = language


def updateURL(url: str):
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
            _VARS['window'].Element("title").Update('\n')
            _VARS['window'].Element("text").Update('This source has no\nparsers')
            _VARS['window'].Element("tags").Update('')
            _VARS['window'].Element('-METHOD-').Update(visible=False)
            _VARS['window'].Element('-LANGUAGE-').Update(visible=False)
            _VARS['window'].Element('ProcText').Update(visible=False)
            _VARS['window'].Element('Exit1').Update(visible=True)
            _VARS['window'].Element('Exit2').Update(visible=False)
            _VARS['window'].Element('text').Update(font=('Roboto', 32))
        elif parsed_news == '':
            _VARS['window'].Element("title").Update('\n')
            _VARS['window'].Element("text").Update('Invalid url')
            _VARS['window'].Element("tags").Update('')
            _VARS['window'].Element('-METHOD-').Update(visible=False)
            _VARS['window'].Element('-LANGUAGE-').Update(visible=False)
            _VARS['window'].Element('ProcText').Update(visible=False)
            _VARS['window'].Element('Exit1').Update(visible=True)
            _VARS['window'].Element('Exit2').Update(visible=False)
            _VARS['window'].Element('text').Update(font=('Roboto', 32))
        else:
            _VARS['window'].Element("title").Update(prep_text(parsed_news[0]))
            _VARS['window'].Element("text").Update(prep_text(parsed_news[1]))
            _VARS['window'].Element("tags").Update(prep_text(tags_to_str(parsed_news[2])))
            _VARS['window'].Element('-METHOD-').Update(visible=True)
            _VARS['window'].Element('-LANGUAGE-').Update(visible=True)
            _VARS['window'].Element('ProcText').Update(visible=True)
            _VARS['window'].Element('Exit1').Update(visible=False)
            _VARS['window'].Element('Exit2').Update(visible=True)
            _VARS['window'].Element('text').Update(font=AppFont)
    else:
        _VARS['window'].Element("title").Update('\n')
        _VARS['window'].Element("text").Update('Invalid url')
        _VARS['window'].Element("tags").Update('')
        _VARS['window'].Element('-METHOD-').Update(visible=False)
        _VARS['window'].Element('-LANGUAGE-').Update(visible=False)
        _VARS['window'].Element('ProcText').Update(visible=False)
        _VARS['window'].Element('Exit1').Update(visible=True)
        _VARS['window'].Element('Exit2').Update(visible=False)
        _VARS['window'].Element('text').Update(font=('Roboto', 32))


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

_VARS['window'].close()
