from unicodecsv import DictReader as dr

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

data = {'labels': [], 'text': []}

with open('db.csv', 'r') as db_file:
    reader = dr(db_file, encoding='utf-8')
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words('english')
    stemmer = SnowballStemmer('english')

    for row in reader:
        tokens = tokenizer.tokenize(row['lyrics'])
        tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t not in stop]
        tokens = [stemmer.stem(t) for t in tokens]

        data['labels'].append(row['genre'])
        data['text'].append(' '.join(tokens))

count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(data['text'])

classifier = MultinomialNB()
classifier.fit(counts, data['labels'])

predictions = classifier.predict(count_vectorizer.transform(["No, I'm not bullish. It's like they're emboldened. They follow our planes, they circle our ships with their little boats, and they scream things at us. It is what happened -- it's not good. You would thought what the deal they made, which was a great deal for them and a horrible deal for us, that they would have had a warmth toward our country, and it's exactly the opposite. They lost respect because they can't believe anybody could be so stupid as to make a deal like that"]))

print predictions
