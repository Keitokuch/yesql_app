from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

class Tfidf():
    def __init__(self, max_df=0.3, min_df=0.00002):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self._tfidf = TfidfVectorizer(max_df=max_df, min_df = min_df,
                        lowercase=False, analyzer='word',
                        tokenizer=self._dummy_func, preprocessor=self._dummy_func,
                        token_pattern=None)

    def lemmatize(self, text):
        tokens = self.tokenizer.tokenize(text.lower())
        filtered = filter(lambda token: token not in self.stop_words, tokens)
        return [self.lemmatizer.lemmatize(w, self.get_wordnet_pos(w)) for w in filtered]

    def fit_transform(self, tokens):
        return self._tfidf.fit_transform(tokens)

    def transform(self, tokens):
        if isinstance(tokens, str):
            tokens = [self.lemmatize(tokens)]
        elif isinstance(tokens[0], str):
            tokens = [tokens]
        return self._tfidf.transform(tokens)

    @staticmethod
    def _dummy_func(x):
        return x

    @staticmethod
    def get_wordnet_pos(word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)
