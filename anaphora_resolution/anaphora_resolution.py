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

rare_words  = {'Petunia' : ['woman', 'Mistress Dursley', 'her'], 'Vernon' : ['man', 'Mister Dursley', 'him'],
               'Dudley' : ['man', 'boy'], 'Ron' : ['man', 'boy'], 'Hagrid' : ['man'], 'Albus Dumbledore' : ['Albus', 'headmaster', 'him', 'he'], 
               'Draco' : ['man', 'boy', 'Malfoy'], 'McGongall' : ['woman', 'McGongall', 'professor'], ' Snape' : ['man', 'Snape', 'him', 'he', 'professor', 'Severus'],
               'Professor Quirrell' : ['man', 'Quirrell'], 'Harry' : ['man', 'boy', 'Harry Potter', 'Potter', 'his'], 
               'Hermione' : ['she', 'woman', 'girl', 'Hermione granger', 'her'], 'Ginny' : ['she', 'her', 'woman', 'girl'], 
               "Argus Flich" : ['he', 'man'], 'Voldemort' : ['man', 'the Dark Lord', 'his', 'Lord Voldemort']}

neuralcoref.add_to_pipe(nlp, max_dist_match=1000, greedyness=.40)

hp_num = input("Enter harry potter book #: ")

nlp.get_pipe('neuralcoref').set_conv_dict(rare_words)

source_file = f"harrypotter{hp_num}.txt"
temp_file = f"harrypotter{hp_num}_clean.txt"

f = open(source_file)
f1 = open(temp_file, 'w')

"""replace punctuation with special char inside quotes so conversations are not treated as individual sentences"""
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

"""add punctuation back to conversation"""
def returnPunctFromQuotes(text):
    include = {'/' : '!', '$' : '.', '|' : '?'}
    for symb in include:
        text = text.replace(symb, include[symb])
    return text

posessive_pronouns = ["his", "her", "their"]

"""concatenate 's to character's name if available and remove ['s]"""
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
    text = text.replace("he's", "his")
    text = text.replace("she's", "her")
    text = text.replace("they's", "their")
    return text


text =  ""

"""neuralcoref has issues with mr. and mrs. names for some reason."""
footer = "Harry Potter and the Goblet of Fire - J.K. Rowling "
for line in f:
    if "Page |" not in line and line.upper() != line:
        line = line.replace(". . .", "")
        line = line.replace("...", "")
        line = line.replace("Mr. Dursley", "Vernon")
        line = line.replace("Mrs. Dursley", "Petunia")
        line = line.replace("You-Know-Who", "Voldemort").replace("the Dark Lord", "Voldemort")
        line = line.replace("Mr. Potter", "Potter")
        line = line.replace("Mrs. Weasley", "Molly")
        line = line.replace("Mr. Weasley", "Arthur")
        line = line.replace("Mrs.", "Mistress")
        line = line.replace("Mr.", "Mister")
        text += line

"""neuralcoref doesn't do posession correctly. insert ['s] to concatenate later to character's name."""
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

"""anaphora resolution at single sentence level"""
for sentence in sentences:
    doc = nlp(sentence)
    doc._.has_coref
    line = returnPunctFromQuotes(doc._.coref_resolved)
    f1.write(f"{line} \n")
    
f1.close()
print("single sentence completed")

final_file = f"harrypotter{hp_num}_final.txt"

f1 = open(temp_file)
f2 = open(final_file, "w")


"""anaphora resolution at two sentence level"""
sentences = []
for line in f1:
    line = line.replace("..", ".")
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
print("Final anaphora resolution completed")


f.close()
f1.close()
f2.close()


    