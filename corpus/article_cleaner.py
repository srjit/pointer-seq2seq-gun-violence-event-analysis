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
    re_split_characters = "-|#|\+|\*|\n\n"
    

    sentences = re.split(re_split_characters, text)
    return sentences
    


def splittext_spacy(text):
    """
    
    Arguments:
    - `text`:
    """
    tokens = nlp(text, parse=True)
    return list(tokens.sents)



def filter_paras(paras):
    """
    
    Arguments:
    - `paras`:
    """
    final_paras = []

    for para in paras:
        for sentence in para:
            sl = len(str(sentence).split()) 

            if sl > 5 and sl < 200:
                ipdb.set_trace() # 
                final_paras.append(sentence)


    return final_paras


def tokenize(line):
    """
    
    Arguments:
    - `line`:
    """
    line = ''.join(ch for ch in line if category(ch)[0] != 'P')
    without_numbers = ' '.join(s for s in line.split() if not any(c.isdigit() for c in s))
    
    return line.lower().split()
    


cur.execute("""SELECT article from news_text""")
rows = cur.fetchall()


for article in rows:
    sentences_lynx = splittext_lynx(article[0])
    
    paragraphs = list(map(splittext_spacy, sentences_lynx))
    paragraphs = filter_paras(paragraphs)

