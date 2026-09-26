"""
Data Preprocessing Module
Responsible for cleaning and preparing raw job posting data for analysis.
"""
import pandas as pd
import numpy as np
import re

def clean_text(text):
    """
    Basic text cleaning: lowercase, remove non-alphanumeric characters (keep spaces),
    and remove extra whitespace.
    """
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_data(df):
    """
    Handles missing values and cleans text fields.
    """
    df = df.copy()
    
    # Text columns to clean
    text_cols = ['job_title', 'job_description', 'requirements', 'benefits', 'company_profile']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
            
    # Categorical columns to handle missing values
    cat_cols = ['employment_type', 'required_experience', 'required_education', 'salary_range', 'location']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
            
    # Numeric/Boolean columns: fill missing with 0
    num_cols = [
        'telecommuting', 'has_company_logo', 'has_company_profile',
        'payment_request', 'unrealistic_salary', 'urgency_language',
        'suspicious_contact', 'missing_company_info'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    return df
