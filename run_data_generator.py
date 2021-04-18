import spacy
import json 
import random
import argparse
import numpy as np
from spacy.language import Language
from spacy.tokens import Span
from processors.utils import read_file
from processors.nlp_provider import NlpProvider
from processors.spacy_help_functions import get_entities, create_entity_pairs

def write_checkpoint(text: str, file='checkpoint.txt'):
    f = open(file, 'w')
    f.write(text)
    f.close()

def read_checkpoint(file='checkpoint.txt'):
    try:
        text = read_file(file)
        return int(text)
    except:
        return 0

def read_raw_example_files():
    friends = []
    foes = []
    neutrals = []
    with open('data/friends.json') as f:
        friends = json.load(f)
    with open('data/foes.json') as f:
        foes = json.load(f)
    with open('data/neutrals.json') as f:
        neutrals = json.load(f)

    return (friends, foes, neutrals)

def write_raw_example_files(friends, foes, neutrals):
    with open('data/friends.json', 'w') as outfile: 
        json.dump(friends, outfile)

    with open('data/foes.json', 'w') as outfile: 
        json.dump(foes, outfile)

    with open('data/neutrals.json', 'w') as outfile: 
        json.dump(neutrals, outfile)

def main():
    provider = NlpProvider() 
    doc = provider.process_file(args.text_file)

    (friends, foes, neutrals) = read_raw_example_files()
    
    checkpoint = read_checkpoint()

    try:
        for (i, sent) in enumerate(doc.sents):  
            
            if checkpoint > i:
                continue

            write_checkpoint(text=str(i))

            sentence_entity_pairs = create_entity_pairs(sent, ['PERSON'])
            
            for ep in sentence_entity_pairs:
                
                if ep[1][1] != 'PERSON' or ep[2][1] != 'PERSON':
                    continue    

                if not isinstance(ep[1][2][0], int) or not isinstance(ep[1][2][1], int) or not isinstance(ep[2][2][0], int) or not isinstance(ep[2][2][1], int):
                    continue
                    
                example = {
                    'id': 'example:' + str(i),
                    'docid': 'docid:' + str(i),
                    'relation': 'per:title',
                    'token': [token.text for token in sent],
                    'subj_start': ep[1][2][0],
                    'subj_end': ep[1][2][1],
                    'obj_start': ep[2][2][0],
                    'obj_end': ep[2][2][1],
                    'subj_type': 'PERSON',
                    'obj_type': 'PERSON',
                    'stanford_pos': [token.pos_ for token in sent],
                    'stanford_ner': [token.ent_type_ if token.ent_type_ != '' else '0' for token in sent],
                    'stanford_head': [token.head.i - sent.start for token in sent],
                    'stanford_deprel': [token.dep_ for token in sent],
                }

                print('Sentence')
                print('========')
                print(sent)
                print('========')
                print(ep[1], ep[2])
                label = input('\nDoes this indicate:\n\t[0] friend\n\t[1] foe\n\t[2] no relation\n\t[other] skip\n')
            
                if label == '0':
                    example['relation'] = 'per:friend'
                    friends.append(example)
                elif label == '1':
                    example['relation'] = 'per:foe'
                    foes.append(example)
                elif label == '2':
                    example['relation'] = 'no_relation'
                    neutrals.append(example)
            
                
                print('Current Lengths: \n\tFriends: ' + str(len(friends)) + '\n\tFoes: ' + str(len(foes)) + '\n\tNo Relation: ' + str(len(neutrals)))

        write_raw_example_files(friends, foes, neutrals)
    except KeyboardInterrupt:
        write_raw_example_files(friends, foes, neutrals)

def distribute_dataset():
    (friends, foes, neutrals) = read_raw_example_files()

    random.shuffle(friends)
    random.shuffle(foes)
    random.shuffle(neutrals)

    train = []
    test = []
    dev = []

    friend_parts = np.array_split(friends, 3)
    foe_parts = np.array_split(foes, 3)
    neutral_parts = np.array_split(neutrals, 3)

    train.extend(list(friend_parts[0]))
    train.extend(list(foe_parts[0]))
    train.extend(list(neutral_parts[0]))

    test.extend(list(friend_parts[1]))
    test.extend(list(foe_parts[1]))
    test.extend(list(neutral_parts[1]))

    dev.extend(list(friend_parts[2]))
    dev.extend(list(foe_parts[2]))
    dev.extend(list(neutral_parts[2]))

    with open('data/train.json', 'w') as outfile:
        json.dump(train, outfile)
    with open('data/test.json', 'w') as outfile:
        json.dump(test, outfile)
    with open('data/dev.json', 'w') as outfile:
        json.dump(dev, outfile)

    print('Successfully created training, test, and dev sets')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip_data_gen", default=False, type=bool, required=False)
    parser.add_argument("--text_file", default="anaphora_resolution/harrypotter1_final.txt", type=str, required=False)
    args = parser.parse_args()
    
    if not args.skip_data_gen:
        main() 
    distribute_dataset()
    