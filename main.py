import spacy
import argparse
from spanbert import SpanBERT
from processors.spacy_help_functions import get_entities, create_entity_pairs
from processors.nlp_provider import NlpProvider
from collections import defaultdict

def main(args):
    results_dict = defaultdict(int)

    entities_of_interest = ["PERSON"]

    # Load spacy model
    provider = NlpProvider() 
    doc = provider.process_file(args.text_file)

    spanbert = SpanBERT("./" + args.model_dir, model_label_list=["no_relation", "per:friend", "per:foe"]) if args.model_dir == "span_bert_training_output" else SpanBERT("./" + args.model_dir) 


    for (i, sentence) in enumerate(doc.sents):  
        if i % 100 == 0:
            print("Completed " + str(i) + " sentences")
        ents = get_entities(sentence, entities_of_interest)
        
        # create entity pairs
        candidate_pairs = []
        sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)

        # Classify Relations for all Candidate Entity Pairs using SpanBERT
        for ep in sentence_entity_pairs:
            # for enty in entity_pair:  
            if ep[1][1] == "PERSON" and ep[2][1] == "PERSON":
                candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
                candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject
                break

        candidate_pairs = [p for p in candidate_pairs if not p["subj"][1] in ["DATE", "LOCATION"]]
                    
        if len(candidate_pairs) == 0:
            continue
        
        relation_preds = spanbert.predict(candidate_pairs)

        for ex, pred in list(zip(candidate_pairs, relation_preds)):
            if pred[0] != "no_relation":
                if pred[1] > args.min_conf:
                    results_dict[(ex["subj"][0], ex["obj"][0], pred[0])] += 1
                    print("\n")
                    print("Sentence: {}".format(sentence))
                    print("Extracted relations:")
                    print("\tSubject: {}\tObject: {}\tRelation: {}\tConfidence: {:.2f}".format(ex["subj"][0], ex["obj"][0], pred[0], pred[1]))
    print("\n Relation Counts")
    print(results_dict)               

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", default="pretrained_spanbert", type=str, required=True)
    parser.add_argument("--min_conf", default=0.4, type=float, required=True)
    parser.add_argument("--text_file", default="anaphora_resolution/harrypotter1_final.txt", type=str, required=False)
    args = parser.parse_args()
    main(args)