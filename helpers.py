import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pickle
import joblib



def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    # Convert to lowercase
    tokens = [word.lower() for word in tokens]
    # Remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    # Join tokens back into text
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def extract_reviews(data):
    extracted_reviews = []
    for review in data:
        review_dict = {
            'review_title': review['review_title'],
            'review_text': review['review_text']
        }
        extracted_reviews.append(review_dict)
    return extracted_reviews

def predict_label(review_title, review_text):
    # Load the Naive Bayes model
    naive_bayes_classifier = joblib.load('Final_Naive_Bayes.pkl')
    vectorizer = joblib.load('Final_Count_Vectorizer.pkl')
    
    # Preprocess the input data
    combined_text = ""
    combined_text += preprocess_text(review_title + ' ' + review_text) + ' '
    
    X_test = vectorizer.transform([combined_text])
    
    # Make predictions
    predicted_label = naive_bayes_classifier.predict(X_test)
    
    return predicted_label[0]