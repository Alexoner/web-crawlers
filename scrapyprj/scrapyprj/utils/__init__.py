
from goose import Goose
from goose.text import StopWordsChinese


def safe_extract(selectors, separator='\t'):
    if not selectors:
        return None
    return separator.join(selectors.extract())

def extract_article(raw_html=None):
    return extract_article.goose.extract(raw_html=raw_html).infos
extract_article.goose = Goose({'stopwords_class': StopWordsChinese})

