from ontology import Ontology


if __name__ == "__main__":
    ontology = Ontology()
    ontology.parse("./food.rdf")
    ontology.build_relations()
    ontology.print_relations()
    ontology.generate_questions()
