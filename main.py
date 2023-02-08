import PySimpleGUI as sg
from data_prep import isValid


_LANGUAGES = ['ru', 'en']
_METHODS = ['1', '2']

_VARS = {'window': False,
         'url': '',
         'method': _METHODS[0],
         'lang': _LANGUAGES[0]}

AppFont = ('Roboto', 12)
sg.theme('black')

layout = [[sg.Combo(_METHODS, size=(20, 0),
                    enable_events=True, key='-METHOD-',
                    default_value=_METHODS[0],
                    background_color='Grey',
                    text_color='Black',
                    pad=((36, 0), (10, 0)),
                    readonly=True,
                    font=AppFont),
           sg.Combo(_LANGUAGES, size=(20, 0),
                    enable_events=True, key='-LANGUAGE-',
                    default_value=_LANGUAGES[0],
                    background_color='Grey',
                    text_color='Black',
                    pad=((36, 0), (10, 0)),
                    readonly=True,
                    font=AppFont)],
          [sg.Button('LoadURL', font=AppFont, pad=((58, 0), (0, 0)), size=(10, 0)),
           sg.Input(key='-IN-', pad=((10, 0), (10, 0)), size=(25, 0),
                    text_color='Black', background_color='Grey',
                    font=AppFont)],
          [sg.Button('Exit', font=AppFont, pad=((504, 0), (3, 0)), size=(10, 0))]]

_VARS['window'] = sg.Window('Keyword extractor',
                            layout,
                            finalize=True,
                            resizable=True,
                            location=(0, 0),
                            element_justification="center",
                            background_color='#FDF6E3')


def updateMethod(method: str):

    _VARS['method'] = method


def updateLanguage(language: str):

    _VARS['lang'] = language


def updateURL(url: str):

    if isValid(url):
        _VARS['url'] = url
        print('True')
    elif isValid('https://' + url):
        _VARS['url'] = 'https://' + url
        print('True')
    else:
        _VARS['url'] = ''
        print('False')
    print(_VARS['url'])


while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'LoadURL':
        updateURL(values['-IN-'])
    elif event == '-METHOD-':
        updateMethod(values['-METHOD-'])
    elif event == '-LANGUAGE-':
        updateLanguage(values['-LANGUAGE-'])

_VARS['window'].close()
