from ontology import Ontology
from util import replace_underscore
from wordnet import Wordnet

if __name__ == "__main__":
    ontology = Ontology()
    ontology.parse("./food.rdf")
    ontology.build_relations()
    ontology.parse_relationships()
    ontology.print_relations()
    ontology.generate_questions_synonyms()

    # wordnet = Wordnet()
    # print(wordnet.get_synonyms("compass"))
    # print(wordnet.get_synonyms("range"))
