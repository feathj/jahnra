from unicodecsv import DictReader as dr
from random import shuffle
from sets import Set

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import Perceptron
# from sklearn.linear_model import RidgeClassifier
# from sklearn.linear_model import PassiveAggressiveClassifier
# from sklearn.neighbors import KNeighborsClassifier


class Jahnra:

    def __init__(self, db_path):
        # init
        self.classifier = MultinomialNB()
        # self.classifier = RandomForestClassifier(n_estimators=100)
        # self.classifier = Perceptron(n_iter=50)
        # self.classifier = RidgeClassifier(tol=1e-2, solver="lsqr")
        # self.classifier = PassiveAggressiveClassifier(n_iter=50)
        # self.classifier = KNeighborsClassifier(n_neighbors=10)

        self.count_vectorizer = CountVectorizer(
                ngram_range=(1, 3),
                analyzer="word",
                tokenizer=None,
                preprocessor=None,
                stop_words=None,
                max_features=5000)

        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop = Set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')

        # train
        self.__train_classifier(db_path)

    def __clean_text(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = [self.stemmer.stem(t.lower()) for t in tokens if not self.stemmer.stem(t.lower()) in self.stop]
        return ' '.join(tokens)

    def __train_classifier(self, db_path):
        # load
        print 'loading'
        data = {}
        with open('db.csv', 'r') as db_file:
            reader = dr(db_file, encoding='utf-8')
            for row in reader:
                if row['genre'] not in data:
                    data[row['genre']] = []
                data[row['genre']].append({
                    'label': row['genre'],
                    'text': self.__clean_text(row['lyrics'])
                    })

        # train
        print 'training'
        train_data = []
        test_data = []
        for label, records in data.iteritems():
            shuffle(records)
            split_index = int(round(len(records) * 0.7))
            train_data.extend(records[:split_index])
            test_data.extend(records[split_index:])

        counts = self.count_vectorizer.fit_transform([d['text'] for d in train_data])
        self.classifier.fit(counts, [d['label'] for d in train_data])

        # test
        print 'testing'
        num_correct = 0
        for d in test_data:
            result = self.predict(d['text'])
            if result == d['label']:
                num_correct += 1

        print '{0}/{1}'.format(num_correct, len(test_data))

    def predict(self, text):
        result = self.classifier.predict(self.count_vectorizer.transform([self.__clean_text(text)]))
        return result[0]

x = Jahnra('./db.csv')
