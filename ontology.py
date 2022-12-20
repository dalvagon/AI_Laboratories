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

    def generate_questions_synonyms(self):
        while True:
            print("Would you like a new question? (y/n)")
            answer = input()
            if answer != "y":
                break
            else:
                type_of_question = random.randint(1, 2)
                pos = random.randint(0, len(self.relations) - 1)
                subject = self.relations[pos][0]
                predicate = self.relations[pos][1]
                obj = self.relations[pos][2]
                words_in_subject = split_by_capital_letter(subject)
                words_in_predicate = split_by_capital_letter(predicate)
                words_in_obj = split_by_capital_letter(obj)
                q_subject = ""
                q_obj = ""
                q_predicate = ""
                for word in words_in_subject:
                    syn = self.wordnet.get_random_syn(word)
                    if syn:
                        q_subject += syn.capitalize()
                    else:
                        q_subject += word
                for word in words_in_predicate:
                    syn = self.wordnet.get_random_syn(word)
                    if syn:
                        q_predicate += syn.capitalize()
                    else:
                        q_predicate += word
                for word in words_in_obj:
                    syn = self.wordnet.get_random_syn(word)
                    if syn:
                        q_obj += syn.capitalize()
                    else:
                        q_obj += word

                print(words_in_subject, q_subject)
                print(words_in_predicate, q_predicate)
                print(words_in_obj, q_obj)

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
                    answer = input().lower().capitalize()
                    self.validate_predicate_by_hypernyms_and_hyponyms(
                        subject, predicate, obj, answer
                    )
                    for (s, p, o) in self.relations:
                        if s == subject and o == obj:
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
                                            for word in split_by_capital_letter(p)
                                            for syn in self.wordnet.get_synonyms(word)
                                        ]
                                    )
                                )
                                or answer == p.lower().capitalize()
                            ):
                                print(GREEN + BOLD + UNDERLINE + "Correct!" + ENDC)
                                break
                            else:
                                print(
                                    RED
                                    + BOLD
                                    + UNDERLINE
                                    + "!"
                                    + ENDC
                                    + " A correct answer is "
                                    + BOLD
                                    + YELLOW
                                    + p
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
                    answer = input().lower().capitalize()
                    self.validate_obj_by_hypernyms_and_hyponyms(
                        subject, predicate, obj, answer
                    )
                    for (s, p, o) in self.relations:
                        if s == subject and p == predicate:
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
                                            for word in split_by_capital_letter(o)
                                            for syn in self.wordnet.get_synonyms(word)
                                        ]
                                    )
                                )
                                or answer == o.lower().capitalize()
                            ):
                                print(GREEN + BOLD + UNDERLINE + "Correct!" + ENDC)
                                break
                            else:
                                print(
                                    RED
                                    + BOLD
                                    + UNDERLINE
                                    + "!"
                                    + ENDC
                                    + " A correct answer is "
                                    + BOLD
                                    + MAGENTA
                                    + o
                                    + ENDC
                                )

    def validate_predicate_by_hypernyms_and_hyponyms(
        self, subject, predicate, obj, answer
    ):
        for (s, p, o) in self.relations:
            if s == subject and o == obj:
                hypernyms = set(
                    [
                        hypernym
                        for word in split_by_capital_letter(p)
                        for hypernym in self.wordnet.get_hypernyms(word)
                    ]
                )
                hyponyms = set(
                    [
                        hyponym
                        for word in split_by_capital_letter(p)
                        for hyponym in self.wordnet.get_hyponyms(word)
                    ]
                )

                if answer in hypernyms:
                    print(
                        "Your asnwer "
                        + BOLD
                        + BLUE
                        + answer
                        + ENDC
                        + " is a hypernym of the correct answer "
                        + BOLD
                        + YELLOW
                        + p
                        + ENDC
                    )

                if answer in hyponyms:
                    print(
                        "Your asnwer "
                        + BOLD
                        + BLUE
                        + answer
                        + ENDC
                        + " is a hyponym of the correct answer "
                        + BOLD
                        + YELLOW
                        + p
                        + ENDC
                    )

    def validate_obj_by_hypernyms_and_hyponyms(self, subject, predicate, obj, answer):
        for (s, p, o) in self.relations:
            if s == subject and p == predicate:
                hypernyms = set(
                    [
                        hypernym
                        for word in split_by_capital_letter(o)
                        for hypernym in self.wordnet.get_hypernyms(word)
                    ]
                )
                hyponyms = set(
                    [
                        hyponym
                        for word in split_by_capital_letter(o)
                        for hyponym in self.wordnet.get_hyponyms(word)
                    ]
                )

                if answer in hypernyms:
                    print(
                        "Your asnwer "
                        + BOLD
                        + BLUE
                        + answer
                        + ENDC
                        + " is a hypernym of the correct answer "
                        + BOLD
                        + MAGENTA
                        + p
                        + ENDC
                    )

                if answer in hyponyms:
                    print(
                        "Your asnwer "
                        + BOLD
                        + BLUE
                        + answer
                        + ENDC
                        + " is a hyponym of the correct answer "
                        + BOLD
                        + MAGENTA
                        + p
                        + ENDC
                    )
