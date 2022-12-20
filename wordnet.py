import random
import nltk
from nltk.corpus.reader import wordlist
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from util import replace_underscore


class Wordnet:
    SYNSET_INDEX = 0

    def print_synsets(self, word):
        synsets = wordnet.synsets(word) or []

        for syn in synsets:
            print("Synset: " + str(syn))
            print("Lemmas: " + str(syn.lemma_names()) + "\n")

    def get_synonyms(self, word):
        syns = wordnet.synonyms(word)
        if syns:
            return [
                replace_underscore(syn).capitalize() for syn in syns[self.SYNSET_INDEX]
            ]

        return []

    def get_hypernyms(self, word):
        syns = wordnet.synsets(word)

        if syns:
            hypernyms = syns[self.SYNSET_INDEX].hypernyms()
            return [
                replace_underscore(hypernym.name().split(".")[0].capitalize())
                for hypernym in hypernyms
            ]

        return []

    def get_hyponyms(self, word):
        syns = wordnet.synsets(word)

        if syns:
            hyponyms = syns[self.SYNSET_INDEX].hyponyms()
            return [
                replace_underscore(hyponym.name().split(".")[0].capitalize())
                for hyponym in hyponyms
            ]

        return []

    def get_random_syn(self, word):
        syns = self.get_synonyms(word)
        if any(syns):
            return random.choice(self.get_synonyms(word))

        return ""
