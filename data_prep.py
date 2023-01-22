import codecs


def get_data(path):

    title = None
    text = ''

    with codecs.open(path, encoding='utf-8') as fin:
        lines = fin.readlines()

    if 'Title:' in lines[0]:
        title = lines[0].replace('\r', '').replace('\n', '')
        lines.pop(0)
        title.replace('Title: ', '')

    for line in lines:
        text += line.replace('\r', '').replace('\n', '')
    text = text.replace('Text: ', '')

    if title == '':
        title = None

    return title, text
