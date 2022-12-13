import random
import rdflib
from colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE


class Ontology:
    def __init__(self):
        self.graph = rdflib.Graph()
        self.relations = []

    def parse(self, file):
        self.graph.parse(file, format="application/rdf+xml")

    def build_relations(self):
        for subject, predicate, obj in self.graph.triples((None, None, None)):
            if (
                not isinstance(subject, rdflib.term.BNode)
                and not isinstance(obj, rdflib.term.BNode)
                and not isinstance(predicate, rdflib.term.BNode)
            ):
                subject = str(subject).split("#")[-1]
                predicate = str(predicate).split("#")[-1]
                obj = str(obj).split("#")[-1]
                self.relations.append((subject, predicate, obj))

    def print_relations(self):
        for (subject, predicate, obj) in self.relations:
            print(
                BOLD
                + CYAN
                + subject
                + ENDC
                + " is in relation of "
                + BOLD
                + YELLOW
                + predicate
                + ENDC
                + " with "
                + BOLD
                + MAGENTA
                + obj
                + ENDC
            )

    def generate_questions(self):
        while True:
            print("Would you like a new question? (y/n)")
            answer = input()
            if answer != "y":
                break
            else:
                type_of_question = random.randint(1, 2)
                pos = random.randint(0, len(self.relations) - 1)
                q_subject = self.relations[pos][0]
                q_predicate = self.relations[pos][1]
                q_obj = self.relations[pos][2]
                if type_of_question == 1:
                    print(
                        "What is the relation between "
                        + BOLD
                        + CYAN
                        + q_subject
                        + ENDC
                        + " and "
                        + BOLD
                        + MAGENTA
                        + q_obj
                        + ENDC
                        + "?"
                    )
                    answer = input()
                    for (subject, predicate, obj) in self.relations:
                        if subject == q_subject and obj == q_obj:
                            if predicate == answer:
                                print(GREEN + BOLD + UNDERLINE + "Correct!" + ENDC)
                            else:
                                print(
                                    RED
                                    + BOLD
                                    + UNDERLINE
                                    + "Incorrect!"
                                    + ENDC
                                    + " The correct answer is "
                                    + BOLD
                                    + YELLOW
                                    + predicate
                                    + ENDC
                                )
                else:
                    print(
                        "Who is related to "
                        + BOLD
                        + CYAN
                        + q_subject
                        + ENDC
                        + " with "
                        + BOLD
                        + YELLOW
                        + q_predicate
                        + ENDC,
                        " relation?",
                    )
                    answer = input()
                    for (subject, predicate, obj) in self.relations:
                        if subject == q_subject and predicate == q_predicate:
                            if obj == answer:
                                print(GREEN + BOLD + UNDERLINE + "Correct!" + ENDC)
                            else:
                                print(
                                    RED
                                    + BOLD
                                    + UNDERLINE
                                    + "Incorrect!"
                                    + ENDC
                                    + " The correct answer is "
                                    + BOLD
                                    + MAGENTA
                                    + obj
                                    + ENDC
                                )
