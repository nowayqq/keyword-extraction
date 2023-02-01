import codecs

from difflib import SequenceMatcher
from string import punctuation


def get_data(path):

    title = None
    text = ''

    with codecs.open(path, encoding='utf-8') as fin:
        lines = fin.readlines()

    if 'Title: ' in lines[0]:
        title = lines[0].replace('\r', '').replace('\n', '')
        lines.pop(0)
        title = title.replace('Title: ', '')

    for line in lines:
        text += line.replace('\r', '').replace('\n', '')
    text = text.replace('Text: ', '')

    if title == '':
        title = None

    fin.close()

    return title, text


def is_equal(a, b):
    mb = SequenceMatcher(lambda x: x in punctuation, a, b).get_matching_blocks()
    if sum(i.size for i in mb) < max(len(a), len(b)) - 2:
        return False
    return True


def prep_data(data: list):

    words = data

    unique = [x for x in words if sum(1 for i in words if is_equal(i, x)) == 1]
    mul = []
    for word in words:
        if sum(1 for i in words if is_equal(i, word)) != 1:
            mul.append(word)
        if len(mul) > 1:
            unique.append(mul[0])
            mul = []

    return sorted(unique)
