import spacy
import argparse
from spanbert import SpanBERT
from spacy_help_functions import get_entities, create_entity_pairs

def main(args):
    entities_of_interest = ["PERSON"]

    # Load spacy model
    provider = NlpProvider() 
    doc = provider.process_file("harrypotter1_preprocessed.txt")

    spanbert = SpanBERT("./" + args.model_dir, model_label_list=["no_relation", "per:friend", "per:foe"]) if args.model_dir == "model" else SpanBERT("./" + args.model_dir) 


    for sentence in doc.sents:  
        print("\n\nProcessing entence: {}".format(sentence))
        # print("Tokenized sentence: {}".format([token.text for token in sentence]))
        ents = get_entities(sentence, entities_of_interest)
        # print("spaCy extracted entities: {}".format(ents))
        
        # create entity pairs
        candidate_pairs = []
        sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)
        # for ep in sentence_entity_pairs:
        #     # TODO: keep subject-object pairs of the right type for the target relation (e.g., Person:Organization for the "Work_For" relation)
        #     candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
        #     candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject
        

        # Classify Relations for all Candidate Entity Pairs using SpanBERT
        for ep in sentence_entity_pairs:
            # for enty in entity_pair:  
            if ep[1][1] == "PERSON" and ep[2][1] == "PERSON":#if  correct entity pair for relation we are checking for -- add
                # print("true") 
                print("\n\nProcessing entence: {}".format(sentence))
                # print("Tokenized sentence: {}".format([token.text for token in sentence]))
                candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
                candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject
                break

        candidate_pairs = [p for p in candidate_pairs if not p["subj"][1] in ["DATE", "LOCATION"]]  # ignore subject entities with date/location type
        
        for p in candidate_pairs:
            print("Subject: {}\tObject: {}".format(p["subj"][0:2], p["obj"][0:2]))
                    
        if len(candidate_pairs) == 0:
            continue
        
        relation_preds = spanbert.predict(candidate_pairs)  # get predictions: list of (relation, confidence) pairs

        # Print Extracted Relations

        for ex, pred in list(zip(candidate_pairs, relation_preds)):
            if pred[0] != "no_relation":
                print("\nExtracted relations:")
                print("\tSubject: {}\tObject: {}\tRelation: {}\tConfidence: {:.2f}".format(ex["subj"][0], ex["obj"][0], pred[0], pred[1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", default="pretrained_spanbert", type=str, required=True)
    args = parser.parse_args()
    main(args)