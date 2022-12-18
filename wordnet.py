import nltk
from nltk.corpus.reader import wordlist
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


class Wordnet:

    def get_synsets(self, word):
        for synset in wordnet.synsets(word):
            print(synset.name())
            print(synset.definition())
            print(synset.examples())
            print("--------------------")

    def get_synonyms(self, word):
        if (wordnet.synsets(word)):
            first_synset = wordnet.synsets(word)[0]
            synset = wordnet.synset(first_synset.name())
            lemmas = synset.lemma_names()
            return lemmas
        return []
