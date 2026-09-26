import pandas as pd
import numpy as np
import os
import random

def generate_demo_dataset(output_path="data/raw/demo_jobs.csv", num_samples=500, random_state=42):
    """
    Generates a synthetic demo dataset for development and UI testing ONLY.
    This is NOT a real-world dataset. It contains artificial patterns so the 
    model has something to learn from during the development phase.
    """
    np.random.seed(random_state)
    random.seed(random_state)
    
    data = []
    
    # Simple word pools
    legit_titles = ["Software Engineer", "Marketing Manager", "Data Analyst", "Customer Support Representative", "HR Specialist"]
    fraud_titles = ["DATA ENTRY WORK FROM HOME", "EARN $500/DAY QUICK", "URGENT HIRING NO EXPERIENCE", "Virtual Assistant - Easy Pay"]
    
    legit_descriptions = [
        "We are looking for a dedicated professional to join our team. Excellent benefits and growth opportunities.",
        "Join our fast-growing startup. You will be responsible for day-to-day operations and collaborating with the team.",
        "Seeking an experienced individual to handle complex projects and deliver high-quality results."
    ]
    
    fraud_descriptions = [
        "Work from home and earn thousands! No experience needed. Just pay a small registration fee.",
        "URGENTLY hiring! Send your bank details immediately to secure this position. Unlimited earning potential.",
        "Easy money! Just forward emails and make $1000 a week. Contact via Telegram only."
    ]
    
    for i in range(num_samples):
        # 20% fraudulent, 80% legitimate
        is_fraud = np.random.choice([0, 1], p=[0.8, 0.2])
        
        if is_fraud:
            title = random.choice(fraud_titles)
            desc = random.choice(fraud_descriptions)
            req = "No experience necessary."
            ben = "Unlimited income."
            comp = "" # often missing
            has_logo = np.random.choice([0, 1], p=[0.9, 0.1])
            has_profile = np.random.choice([0, 1], p=[0.85, 0.15])
            pay_req = np.random.choice([0, 1], p=[0.3, 0.7]) # Highly correlated
            urgency = np.random.choice([0, 1], p=[0.2, 0.8])
            suspicious_contact = np.random.choice([0, 1], p=[0.1, 0.9])
            missing_info = np.random.choice([0, 1], p=[0.1, 0.9])
            unrealistic_salary = np.random.choice([0, 1], p=[0.2, 0.8])
        else:
            title = random.choice(legit_titles)
            desc = random.choice(legit_descriptions)
            req = "Bachelor's degree and 2+ years of experience."
            ben = "Health, Dental, 401k."
            comp = "We are an established industry leader committed to innovation."
            has_logo = np.random.choice([0, 1], p=[0.1, 0.9])
            has_profile = np.random.choice([0, 1], p=[0.1, 0.9])
            pay_req = 0 # Legit jobs rarely ask for payment
            urgency = np.random.choice([0, 1], p=[0.8, 0.2])
            suspicious_contact = np.random.choice([0, 1], p=[0.95, 0.05])
            missing_info = np.random.choice([0, 1], p=[0.9, 0.1])
            unrealistic_salary = 0
            
        # Introduce some missing values randomly
        if random.random() < 0.1: title = np.nan
        if random.random() < 0.1: desc = np.nan
        
        row = {
            "job_title": title,
            "job_description": desc,
            "requirements": req,
            "benefits": ben,
            "company_profile": comp,
            "telecommuting": np.random.choice([0, 1], p=[0.7, 0.3]),
            "has_company_logo": has_logo,
            "has_company_profile": has_profile,
            "employment_type": random.choice(["Full-time", "Part-time", "Contract", np.nan]),
            "required_experience": random.choice(["Entry level", "Mid-Senior level", "Executive", np.nan]),
            "required_education": random.choice(["Bachelor's Degree", "High School or equivalent", "Unspecified", np.nan]),
            "salary_range": random.choice(["$50k-$70k", "$100k+", np.nan]),
            "location": random.choice(["New York, NY", "Remote", "London, UK", "Unknown"]),
            "payment_request": pay_req,
            "unrealistic_salary": unrealistic_salary,
            "urgency_language": urgency,
            "suspicious_contact": suspicious_contact,
            "missing_company_info": missing_info,
            "fraudulent": is_fraud
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} demo samples at {output_path}")

if __name__ == "__main__":
    generate_demo_dataset()
