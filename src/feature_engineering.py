"""
Feature Engineering Module
Responsible for extracting relevant ML features (e.g., NLP vectors, text lengths) from the cleaned data.
"""
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class TextCombiner(BaseEstimator, TransformerMixin):
    """
    Combines multiple text columns into a single 'combined_text' column.
    """
    def __init__(self, text_cols):
        self.text_cols = text_cols
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        X = X.copy()
        X['combined_text'] = X[self.text_cols].astype(str).agg(' '.join, axis=1)
        return X[['combined_text']]

def build_feature_pipeline():
    """
    Builds a Scikit-Learn ColumnTransformer pipeline to handle:
    1. Text features (via TF-IDF)
    2. Categorical features (via One-Hot Encoding)
    3. Boolean/Numeric features (passthrough)
    """
    text_cols = ['job_title', 'job_description', 'requirements', 'benefits', 'company_profile']
    cat_cols = ['employment_type', 'required_experience', 'required_education', 'salary_range', 'location']
    num_cols = [
        'telecommuting', 'has_company_logo', 'has_company_profile',
        'payment_request', 'unrealistic_salary', 'urgency_language',
        'suspicious_contact', 'missing_company_info'
    ]

    # Pipeline for text
    text_pipeline = Pipeline([
        ('combiner', TextCombiner(text_cols=text_cols)),
        # we extract single column to pass to tfidf
        ('tfidf', ColumnTransformer([
            ('tfidf_vec', TfidfVectorizer(max_features=1000, stop_words='english'), 'combined_text')
        ]))
    ])

    # Combine everything
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', text_pipeline, text_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', 'passthrough', num_cols)
        ]
    )
    
    return preprocessor
