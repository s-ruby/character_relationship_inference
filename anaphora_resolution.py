"""
update spacy requirements to 2.1.3
pip install neuralcoref --no-binary neuralcoref
re-install requirements
python -m spacy download en
"""

f = open("harrypotter1.txt")
f1 = open("harrypotter1_preprocessed.txt", 'w')

# # Load your usual SpaCy model (one of SpaCy English models)
import spacy
nlp = spacy.load('en')

# load NeuralCoref and add it to the pipe of SpaCy's model
import neuralcoref
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')

paragraph = ''
for line in f:
    if len(line.split()) != 0:
        paragraph += line
    else:
        doc = nlp(paragraph)
        doc._.has_coref
        f1.write(doc._.coref_resolved)
        f1.write('\n')
        paragraph = ''
        
    
f.close()
f1.close()



    