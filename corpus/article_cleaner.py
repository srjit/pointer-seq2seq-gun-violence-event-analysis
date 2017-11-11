import re
import ipdb
import connector
from unicodedata import category
import nltk, string
import csv
import os
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

titles = ('Ms.', 'Mr.', 'Sgt.', 'Lt.')



def build_keywords(filepath):
    f = open(filepath, 'r')
    keywords = set()
    for line in f:
            if line[0] == '#':
                    continue
            else:
                    keywords.add(line.strip())
    f.close()
    return keywords



police_file = "police_keywords.txt"
kill_file = "kill_keywords.txt"

police_keywords, kill_keywords = build_keywords(police_file), build_keywords(kill_file)

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
                final_paras.append(sentence)


    return final_paras




    
def get_NE_ending_in_s(sentence):
    list_of_entity = []
    sent_tok = nltk.word_tokenize(sentence)
    sent_post_tag = nltk.pos_tag(sent_tok)
    entity = nltk.ne_chunk(sent_post_tag)   
    list_of_entity = [ " ".join(w for w, t in elt) for 
                      elt in entity if isinstance(elt, nltk.Tree)]

    

    return [entity for entity in list_of_entity 
                if entity.lower().endswith("s") or entity.startswith(titles)]




def tokenize(line):
    """
    
    Arguments:
    - `line`:
    """
    line = str(line)

    if any(s in line for s in police_keywords) or any(s in line for s in kill_keywords):
        filter1 = [ch for ch in line if category(ch)[0] != 'P']
        sentence =  "".join([s for s in filter1 if not any(c.isdigit() for c in s)])

        list_of_entity = get_NE_ending_in_s(sentence)


        ## if the entity starts with en element in list of titles crop the title part
        ## otherwise remove the final "s"
        for entity in list_of_entity:
            if entity.startswith(titles):
               import ipdb
               ipdb.set_trace()
               sentence = sentence.replace(entity, entity[entity.index('.')+1 : len(entity)])
            else:
                sentence = sentence.replace(entity, entity[0:len(entity)-1])

        return sentence.strip()

    
    

cur.execute("""SELECT url, article from news_text""")
rows = cur.fetchall()

i = 0

delete = """Drop table if exists clean_docs"""
cur.execute(delete)
cur.execute("Create Table clean_docs(url text, article text[]);")
conn.commit()


output_file = "cleaned_docs.csv"

if os.path.isfile(output_file):
    os.remove(output_file)

writer = csv.writer(open(output_file, "a+"), delimiter="\t")

for article in rows:
    sentences_lynx = splittext_lynx(article[1])
    
    paragraphs = list(map(splittext_spacy, sentences_lynx))
    paragraphs = filter_paras(paragraphs)
    print(i+1)
    sentences = list(map(tokenize,paragraphs))


    
    sentences = list(set([sentence for sentence in sentences if sentence is not None]))

    url = article[0]
    writer.writerow([url, sentences])
    
    i+=1
