import re

def analyze_risk(job_data, ml_probability):
    """
    Analyzes a job posting using rule-based heuristics and combines it with the ML model's probability.
    
    Args:
        job_data (dict): The job posting fields.
        ml_probability (float): The probability (0.0 to 1.0) of being fraudulent from the ML model.
        
    Returns:
        dict: A structured dictionary containing the final risk score, level, warning signs, 
              positive signs, and an explanation.
    """
    warning_signs = []
    positive_signs = []
    
    # 1. Prepare texts for analysis
    title = str(job_data.get('job_title', '')).lower()
    description = str(job_data.get('job_description', '')).lower()
    requirements = str(job_data.get('requirements', '')).lower()
    benefits = str(job_data.get('benefits', '')).lower()
    company_profile = str(job_data.get('company_profile', '')).lower()
    
    combined_text = f"{title} {description} {requirements} {benefits} {company_profile}"
    
    # Rule 1: Payment-related language
    payment_keywords = ['registration fee', 'training fee', 'security deposit', 'processing fee', 'pay to apply']
    found_payment = [kw for kw in payment_keywords if kw in combined_text]
    if found_payment:
        warning_signs.append({
            "indicator": "Payment Request Detected",
            "explanation": f"The posting contains suspicious payment-related terms: {', '.join(found_payment)}. Legitimate employers rarely ask candidates to pay fees."
        })
        
    # Rule 2: Unrealistic compensation or guarantees
    unrealistic_keywords = ['earn thousands', 'unlimited income', 'easy money', 'no experience necessary', 'no experience needed', 'get rich quick']
    found_unrealistic = [kw for kw in unrealistic_keywords if kw in combined_text]
    if found_unrealistic:
        warning_signs.append({
            "indicator": "Unrealistic Compensation/Promises",
            "explanation": f"Contains language often used in scams to lure applicants: {', '.join(found_unrealistic)}."
        })
        
    # Rule 3: Urgency or pressure
    urgency_keywords = ['immediate joining', 'limited seats', 'act immediately', 'send documents now', 'urgent hiring']
    found_urgency = [kw for kw in urgency_keywords if kw in combined_text]
    if found_urgency:
        warning_signs.append({
            "indicator": "High Pressure / Urgency",
            "explanation": f"Scams often create false urgency: {', '.join(found_urgency)}."
        })
        
    # Rule 4: Missing company information
    if not job_data.get('company_profile') or len(job_data.get('company_profile', '').strip()) < 10:
        warning_signs.append({
            "indicator": "Missing Company Information",
            "explanation": "No substantial company description is provided, making it hard to verify the employer."
        })
    else:
        positive_signs.append("Company description is provided.")
        
    if not job_data.get('location') or job_data.get('location', '').lower() == 'unknown':
        warning_signs.append({
            "indicator": "Missing Location",
            "explanation": "The job location is unspecified or unknown."
        })
        
    # Rule 5: Suspicious contact requests
    suspicious_contacts = ['telegram', 'whatsapp', 'direct message only']
    found_contacts = [kw for kw in suspicious_contacts if kw in combined_text]
    if found_contacts:
        warning_signs.append({
            "indicator": "Suspicious Contact Method",
            "explanation": f"Requests to communicate via unofficial channels: {', '.join(found_contacts)}."
        })
        
    # Rule 6: Poorly structured job posting
    orig_desc = str(job_data.get('job_description', ''))
    if len(orig_desc.split()) < 20 and len(orig_desc.strip()) > 0:
        warning_signs.append({
            "indicator": "Very Short Description",
            "explanation": "The job description is suspiciously brief."
        })
        
    # Check for excessive capitalization in title
    orig_title = str(job_data.get('job_title', ''))
    if len(orig_title) > 5 and sum(1 for c in orig_title if c.isupper()) / len(orig_title) > 0.5:
        warning_signs.append({
            "indicator": "Excessive Capitalization",
            "explanation": "The job title uses excessive uppercase letters, a common spam technique."
        })

    # Rule 7: Positive Indicators
    if job_data.get('has_company_logo') == 1:
        positive_signs.append("Company logo is present.")
    if job_data.get('has_company_profile') == 1:
        positive_signs.append("Detailed company profile flag is active.")
        
    # --- COMBINING ML AND RULES ---
    # Start with ML probability mapped to a 0-100 scale
    base_score = ml_probability * 100
    
    # Add penalty points for each warning sign (configurable weight)
    penalty_per_warning = 15
    rule_penalty = len(warning_signs) * penalty_per_warning
    
    # Deduct points for positive signs
    bonus_per_positive = 5
    rule_bonus = len(positive_signs) * bonus_per_positive
    
    final_score = base_score + rule_penalty - rule_bonus
    
    # Cap between 0 and 100
    final_score = max(0, min(100, final_score))
    
    # Determine Risk Level
    if final_score < 30:
        risk_level = "Low"
    elif final_score < 70:
        risk_level = "Medium"
    else:
        risk_level = "High"
        
    # Explanation text
    explanation = f"The Machine Learning model returned a base confidence score of {base_score:.1f}/100. "
    explanation += f"Rule-based analysis added {rule_penalty} points for {len(warning_signs)} warning sign(s) "
    explanation += f"and deducted {rule_bonus} points for {len(positive_signs)} positive sign(s), "
    explanation += f"resulting in a final Risk Score of {final_score:.1f}/100."
    
    return {
        "risk_score": round(final_score, 1),
        "risk_level": risk_level,
        "warning_signs": warning_signs,
        "positive_signs": positive_signs,
        "explanation": explanation,
        "ml_probability": ml_probability
    }

if __name__ == "__main__":
    # Test cases
    print("--- Testing Risk Analyzer ---")
    
    # 1. Normal-looking job
    normal_job = {
        "job_title": "Software Engineer",
        "job_description": "We are looking for a skilled software engineer to join our team. You will write clean code.",
        "company_profile": "TechCorp is a leading technology company established in 2010.",
        "location": "San Francisco, CA",
        "has_company_logo": 1
    }
    print("\n1. Normal Job")
    print(analyze_risk(normal_job, 0.05))
    
    # 2. Suspicious-looking job
    suspicious_job = {
        "job_title": "EARN THOUSANDS QUICK",
        "job_description": "Urgent hiring! Send registration fee to start. Easy money working from home.",
        "company_profile": "",
        "location": "Unknown",
        "has_company_logo": 0
    }
    print("\n2. Suspicious Job")
    print(analyze_risk(suspicious_job, 0.85))
    
    # 3. Incomplete job posting
    incomplete_job = {
        "job_title": "Assistant",
        "job_description": "Help around the office.",
        "company_profile": "",
        "location": ""
    }
    print("\n3. Incomplete Job")
    print(analyze_risk(incomplete_job, 0.40))
