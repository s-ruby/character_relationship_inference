import nltk
# nltk.download('punkt')

    
def tag_characters(book_num, write_file):

    file = open(f"/Users/serenakillion/Desktop/code/character_relationship_inference/anaphora_resolution/harrypotter{book_num}_final.txt")

    text = ''
    "Page |"

    for x in file:
        if "Page |" not in x:
            text+= x
    # print(temp)
    proc = []
    final = []

    characters = ["Harry", "Riddle", "Voldemort", "Quirrell", "the Dark Lord", "Ron", "Hermione", "Malfoy", "Draco", "Dumbledore", "Snape", "Hagrid", "Ginny", "Dudleyl",
                "Neville", "McGongall", "Rita", "Umbridge", "Cornelius", "Ballatrix", "Lestrange", "Lucius", "Weasley", "Cho"]

    for ch in characters:
        text = text.replace(ch, f"<PER>{ch}</PER>")

    a_list = nltk.tokenize.sent_tokenize(text)

    for a in a_list:
        if a.count('PER') > 2:
            final.append(a)

    file.close()

    wf = open(write_file, 'a')
    for sent in final:
        wf.write(sent + '\n')

    wf.close()
    

book_num = input("Enter harry poter book# or all: ")

if book_num != "all":
    write_file = f"hp{book_num}_processed_tag.txt"
    tag_characters(book_num, write_file)
else:
    write_file = f"hp-all_processed_tag.txt"
    for i in range(1, 8):
        tag_characters(str(i), write_file)