import spacy
from spanbert import SpanBERT
from spacy_help_functions import get_entities, create_entity_pairs

f = open("harrypotter1_preprocessed.txt")

para_by_char = []
paragraph = ''
text = ''
for sentence in f:
    text += sentence
    if len(sentence.split()) != 0:
        paragraph += sentence
    else:
        para_by_char.append(len(paragraph)+1)
        paragraph = ''
    

entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]
text = text.replace('\n', ' ')

# Load spacy model
nlp = spacy.load("en_core_web_lg")  

# Load pre-trained SpanBERT model
spanbert = SpanBERT("./pretrained_spanbert")  

# Apply spacy model to raw text (to split to sentences, tokenize, extract entities etc.)
doc = nlp(text)  


start_char = 0

for p in para_by_char:
    paragraph = doc.char_span(start_char, start_char + p)
    # print("\n\nProcessing entence: {}".format(sentence))
    # print("Tokenized sentence: {}".format([token.text for token in sentence]))
    
    try:
        assert (type(paragraph) == spacy.tokens.span.Span)
        ents = get_entities(paragraph, entities_of_interest)

        # print("spaCy extracted entities: {}".format(ents))
        
        # create entity pairs
        candidate_pairs = []
        sentence_entity_pairs = create_entity_pairs(paragraph, entities_of_interest)

        for ep in sentence_entity_pairs:
            # TODO: keep subject-object pairs of the right type for the target relation (e.g., Person:Organization for the "Work_For" relation)
            candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
            candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject
        

        # Classify Relations for all Candidate Entity Pairs using SpanBERT
        candidate_pairs = [p for p in candidate_pairs if not p["subj"][1] in ["DATE", "LOCATION"]]  # ignore subject entities with date/location type
    
        if len(candidate_pairs) != 0:
            relation_preds = spanbert.predict(candidate_pairs)  # get predictions: list of (relation, confidence) pairs

            # Print Extracted Relations

            for ex, pred in list(zip(candidate_pairs, relation_preds)):
                if pred[0] != "no_relation":
                    print("\nExtracted relations:")
                    print("\tSubject: {}\tObject: {}\tRelation: {}\tConfidence: {:.2f}".format(ex["subj"][0], ex["obj"][0], pred[0], pred[1]))
    except:
        print(text[start_char:start_char + p])
    
    start_char += p
    
f.close()
