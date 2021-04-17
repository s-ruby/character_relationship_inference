"""
update spacy requirements to 2.1.3
pip install neuralcoref --no-binary neuralcoref
re-install requirements
python -m spacy download en
"""

import string
import nltk
# nltk.download('punkt')
import spacy
import neuralcoref

nlp = spacy.load('en')

rare_words  = {'Petunia' : ['woman', 'Mrs. Dursley', 'her'], 'Vernon' : ['man', 'Mr. Dursley', 'him'],
               'Dudley' : ['man', 'boy'], 'Ron' : ['man', 'boy'], 'Hagrid' : ['man'], 'Albus Dumbledore' : ['Albus', 'headmaster', 'him', 'he'], 
               'Draco' : ['man', 'boy'], 'Professor McGongall' : ['woman', 'McGongall'], 'Professor Snape' : ['man', 'Snape', 'him', 'he'],
               'Professor Quirrell' : ['man', 'Quirrell'], 'Harry' : ['man', 'boy', 'Harry Potter', 'Potter', 'him', 'he'], 
               'Hermione' : ['woman', 'girl', 'Hermione Granger', 'her']}
neuralcoref.add_to_pipe(nlp, max_dist=100)

nlp.get_pipe('neuralcoref').set_conv_dict(rare_words)
f = open("harrypotter1.txt")
f1 = open("harrypotter1_clean.txt", 'w')

def removePunctFromQuotes(text):
    returnText = ""
    count = 0
    quoteStart = 0
    start = 0
    numQuotes = text.count('“')
    while count < numQuotes:
        quoteStart = text.find('“', quoteStart)
        if quoteStart == -1:
            break
        quoteEnd = text.find('”', quoteStart + 1)
        wordsSpoken = text[quoteStart:quoteEnd + 1]
        exclude = {'!' : '/', '.' : '$', '?' : '|'}
        for punct in exclude:
            wordsSpoken = wordsSpoken.replace(punct, exclude[punct])
        returnText += text[start:quoteStart] + wordsSpoken
        quoteStart = quoteEnd + 1
        start = quoteStart
        count += 1
    return returnText + text[quoteStart::]

def returnPunctFromQuotes(text):
    include = {'/' : '!', '$' : '.', '|' : '?'}
    for symb in include:
        text = text.replace(symb, include[symb])
    return text
        
def addPossession(line):
    line_list = line.split()
    i = 0
    while i < len(line_list):
        if line_list[i] == "['s]": 
            if line_list[i-1] not in posessive_pronouns:
                line_list[i-1] = f"{line_list[i-1]}'s"
            line_list.pop(i)
        i += 1
    text = " ".join(line_list)
    text = text.replace("he's", "his").replace("she's", "her").replace("they's", "their")
    return " ".join(line_list)


        
posessive_pronouns = ["his", "her", "their"]

text =  ""

for line in f:
    line = line.replace(". . .", "...")
    line = line.replace("...", "")
    line = line.replace("Mr. Dursley", "Vernon")
    line = line.replace("Mrs. Dursley", "Petunia")
    line = line.replace("You-Know-Who", "Voldemort")
    line = line.replace("Mr. Potter", "Potter")
    text += line.lower()
    
i = 0
word_list = text.split()
for word in word_list:
    if word in posessive_pronouns:
        word_list.insert(i+1, "['s]")
    i += 1
        
    
text = " ".join(word_list)

text = removePunctFromQuotes(text)
tokens = nltk.sent_tokenize(text)

sentences = []
for t in tokens:
    sentences.append(t)


for sentence in sentences:
    doc = nlp(sentence)
    doc._.has_coref
    line = returnPunctFromQuotes(doc._.coref_resolved)
    f1.write(f"{line} \n")
    
f1.close()

f1 = open("harrypotter1_clean.txt")
    
f2 = open("harrypotter1_final.txt", "w")

sentences = []
for line in f1:
    sentences.append(line)

sentence_one = sentences[0]
for i in range(1, len(sentences)):
    joined = sentence_one + " " + sentences[i]
    doc = nlp(joined)
    doc._.has_coref
    tokens = nltk.sent_tokenize(doc._.coref_resolved)
    sent = returnPunctFromQuotes(tokens[0])
    sent = addPossession(sent)
    f2.write(f"{sent} \n")
    try: 
        sentence_one = tokens[1]
    except:
        print(sentences[i])
        print('\n')
        print(joined)
        print('\n')
        print(tokens)
        break
sent = returnPunctFromQuotes(tokens[1])
sent = addPossession(sent)
f2.write(sent)


f.close()
f1.close()
f2.close()


    