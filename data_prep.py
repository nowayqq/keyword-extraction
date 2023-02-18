import validators
from difflib import SequenceMatcher
from string import punctuation


def prep_data_for_save(lst: list):
    res = []
    for i in range(4):
        res.append(lst[i])
    lst = lst[4:]
    for item in lst:
        tmp_str = ''
        for sub_item in item:
            tmp_str += sub_item + ','
        res.append(tmp_str[:-1])
    return res


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


def list_to_str(lst: list):
    lst_str = ''
    for item in lst:
        if isinstance(item, tuple):
            lst_str += item[0] + ', '
        else:
            lst_str += item + ', '
    return lst_str[:-2]


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


def check_words(lst, word):
    flag = True
    for item in lst:
        if word in item:
            flag = False
    return flag


def del_duplicates(lst):
    li = []
    for item in lst:
        if isinstance(item, tuple):
            if item[0] not in li and check_words(li, item[0]):
                li.append(item[0])
        else:
            if item not in li:
                li.append(item)
    return li


def prep_data(data: list):
    words = []
    for item in data:
        if isinstance(item, tuple):
            words.append(item[0])
        else:
            words.append(item)
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

