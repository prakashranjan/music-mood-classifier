import nltk
from nltk.corpus import wordnet
#nltk.download()
syns = wordnet.synsets("regret")
print(syns[0].name())
print(syns[0].lemmas()[0].name())
print(syns[0].definition())
print(syns[0].examples())
synonyms = []
antonyms = []

for syn in wordnet.synsets("depression"):
    for l in syn.lemmas():
        print("l:", l)
        synonyms.append(l.name())
        #print("\n++++", l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
            #print("\n----",l.antonyms()[0].name())

print("\nsynonyms--> ", set(synonyms))
print("\nantonyms-->", set(antonyms))



w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print(w1.wup_similarity(w2))


w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('car.n.01')
print(w1.wup_similarity(w2))


w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('cat.n.01')
print(w1.wup_similarity(w2))