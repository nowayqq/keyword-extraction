from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


_NEWS_SITES_WITH_PARSERS = ['ria.ru']


def get_parser(url: str):

    try:
        domain = re.search('https?://([A-Za-z_0-9.-]+).*', url).group(1)
    except AttributeError:
        domain = ''
        pass
    if domain not in _NEWS_SITES_WITH_PARSERS:
        return None
    elif domain == _NEWS_SITES_WITH_PARSERS[0]:
        return parse_ria(url)


def parse_ria(url: str):

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    raw_text = text

    text = re.sub(r"https?://[^,\s]+,?", "", text)
    text = text[re.search(r'content \d+ .+ — РИА Новости. ', text).end():re.search(r' Новости 154.796', text).start()]

    i = 1
    while i < len(text):
        if text[i - 1] == '.':
            text = text[:i] + ' ' + text[i:]
        i += 1

    text = text.replace('  ', ' ').replace('&lt;. . . &gt;', '<...>')

    while text[-1] != '.':
        text = text[:-1]

    title = raw_text[:re.search(r' - РИА Новости, ', raw_text).start()]

    tags = re.sub(r"https?://[^,\s]+,?", "", raw_text)
    tags = tags[re.search(r'Новостиru-RU Новости 154.796internet-group@rian.ru7 495 645-6601ФГУП МИА «Россия сегодня»\n35360\n3536019201080true19201440true Новости 154.796internet-group@rian.ru7 495 645-6601ФГУП МИА «Россия сегодня»\n35360\n35360', tags).end():]
    tags = tags[:re.search(r'\d{2}:', tags).start()]
    tags = tags.replace('ФГУП МИА «Россия сегодня»\n35360\n35360', '')

    for i in range(len(tags)):
        if (tags[i].islower() or tags[i].isdigit()) and tags[i + 1].isupper():
            tags = tags[i + 1:]
            break
    tags = tags.replace('\n', ' ').split(sep=',')
    for i in range(len(tags)):
        if tags[i].startswith(' '):
            tags[i] = tags[i][1:]

    return title, text, tags
