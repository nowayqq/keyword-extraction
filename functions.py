import yake
import spacy
import nltk

from nlp_rake import Rake
from nltk.corpus import stopwords
from summa import keywords


def get_stops(lang='ru'):

    nltk.download("stopwords")

    if lang == 'ru':
        return list(set(stopwords.words("russian")))
    else:
        return list(set(stopwords.words("english")))


def get_keywords2(text, title, lang):
    full_text = text

    if title is not None:
        if title[-1] == ' ':
            title = title[:-1]
        if title[-1] == '.':
            full_text = title + " " + text
        else:
            full_text = title + ". " + text

    text_clean = ""

    stops = get_stops(lang)

    for i in full_text.split():
        if i not in stops:
            text_clean += i + " "

    if lang == 'ru':
        return keywords.keywords (text_clean, language="russian").split("\n")
    else:
        return keywords.keywords (text_clean, language="english").split("\n")


def get_keyphrases2(text, title, lang, kp_count):
    full_text = text

    if title is not None:
        if title[-1] == ' ':
            title = title[:-1]
        if title[-1] == '.':
            full_text = title + " " + text
        else:
            full_text = title + ". " + text

    stops = get_stops(lang)

    rake = Rake(stopwords=stops, max_words=20)
    return rake.apply(text)[:kp_count]


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


def get_keywords1(text, title, lang):
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


def get_keyphrases1(text, title, lang, kp_count):
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