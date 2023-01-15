# import spacy
# from textblob import TextBlob
# from collections import Counter
# from spacy.lang.en.stop_words import STOP_WORDS
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# nlp = spacy.load("en_core_web_sm")
# analyzer = SentimentIntensityAnalyzer()


# async def bad_reputation_finder(company, text) -> list|None:
#     doc = nlp(text)
#     bad_text = []
#     for sent in doc.sents:
#         for token in sent:
#             if token.text == company:
#                 for child in token.children:
#                     sentiment = analyzer.polarity_scores(child.text)['compound']
#                     if sentiment < 0:
#                         bad_text.append(sent.text)
#     return bad_text if bad_text else None                   

# async def title_sentiment_analyzer(articles_text):
#     sentiment = TextBlob(articles_text).sentiment.polarity
#     return sentiment

# def summarizer_lite(text, ratio=0.3):
#     doc = nlp(text)
#     stopwords = STOP_WORDS
#     word_frequencies = Counter([token.text for token in doc if token.text not in stopwords])
#     most_common_words = word_frequencies.most_common(int(len(word_frequencies) * ratio))
#     summary = " ".join([pair[0] for pair in most_common_words])
#     return summary



import nltk
nltk.download("stopwords")
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("cirfproject-firebase-adminsdk-o9myp-0daa4e01f4.json")
firebase_admin.initialize_app(cred)

from firebase_admin import firestore

db = firestore.client()

# doc_ref.set({
#     "mit" : ["this", "is", "test", "data"]
# })

def risk_entities (list, company):
    
    negative_words = []
    for i in range(len(list)):
        
        sentence = list[i]
        
        # sia = SentimentIntensityAnalyzer()
        # scores = sia.polarity_scores(sentence)  
        #negative_words = [word for word in sentence.split() if scores["compound"] < 0 and word.lower() not in stop_words]
        blob = TextBlob(sentence)

        if blob.sentiment.polarity < 0:
            for word, tag in blob.tags:
                if tag == "NN" or tag == "JJ":
                    if TextBlob(word).sentiment.polarity < 0:
                        negative_words.append(word)

    doc_ref = db.collection("risk_entities").document(company) 
    # doc = doc_ref.get()

    # if doc.exists:

    doc_ref.set({f"{company}": set(negative_words)})     




