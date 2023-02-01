from sklearn.pipeline import Pipeline
from functions import *


def create_pipeline(
        text: str, method: int = 1, title: str = None, lang: str = 'ru', kp_count: int = 1
) -> Pipeline:
    if method == 2:
        pipeline_steps = [
            ("keywords", get_keywords2(text, title, lang)),
            ("verbs", get_verbs(text, title, lang)),
            ("keyphrases", get_keyphrases2(text, title, lang, kp_count))
        ]
    else:
        pipeline_steps = [
            ("keywords", get_keywords1(text, title, lang)),
            ("verbs", get_verbs(text, title, lang)),
            ("keyphrases", get_keyphrases1(text, title, lang, kp_count))
        ]

    return Pipeline(steps=pipeline_steps)
