import pandas as pd
import spacy
from spacy.language import EntityRecognizer



__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

nlp = spacy.load('en', entity=False, parser=False)
ner = EntityRecognizer(nlp.vocab, entity_types=['PERSON'])



def get_named_entities(text):
    """
    """
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.label_, ent.text)
#    doc.ents = []

    import ipdb
    ipdb.set_trace()
    pass


input_document = "cleaned_docs.csv"
data = pd.read_csv(input_document, sep="\t", header=None)
data.columns = ["url", "article"]

data['entities'] = data.article.apply(lambda x: get_named_entities(x))


