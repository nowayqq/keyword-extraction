import validators
from difflib import SequenceMatcher
from string import punctuation


def prep_text(text: str):

    i = 0
    j = 0
    result = text
    while i < len(result):
        if j >= 62 and result[i] == ' ':
            result = result[:i] + '\n' + result[i + 1:]
            j = 0
        j += 1
        i += 1
    return result


def tags_to_str(tags: list):

    tags_str = ''
    for tag in tags:
        tags_str += tag + ', '
    return tags_str[:-2] + '\n'


def isValid(url: str):

    if validators.url(url):
        return True
    else:
        return False


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

    try:
        unique.remove('это')
    except ValueError:
        return sorted(unique)

    return sorted(unique)

