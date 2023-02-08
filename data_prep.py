import codecs
import validators
from difflib import SequenceMatcher
from string import punctuation


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

