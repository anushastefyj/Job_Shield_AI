"""
Model Training Module
Responsible for training the Machine Learning models (Logistic Regression & Random Forest),
evaluating them, and saving the best model and pipeline.
"""
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.pipeline import Pipeline

from src.data_preprocessing import preprocess_data
from src.feature_engineering import build_feature_pipeline
from src.generate_demo_data import generate_demo_dataset

def train_and_evaluate():
    # 1. Check if dataset exists, if not generate it
    data_path = "data/raw/demo_jobs.csv"
    if not os.path.exists(data_path):
        print("Demo dataset not found. Generating...")
        generate_demo_dataset(data_path, num_samples=600)
        
    df = pd.read_csv(data_path)
    
    # 2. Preprocessing
    print("Preprocessing data...")
    df_clean = preprocess_data(df)
    
    # 3. Train-Test Split (stratified)
    X = df_clean.drop(columns=['fraudulent'])
    y = df_clean['fraudulent']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Build feature pipeline
    feature_pipeline = build_feature_pipeline()
    
    # 5. Train two models
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    best_f1 = 0
    best_model_name = ""
    best_pipeline = None
    
    print("\nEvaluating Models:")
    print("-" * 50)
    for name, model in models.items():
        # Create full pipeline (Features + Model)
        full_pipeline = Pipeline([
            ('features', feature_pipeline),
            ('classifier', model)
        ])
        
        # Train
        full_pipeline.fit(X_train, y_train)
        
        # Predict on test
        y_pred = full_pipeline.predict(X_test)
        
        # Evaluate actual metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"Model: {name}")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  Confusion Matrix:\n{cm}\n")
        
        # Select best model based on F1-Score (balances precision and recall)
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = full_pipeline
            
    print("-" * 50)
    print(f"Selected Model: {best_model_name} (Highest F1-Score: {best_f1:.4f})")
    
    # 6. Save the selected pipeline
    os.makedirs("models", exist_ok=True)
    model_path = "models/best_model_pipeline.joblib"
    joblib.dump(best_pipeline, model_path)
    print(f"Model saved successfully to {model_path}")
    print("\nTraining completed.")

if __name__ == "__main__":
    train_and_evaluate()
