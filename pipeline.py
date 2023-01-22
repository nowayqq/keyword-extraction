from sklearn.pipeline import Pipeline
from functions import get_verbs
from functions import get_keywords
from functions import get_keyphrases


def create_pipeline(
        text: str, title: str = None, lang: str = 'ru', kp_count: int = 1
) -> Pipeline:
    pipeline_steps = [
        ("keywords", get_keywords(text, title, lang)),
        ("verbs", get_verbs(text, title, lang)),
        ("keyphrases", get_keyphrases(text, title, lang, kp_count))
    ]
    return Pipeline(steps=pipeline_steps)