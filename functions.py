import yake
import spacy


def get_verbs(text, title, lang):
    full_text = text

    if title is not None:
        if title[-1] == ' ':
            title = title[:-1]
        if title[-1] == '.':
            full_text = title + " " + text
        else:
            full_text = title + ". " + text

    if lang == 'ru':
        nlp = spacy.load('ru_core_news_md')
    else:
        nlp = spacy.load('en_core_web_md')

    doc = nlp(full_text)
    return [token.lemma_ for token in doc if token.pos_ == "VERB"]


def get_keywords(text, title, lang):
    full_text = text

    if title is not None:
        if title[-1] == ' ':
            title = title[:-1]
        if title[-1] == '.':
            full_text = title + " " + text
        else:
            full_text = title + ". " + text

    if lang == 'ru':
        nlp = spacy.load('ru_core_news_md')
    else:
        nlp = spacy.load('en_core_web_md')

    doc = nlp(full_text)
    return [(entity.text, entity.label_) for entity in doc.ents]


def get_keyphrases(text, title, lang, kp_count):
    full_text = text

    if title is not None:
        if title[-1] == ' ':
            title = title[:-1]
        if title[-1] == '.':
            full_text = title + " " + text
        else:
            full_text = title + ". " + text

    kw_extractor = yake.KeywordExtractor(lan=lang, top=kp_count, n=20)
    return kw_extractor.extract_keywords(full_text)