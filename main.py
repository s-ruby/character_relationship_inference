import spacy
from spanbert import SpanBERT
from spacy_help_functions import get_entities, create_entity_pairs

# import file
f = open("/content/SpanBERT/harrypotter1.txt")

# clean text
text = ''
for each in f:
  if "Page |" not in each:
    text += each

text = text.replace('\r', '').replace('\n', '')

print(text)

entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]

# Load spacy model
nlp = spacy.load("en_core_web_lg")  

# Load pre-trained SpanBERT model
spanbert = SpanBERT("./pretrained_spanbert")  

# Apply spacy model to raw text (to split to sentences, tokenize, extract entities etc.)
doc = nlp(text)  

for sentence in doc.sents:  
    # print("\n\nProcessing entence: {}".format(sentence))
    # print("Tokenized sentence: {}".format([token.text for token in sentence]))
    ents = get_entities(sentence, entities_of_interest)
    # print("spaCy extracted entities: {}".format(ents))
    
    # create entity pairs
    candidate_pairs = []
    sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)
    for ep in sentence_entity_pairs:
        # TODO: keep subject-object pairs of the right type for the target relation (e.g., Person:Organization for the "Work_For" relation)
        candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
        candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject
    

    # Classify Relations for all Candidate Entity Pairs using SpanBERT
    candidate_pairs = [p for p in candidate_pairs if not p["subj"][1] in ["DATE", "LOCATION"]]  # ignore subject entities with date/location type
 
    if len(candidate_pairs) == 0:
        continue
    
    relation_preds = spanbert.predict(candidate_pairs)  # get predictions: list of (relation, confidence) pairs

    # Print Extracted Relations

    for ex, pred in list(zip(candidate_pairs, relation_preds)):
        if pred[0] != "no_relation":
          print("\nExtracted relations:")
          print("\tSubject: {}\tObject: {}\tRelation: {}\tConfidence: {:.2f}".format(ex["subj"][0], ex["obj"][0], pred[0], pred[1]))

