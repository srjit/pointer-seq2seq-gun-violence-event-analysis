import re
import connector

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


# Sentence Segmentation from Keith-et-al
# 2. Segment sentences in two steps:

# (a) Segment documents to fragments of text (typically, paragraphs) by splitting on
# Lynx’s representation of HTML paragraph, list markers, and other dividers:
# double newlines and the characters -,*, |, + and #.

# (b) Apply spaCy’s sentence segmenter (and NLP pipeline) to these paragraph-like
# text fragments.

import spacy
nlp = spacy.load('en')

conn = connector._getpostgres_connection()
cur = conn.cursor()


def splittext_lynx(text):
    """
    
    Arguments:
    - `text`:
    """
    re_split_characters = "-|#|+|\*|\n\n"
    sentences = re.split(re_split_characters, text)
    return sentences
    


def splittext_spacy(text):
    """
    
    Arguments:
    - `text`:
    """
    tokens = nlp(text, parse=True)
    return list(tokens.sents)




cur.execute("""SELECT url from news_text""")
rows = cur.fetchall()

for article in rows:
    sentences_lynx = splittext_lynx(article)
    sentences_spacy = splittext_spacy(article)

    print(sentences_lynx)
    print(sentences_spacy)

