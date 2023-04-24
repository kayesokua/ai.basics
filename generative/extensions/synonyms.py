import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

def get_all_synonyms(mood_history):
    mood_options = []
    for word, count in mood_history.items():
        synonyms = []
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                synonyms.append(lemma.name())
        if synonyms:
             mood_options.extend(synonyms)
    return list(set(mood_options))
