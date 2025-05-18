import nltk
from nltk.stem import SnowballStemmer

nltk.download('punkt')
stemmer = SnowballStemmer('english')

def tokenize_and_stem(text):
    tokens = nltk.word_tokenize(text)

    return [stemmer.stem(t) for t in tokens]
