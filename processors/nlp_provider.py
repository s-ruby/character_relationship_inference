import spacy
from spacy.language import Language
from spacy.tokens import Span
from .utils import expand_person_entities, read_file

class NlpProvider:

    def __init__(self, model="en_core_web_lg"):
        self.model = model
        self.nlp = spacy.load(self.model)  
        self.nlp.max_length = 1338591
        self.nlp.add_pipe("expand_person_entities", after="ner")
    
    def get_nlp(self):
        return self.nlp

    def process_file(self, filename: str):
        return self.nlp(read_file(filename))
