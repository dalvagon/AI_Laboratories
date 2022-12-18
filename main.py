from ontology import Ontology
from wordnet import Wordnet

if __name__ == "__main__":
    ontology = Ontology()
    ontology.parse("./food.rdf")
    ontology.build_relations()
    ontology.parse_relationships()
    ontology.print_relations()
    ontology.generate_questions_synonyms()

    wordnet = Wordnet()
    #input_word = input("Enter a word: ")
    #wordnet.getSynsets(input_word)
   # wordnet.getSynoyms(input_word)
