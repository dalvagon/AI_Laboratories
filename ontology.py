import random

import rdflib

g = rdflib.Graph()

g.parse("food.rdf", format='application/rdf+xml')
relations = []
for subject, predicate, obj in g.triples((None, None, None)):
    if not isinstance(subject, rdflib.term.BNode) and \
            not isinstance(obj, rdflib.term.BNode) and \
            not isinstance(predicate, rdflib.term.BNode):
        subject = str(subject).split('#')[-1]
        predicate = str(predicate).split('#')[-1]
        obj = str(obj).split('#')[-1]

        # ex 2
        print(subject, " is in relation ", predicate, " with ", obj)

        # ex 3
        relations.append((subject, predicate, obj))

# generate questions

while True:
    print("Do you want next question? (y/n)")
    answer = input()
    if answer == 'n':
        break
    else :
        pos = random.randint(0, len(relations) - 1)
        print("What is the relation between ", relations[pos][0], " and ", relations[pos][2], "?")
        answer = input()
        for triple in relations:
            if triple[0] == relations[pos][0] and triple[2] == relations[pos][2]:
                if triple[1] == answer:
                    print("Correct!")
                else:
                    print("Incorrect! The correct answer is ", triple[1])

