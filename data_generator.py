import spacy
import json 
from spacy_help_functions import get_entities, create_entity_pairs
from spacy.language import Language
from spacy.tokens import Span
from processors.utils import read_file
from processors.nlp_provider import NlpProvider
import random

def write_checkpoint(text: str, file="checkpoint.txt"):
    f = open(file, "w")
    f.write(text)
    f.close()

def read_checkpoint(file="checkpoint.txt"):
    try:
        text = read_file(file)
        return int(text)
    except:
        return 0

def main():
    try:
        # Load spacy model
        provider = NlpProvider() 
        doc = provider.process_file("harrypotter1_preprocessed.txt")

        friends = []
        foes = []
        neutrals = []
        with open('data/friends.json') as f:
            friends = json.load(f)
        with open('data/foes.json') as f:
            foes = json.load(f)
        with open('data/neutrals.json') as f:
            neutrals = json.load(f)
        
        checkpoint = read_checkpoint()
        print("checkpoint!", checkpoint)
        for (i, sent) in enumerate(doc.sents):  
            
            if checkpoint > i:
                continue

            write_checkpoint(text=str(i))

            sentence_entity_pairs = create_entity_pairs(sent, ["PERSON"])
            
            for ep in sentence_entity_pairs:
                
                if ep[1][1] != "PERSON" or ep[2][1] != "PERSON":
                    continue    

                example = {
                    "id": "example:" + str(i),
                    "docid": "docid:" + str(i),
                    "relation": "per:title",
                    "token": [token.text for token in sent],
                    "subj_start": ep[1][0],
                    "subj_end": ep[1][1],
                    "obj_start": ep[2][0],
                    "obj_end": ep[2][1],
                    "subj_type": "PERSON",
                    "obj_type": "PERSON",
                    "stanford_pos": [token.pos_ for token in sent],
                    "stanford_ner": [token.ent_type_ if token.ent_type_ != "" else "0" for token in sent],
                    "stanford_head": [token.head.i for token in sent],
                    "stanford_deprel": [token.dep_ for token in sent],
                }

                print("Sentence")
                print("========")
                print(sent)
                print("========")
                print(ep[1], ep[2])
                label = input("\nDoes this indicate:\n\t[0] friend\n\t[1] foe\n\t[2] no relation\n")
            
                if label == "0":
                    example["relation"] = "per:friend"
                    friends.append(example)
                elif label == "1":
                    example["relation"] = "per:foe"
                    foes.append(example)
                elif label == "2":
                    example["relation"] = "no_relation"
                    neutrals.append(example)
                
                print("Current Lengths: \n\tFriends: " + str(len(friends)) + "\n\tFoes: " + str(len(foes)) + "\n\tNo Relation: " + str(len(neutrals)))

        with open("data/friends.json", "w") as outfile: 
            json.dump(friends, outfile)

        with open("data/foes.json", "w") as outfile: 
            json.dump(foes, outfile)

        with open("data/neutrals.json", "w") as outfile: 
            json.dump(neutrals, outfile)
    except KeyboardInterrupt:
        with open("data/friends.json", "w") as outfile: 
            json.dump(friends, outfile)

        with open("data/foes.json", "w") as outfile: 
            json.dump(foes, outfile)

        with open("data/neutrals.json", "w") as outfile: 
            json.dump(neutrals, outfile)

if __name__ == '__main__':
    main() 
    