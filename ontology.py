import random
import re

import rdflib
from colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE
from util import split_by_capital_letter
from wordnet import Wordnet


class Ontology:
    def __init__(self):
        self.graph = rdflib.Graph()
        self.relations = []
        self.all_relations = []
        self.wordnet = Wordnet()

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
                if not str(subject).startswith("has"):
                    self.relations.append((subject, predicate, obj))
            if isinstance(subject, rdflib.term.BNode) and isinstance(
                obj, rdflib.term.BNode
            ):
                subject = str(subject).split("#")[-1]
                predicate = str(predicate).split("#")[-1]
                obj = str(obj).split("#")[-1]
                if predicate == "allValuesFrom":
                    self.all_relations.append((subject, predicate, obj))
            if isinstance(obj, rdflib.term.BNode):
                subject = str(subject).split("#")[-1]
                predicate = str(predicate).split("#")[-1]
                obj = str(obj).split("#")[-1]
                if predicate == "subClassOf":
                    self.all_relations.append((subject, predicate, obj))
            if isinstance(subject, rdflib.term.BNode):
                subject = str(subject).split("#")[-1]
                predicate = str(predicate).split("#")[-1]
                obj = str(obj).split("#")[-1]
                if obj.startswith("has") or predicate.startswith("has"):
                    self.all_relations.append((subject, predicate, obj))

    def parse_relationships(self):
        for (subject, predicate, obj) in self.all_relations:
            triple = ()
            if not isinstance(subject, rdflib.BNode) and predicate == "subClassOf":
                triple += (subject,)
                self.search_properties(obj, triple)

    def search_properties(self, b_node, triple):
        values = []
        for (subject, predicate, obj) in self.all_relations:
            if str(subject).__eq__(str(b_node)) and predicate == "allValuesFrom":
                next_subj = obj
                for (subject, predicate, obj) in self.all_relations:
                    if (
                        str(next_subj).__eq__(str(subject))
                        and predicate == "onProperty"
                    ):
                        triple += (obj,)
                        values = self.search_values(next_subj)

                line = ""
                if len(values) > 0:
                    for value in values:
                        line += str(value) + " "
                    triple += (line,)
                    self.relations.append(triple)

    def search_values(self, b_node):
        values = []
        for (subject, predicate, obj) in self.all_relations:
            if str(subject).__eq__(str(b_node)) and predicate == "hasValue":
                values.append(obj)
        return values

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

    def generate_questions_synonyms(self):
        while True:
            print("Would you like a new question? (y/n)")
            answer = input()
            if answer != "y":
                break
            else:
                type_of_question = random.randint(1, 2)
                pos = random.randint(0, len(self.relations) - 1)
                subject = split_by_capital_letter(self.relations[pos][0])
                predicate = split_by_capital_letter(self.relations[pos][1])
                obj = split_by_capital_letter(self.relations[pos][2])
                q_subject = ""
                q_obj = ""
                q_predicate = ""
                for word in subject:
                    syn = self.wordnet.get_random_syn(word)
                    if syn:
                        q_subject += syn.capitalize()
                    else:
                        q_subject += word
                for word in obj:
                    syn = self.wordnet.get_random_syn(word)
                    if syn:
                        q_obj += syn.capitalize()
                    else:
                        q_obj += word
                for word in predicate:
                    syn = self.wordnet.get_random_syn(word)
                    if syn:
                        q_predicate += syn.capitalize()
                    else:
                        q_predicate += word
                print(subject, q_subject)
                print(predicate, q_predicate)
                print(obj, q_obj)

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
                    self.validate_by_hypernyms(q_subject, answer, q_obj)
                    for (
                        subject,
                        predicate,
                        obj,
                    ) in (
                        self.relations
                    ):  # check for common synonyms between subject and query subject and between object and query object
                        if set(
                            [
                                syn
                                for word in split_by_capital_letter(q_subject)
                                for syn in self.wordnet.get_synonyms(word)
                            ]
                        ).issubset(
                            set(
                                [
                                    syn
                                    for word in split_by_capital_letter(subject)
                                    for syn in self.wordnet.get_synonyms(word)
                                ]
                            )
                        ) and set(
                            [
                                syn
                                for word in split_by_capital_letter(q_obj)
                                for syn in self.wordnet.get_synonyms(word)
                            ]
                        ).issubset(
                            set(
                                [
                                    syn
                                    for word in split_by_capital_letter(obj)
                                    for syn in self.wordnet.get_synonyms(word)
                                ]
                            )
                        ):
                            if (
                                set(
                                    [
                                        syn
                                        for word in split_by_capital_letter(answer)
                                        for syn in self.wordnet.get_synonyms(word)
                                    ]
                                ).issubset(
                                    set(
                                        [
                                            syn
                                            for word in split_by_capital_letter(
                                                predicate
                                            )
                                            for syn in self.wordnet.get_synonyms(word)
                                        ]
                                    )
                                )
                                or answer == predicate
                            ):
                                print(GREEN + BOLD + UNDERLINE + "Correct!" + ENDC)
                                break
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
                                break
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
                        if set(
                            [
                                syn
                                for word in split_by_capital_letter(q_subject)
                                for syn in self.wordnet.get_synonyms(word)
                            ]
                        ).issubset(
                            set(
                                [
                                    syn
                                    for word in split_by_capital_letter(subject)
                                    for syn in self.wordnet.get_synonyms(word)
                                ]
                            )
                        ) and set(
                            [
                                syn
                                for word in split_by_capital_letter(q_predicate)
                                for syn in self.wordnet.get_synonyms(word)
                            ]
                        ).issubset(
                            set(
                                [
                                    syn
                                    for word in split_by_capital_letter(predicate)
                                    for syn in self.wordnet.get_synonyms(word)
                                ]
                            )
                        ):
                            if (
                                set(
                                    [
                                        syn
                                        for word in split_by_capital_letter(answer)
                                        for syn in self.wordnet.get_synonyms(word)
                                    ]
                                ).issubset(
                                    set(
                                        [
                                            syn
                                            for word in split_by_capital_letter(obj)
                                            for syn in self.wordnet.get_synonyms(word)
                                        ]
                                    )
                                )
                                or answer == obj
                            ):
                                print(GREEN + BOLD + UNDERLINE + "Correct!" + ENDC)
                                break
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
                                break

    def validate_by_hypernyms(self, q_subject, answer, q_obj):
        q_subject_h = set(
            [
                hypernym
                for word in split_by_capital_letter(q_subject)
                for hypernym in self.wordnet.get_hypernyms(word)
            ]
        )

        q_obj_h = set(
            [
                hypernym
                for word in split_by_capital_letter(q_obj)
                for hypernym in self.wordnet.get_hypernyms(word)
            ]
        )

        for (subject, predicate, obj) in self.relations:
            subject_h = set(
                [
                    hypernym
                    for word in split_by_capital_letter(subject)
                    for hypernym in self.wordnet.get_hypernyms(word)
                ]
            )

            obj_h = set(
                [
                    hypernym
                    for word in split_by_capital_letter(obj)
                    for hypernym in self.wordnet.get_hypernyms(word)
                ]
            )

            if subject_h & q_subject_h and obj_h & q_obj_h:
                if predicate == answer:
                    print(
                        "Validated by hypernyms: ",
                        subject_h & q_subject_h,
                        " and ",
                        obj_h & q_obj_h,
                    )
                    break
