"""
Prediction Module
Responsible for loading the trained model and generating predictions/risk scores for new job postings.
"""
import pandas as pd
import joblib
import os
from src.data_preprocessing import preprocess_data

def predict_job_risk(job_data_dict):
    """
    Given a dictionary of job posting features, predicts whether it is potentially fraudulent.
    Returns the predicted class, risk score (probability), and raw model output.
    """
    model_path = "models/best_model_pipeline.joblib"
    
    if not os.path.exists(model_path):
        return {
            "error": "Model not found. Please train the model first."
        }
        
    # Load the trained pipeline (which includes preprocessing, feature extraction, and classifier)
    pipeline = joblib.load(model_path)
    
    # Convert single dictionary to DataFrame
    df = pd.DataFrame([job_data_dict])
    
    # Apply the same cleaning steps
    df_clean = preprocess_data(df)
    
    # Predict probabilities
    # Classes are typically [0, 1] where 1 is fraudulent
    probabilities = pipeline.predict_proba(df_clean)[0]
    predicted_class_idx = pipeline.predict(df_clean)[0]
    
    risk_score = probabilities[1] # Probability of being class 1 (fraudulent)
    
    return {
        "predicted_class": int(predicted_class_idx),
        "risk_score": float(risk_score),
        "model_output": {
            "probability_legitimate": float(probabilities[0]),
            "probability_fraudulent": float(probabilities[1])
        }
    }

if __name__ == "__main__":
    # Example usage for testing prediction
    sample_job = {
        "job_title": "URGENT WORK FROM HOME NO EXPERIENCE",
        "job_description": "We need people to work immediately. Send your bank details.",
        "requirements": "None.",
        "benefits": "Make $5000 a week",
        "company_profile": "",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_company_profile": 0,
        "employment_type": "Full-time",
        "required_experience": "Entry level",
        "required_education": "Unspecified",
        "salary_range": "$100k+",
        "location": "Remote",
        "payment_request": 1,
        "unrealistic_salary": 1,
        "urgency_language": 1,
        "suspicious_contact": 1,
        "missing_company_info": 1
    }
    
    result = predict_job_risk(sample_job)
    print("Prediction Result:")
    print(result)
