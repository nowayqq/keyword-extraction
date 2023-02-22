from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


_NEWS_SITES_WITH_PARSERS = ['ria.ru', 'rsport.ria.ru', 'realty.ria.ru']
_RIA = _NEWS_SITES_WITH_PARSERS[:3]
SYMBOLS = ['(', ')', '\'', '\"', '*', '!', '.']


def get_parser(url: str):

    try:
        domain = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
    except AttributeError:
        domain = ''
        pass
    if domain not in _NEWS_SITES_WITH_PARSERS:
        return None
    elif domain in _RIA:
        return parse_ria(url)


def parse_ria(url: str):

    try:
        html = urlopen(url).read()
    except HTTPError:
        return ''
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    raw_text = text

    text = re.sub(r"https?://[^,\s]+,?", "", text)
    try:
        text = text[re.search(r'@content \d+ .+ —?-?–?—?–?−?-? РИА (Новости)?'
                              r'(Недвижимость)?. ', text).end():re.search(
                              r' Новости (Спорт )?154.796', text).start()]
    except AttributeError:
        text = raw_text[re.search(r'@contenthttps://.*.jpg', raw_text).end():
                        re.search(r' Новости (Спорт )?154.796', raw_text).start()]
        text = re.sub(r"https?://[^,\s]+,?", "", text)

    i = 1
    while i < len(text):
        if text[i - 1] == '.':
            text = text[:i] + ' ' + text[i:]
        i += 1

    text = text.replace('  ', ' ').replace('&lt;', '<').replace('&gt;', '>')

    while text[-1] != '.':
        text = text[:-1]

    try:
        title = raw_text[:re.search(r' - (Недвижимость )?РИА Новости( Спорт)?, '
                                    , raw_text).start()]
    except AttributeError:
        title = raw_text[:re.search(r'\nРегистрация пройдена успешно!\nПожалуйста, '
                                    r'перейдите по ссылке из письма,', raw_text).start()]

    tags = re.sub(r"https?://[^,\s]+,?", "", raw_text)
    tags = tags[re.search(
        r'201080true19201440true (РИА )?Новости (Спорт )?'
        r'154.796internet-group@rian.ru7 495 645-6601ФГУП '
        r'МИА «Россия сегодня»(\n35360\n35360)?(\n20660\n20660)?'
        r'(\n42060\n42060)?', tags).end():]
    tags = tags[:re.search(r'\d{2}:', tags).start()]
    tags = tags.replace('ФГУП МИА «Россия сегодня»\n35360\n35360', '')
    tags = tags.replace('ФГУП МИА «Россия сегодня»\n20660\n20660', '')
    tags = tags.replace('ФГУП МИА «Россия сегодня»\n42060\n42060', '')

    for i in range(len(tags) - 1):
        if (tags[i].islower() or tags[i].isdigit() or tags[i] in SYMBOLS) and tags[i + 1].isupper():
            tags = tags[i + 1:]
            break
    tags = tags.replace('\n', ' ').split(sep=',')
    for i in range(len(tags)):
        if tags[i].startswith(' '):
            tags[i] = tags[i][1:]

    return title, text, tags
