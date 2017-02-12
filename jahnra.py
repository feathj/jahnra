from unicodecsv import DictReader as dr
from random import shuffle
from sets import Set

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier


class Jahnra:
    DOCUMENT_THRESHOLD = 1000

    def __pipeline(self, classifier):
        return Pipeline([
            ('count_vectorizer', CountVectorizer(ngram_range=(1,  2))),
            ('tfidf_transformer', TfidfTransformer()),
            ('classifier', classifier)])

    def __init__(self, db_path, test=False):
        # init
        self.classifiers = {}
        self.classifiers['nb'] = self.__pipeline(MultinomialNB())
        # self.classifiers['rf'] = self.__pipeline(RandomForestClassifier(n_estimators=100))
        self.classifiers['pe'] = self.__pipeline(Perceptron(n_iter=50))
        self.classifiers['ri'] = self.__pipeline(RidgeClassifier(tol=1e-2, solver="lsqr"))
        self.classifiers['pg'] = self.__pipeline(PassiveAggressiveClassifier(n_iter=50))
        self.classifiers['kn'] = self.__pipeline(KNeighborsClassifier(n_neighbors=10))
        self.classifiers['sgd'] = self.__pipeline(SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42))

        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop = Set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')

        # train
        self.__train_classifiers(db_path, test)

    def __clean_text(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = [t.lower() for t in tokens]
        tokens = [self.stemmer.stem(t) for t in tokens]
        tokens = [t for t in tokens if t not in self.stop]
        return ' '.join(tokens)

    def __train_classifiers(self, db_path, test=False):
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
            for genre, records in data.iteritems():
                if len(records) >= Jahnra.DOCUMENT_THRESHOLD:
                    print '{0}: {1}'.format(genre, len(records))

        # train
        print 'training'
        train_data = []
        test_data = []
        for label, records in data.iteritems():
            if len(records) < Jahnra.DOCUMENT_THRESHOLD:
                continue
            if test:
                shuffle(records)
                split_index = int(round(len(records) * 0.7))
                train_data.extend(records[:split_index])
                test_data.extend(records[split_index:])
            else:
                train_data.extend(records)

        train_text = [d['text'] for d in train_data]
        train_labels = [d['label'] for d in train_data]

        test_text = [d['text'] for d in test_data]
        test_labels = [d['label'] for d in test_data]
        test_results = {}

        for classifier_label, classifier in self.classifiers.iteritems():
            print classifier_label
            classifier.fit(train_text, train_labels)
            if test:
                predictions = classifier.predict(test_text)
                correct_predictions = 0
                for index, val in enumerate(predictions):
                    if val == test_labels[index]:
                        correct_predictions += 1
                test_results[classifier_label] = (float(correct_predictions) / float(len(test_data))) * 100.0 
        if test:
            print test_results

    def predict(self, classifier, text):
        result = self.classifiers[classifier].predict([self.__clean_text(text)])
        return result[0]

# x = Jahnra('./db.csv', True)
