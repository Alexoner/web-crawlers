
from goose import Goose
from goose.text import StopWordsChinese


def safe_extract(selectorList, separator='\t'):
    if not selectorList:
        return None
    return separator.join(selectorList.extract())

def extract_article(raw_html=None):
    return extract_article.goose.extract(raw_html=raw_html).infos
extract_article.goose = Goose({'stopwords_class': StopWordsChinese})

