from spacy.language import Language
from spacy.tokens import Span

@Language.component("expand_person_entities")
def expand_person_entities(doc):
    new_ents = []
    for ent in doc.ents:
        # Only check for title if it's a person and not the first token
        if ent.label_ == "PERSON" and ent.start != 0:
            prev_token = doc[ent.start - 1]
            if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms.", "Mrs.", "Mrs"):
                new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
                new_ents.append(new_ent)
            else:
                new_ents.append(ent)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

def read_file(filename="harrypotter1_preprocessed.txt"):
    f = open(filename)

    text = ''
    for each in f:
        if "Page |" not in each:
            text += each
    f.close()

    text = text.replace('\r', '').replace('\n', ' ').replace('  ', ' ')

    return text