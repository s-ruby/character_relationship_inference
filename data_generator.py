import spacy
import json 
from spacy_help_functions import get_entities, create_entity_pairs
from spacy.language import Language
from spacy.tokens import Span
from processors.utils import read_file
from processors.nlp_provider import NlpProvider

def main():
    # Load spacy model
    provider = NlpProvider() 
    doc = provider.process_file("harrypotter1_preprocessed.txt")

    friends = []
    foes = []
    neutrals = []

    for (i, sent) in enumerate(doc.sents):  

        sentence_entity_pairs = create_entity_pairs(sent, ["PERSON"])
        
        for ep in sentence_entity_pairs:
            
            entity1 = ep[1]
            entity2 = ep[2]
            rng_entity1 = entity1[2]
            rng_entity2 = entity2[2]

            if entity1[1] == "PERSON" and entity2[1] == "PERSON":
                
                if entity1[2][0] - 1 >= 0 and sent[entity1[2][0] - 1].text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
                    rng_entity1 = (entity1[2][0] - 1, entity1[2][0])
                
                if entity2[2][0] - 1 >= 0 and sent[entity2[2][0] - 1].text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
                    rng_entity2 = (entity2[2][0] - 1, entity2[2][0])
                    
                named_entities = []
                for token in sent:
                    if token.ent_type_ == "PERSON":
                        named_entities.append(token.i) 

                example = {
                    "id": "example:" + str(i),
                    "docid": "docid:" + str(i),
                    "relation": "per:title",
                    "token": [token.text for token in sent],
                    "subj_start": rng_entity1[0],
                    "subj_end": rng_entity1[1],
                    "obj_start": rng_entity2[0],
                    "obj_end": rng_entity2[1],
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
                print(entity1, rng_entity1, entity2, rng_entity2)
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
                
                print(len(friends), len(foes), len(neutrals))



    with open("data/friends.json", "w") as outfile: 
        json.dump(friends, outfile)

    with open("data/foes.json", "w") as outfile: 
        json.dump(foes, outfile)

    with open("data/neutrals.json", "w") as outfile: 
        json.dump(neutrals, outfile)

if __name__ == '__main__':
    main() 