import rdflib

g = rdflib.Graph()

g.parse("food.rdf", format='application/rdf+xml')

for subject, predicate, obj in g.triples((None, None, None)):
    if not isinstance(subject, rdflib.term.BNode) and \
            not isinstance(obj, rdflib.term.BNode) and \
            not isinstance(predicate, rdflib.term.BNode):
        subject = str(subject).split('#')[-1]
        predicate = str(predicate).split('#')[-1]
        obj = str(obj).split('#')[-1]
        print(subject, " is in relation ", predicate, " with ", obj)
