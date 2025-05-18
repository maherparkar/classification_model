#
#
#
# import pandas as pd
# import nltk
# from nltk.tokenize import word_tokenize
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.pipeline import Pipeline, FeatureUnion
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, classification_report
# from sklearn.base import TransformerMixin
# import joblib
#
# # Download necessary NLTK resources
# nltk.download('punkt')
#
# # Define a tokenizer using NLTK
# def tokenize(text):
#     return word_tokenize(text)
#
#
# # Feature extraction function that checks for specific keywords
# def extract_features(text):
#     features = {}
#     # Phrases that might be specific to receipts
#     receipt_terms = ["receipt no", "receipt date", "payment method", "received with thanks"]
#     # Phrases that might be specific to discharge summaries
#     discharge_terms = ["discharge diagnosis", "follow-up", "medication prescribed", "patient was advised", "clinical summary", "treatment outcome"]
#     # Phrases that might be specific to lab reports
#     lab_terms = ["test results", "laboratory findings", "biomarker", "lab no", "manual no", "sample collectiondate", "report date" ,
#                  "report status" , "report status final" , "end of report" , "xray chest pa" ,"x-ray - chest pa view" ,
#                  "bronchoscopy", "brochoscopy + bal" ,"impression:"]
#
#     for term in receipt_terms:
#         features[f'receipt_{term.replace(" ", "_")}'] = term in text.lower()
#     for term in discharge_terms:
#         features[f'discharge_{term.replace(" ", "_")}'] = term in text.lower()
#     for term in lab_terms:
#         features[f'lab_{term.replace(" ", "_")}'] = term in text.lower()
#
#     return features
# class TextExtractor(TransformerMixin):
#     """Extract textual content for TfidfVectorizer."""
#     def fit(self, x, y=None):
#         return self
#
#     def transform(self, data):
#         return [item['text'] for item in data] if data else []
#
# class DictExtractor(TransformerMixin):
#     """Extract dictionary content for DictVectorizer."""
#     def fit(self, x, y=None):
#         return self
#
#     def transform(self, data):
#         return [item['features'] for item in data] if data else []
#
# # Custom transformer to select an item from a dictionary
# class ItemSelector(TransformerMixin):
#     def __init__(self, key):
#         self.key = key
#
#     def fit(self, x, y=None):
#         return self
#
#     def transform(self, data_dict):
#         # Add a check to make sure data_dict is a dictionary
#         if isinstance(data_dict, dict):
#             return data_dict[self.key]
#         else:
#             raise ValueError("ItemSelector expects a dictionary input, got: {}".format(type(data_dict)))
#
# # Read the dataset
# df = pd.read_excel(r"E:\recent_downloads\datset_medical.xlsx")
# df['text_column'] = df['text_column'].fillna('')
# df['text_label'] = df['text_label'].fillna('')
#
# # Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(
#     df['text_column'],
#     df['text_label'],
#     test_size=0.2,
#     random_state=42
# )
#
# # Create the feature matrix for training
# # Create the feature matrix for training and testing
# train_features = [{'text': text, 'features': extract_features(text)} for text in X_train]
# test_features = [{'text': text, 'features': extract_features(text)} for text in X_test]
#
#
# # Pipeline setup
# pipeline = Pipeline([
#     ('union', FeatureUnion(
#         transformer_list=[
#             ('text', Pipeline([
#                 ('extract_text', TextExtractor()),  # Ensure only text is passed to TfidfVectorizer
#                 ('tfidf', TfidfVectorizer(tokenizer=tokenize, stop_words='english', ngram_range=(1, 3), min_df=0.01)),
#             ])),
#             ('keywords', Pipeline([
#                 ('extract_keywords', DictExtractor()),  # Ensure only dict features are passed to DictVectorizer
#                 ('vect', DictVectorizer()),
#             ])),
#         ]
#     )),
#     ('clf', LogisticRegression(max_iter=1000)),
# ])
#
# # Grid search to find the best model parameters
# parameters = {
#     'union__text__tfidf__max_features': (1000, 5000, None),
#     'clf__C': (0.1, 1, 10),
# }
# grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, scoring='accuracy', cv=5)
# grid_search.fit(train_features, y_train)
#
# # Best model
# best_model = grid_search.best_estimator_
#
# # Prepare the feature matrix for testing
#
# predictions = best_model.predict(test_features)
#
# # Evaluate the model
# accuracy = accuracy_score(y_test, predictions)
# report = classification_report(y_test, predictions)
#
# print(f'Best Model Parameters: {grid_search.best_params_}')
# print(f'Accuracy: {accuracy:.2f}')
# print('Classification Report:')
# print(report)
#
# # Save the model
# model_filename = 'optimized_classifier_model_medical.joblib'
# joblib.dump(best_model, model_filename)
# print(f'Model saved to {model_filename}')
import os

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import nltk
from nltk.stem import SnowballStemmer
import joblib
from portal.packages.final_classifier.tokenizer import tokenize_and_stem

# Read Excel file
excel_path= os.getcwd() + "/datset_medical 1.xlsx"
df = pd.read_excel(excel_path)
df['text_column'] = df['text_column'].fillna('')
df['text_label'] = df['text_label'].fillna('')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df['text_column'],
    df['text_label'],
    test_size=0.2,
    random_state=42
)

# Create a pipeline with a TF-IDF vectorizer and Multinomial Naive Bayes classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words='english', ngram_range=(1, 2), min_df=0.01)),
    ('clf', MultinomialNB()),
])

# Set up the grid search
parameters = {
    'tfidf__max_features': (1000, 5000, None),
    'clf__alpha': (0.1, 1, 10),
}

grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, scoring='accuracy', cv=5)
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Make predictions with the best model
predictions = best_model.predict(X_test)

# Evaluate the performance
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print(f'Best Model Parameters: {grid_search.best_params_}')
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(report)

# Save the best model and vectorizer
model_filename = os.getcwd() + '/optimized_naive_bayes_model_medical.joblib'
joblib.dump(best_model, model_filename)
print(f'Model saved to {model_filename}')
