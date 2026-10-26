import re


def analyze_job(
    company_name,
    job_title,
    recruiter_name="",
    job_url="",
    salary="",
    description=""
):

    score = 0
    reasons = []

    # Combine all information
    text = " ".join([
        company_name,
        job_title,
        recruiter_name,
        job_url,
        salary,
        description
    ]).lower()


    # ==========================================
    # 1. PAYMENT / FEE DETECTION
    # ==========================================

    payment_keywords = [
        "registration fee",
        "registration fees",
        "application fee",
        "application fees",
        "processing fee",
        "processing fees",
        "security deposit",
        "security fee",
        "joining fee",
        "joining fees",
        "training fee",
        "training fees",
        "pay to apply",
        "pay for job",
        "pay money",
        "payment required",
        "deposit money",
        "pay rs",
        "pay ₹"
    ]

    payment_found = []

    for keyword in payment_keywords:
        if keyword in text:
            payment_found.append(keyword)

    if payment_found:
        score += min(len(payment_found) * 25, 40)

        reasons.append(
            "A possible registration, application, training or "
            "security fee was detected."
        )


    # ==========================================
    # 2. SENSITIVE INFORMATION
    # ==========================================

    sensitive_keywords = [
        "bank account",
        "bank details",
        "credit card",
        "debit card",
        "cvv",
        "otp",
        "one time password",
        "atm pin",
        "upi pin",
        "password",
        "send otp",
        "share otp",
        "aadhaar number",
        "pan card"
    ]

    sensitive_found = []

    for keyword in sensitive_keywords:
        if keyword in text:
            sensitive_found.append(keyword)

    if sensitive_found:
        score += min(len(sensitive_found) * 20, 35)

        reasons.append(
            "The job information appears to request sensitive "
            "personal or financial information."
        )


    # ==========================================
    # 3. UNREALISTIC SALARY
    # ==========================================

    salary_patterns = [
        r"earn\s+₹?\s*\d+\s*(?:lakh|lakhs|crore|crores)?\s*(?:per day|daily)",
        r"₹\s*\d+\s*(?:lakh|lakhs)\s*per month",
        r"\d+\s*(?:lakh|lakhs)\s*per month",
        r"no experience.*high salary",
        r"earn money fast",
        r"make money fast",
        r"guaranteed income",
        r"guaranteed salary",
        r"guaranteed earnings",
        r"easy money"
    ]

    salary_risk = False

    for pattern in salary_patterns:

        if re.search(pattern, text):
            salary_risk = True
            break

    if salary_risk:

        score += 20

        reasons.append(
            "The advertised salary or income appears unusually "
            "high or unrealistic."
        )


    # ==========================================
    # 4. URGENCY
    # ==========================================

    urgency_keywords = [
        "urgent hiring",
        "urgent requirement",
        "limited seats",
        "limited vacancies",
        "act now",
        "apply immediately",
        "apply today",
        "last chance",
        "immediate joining",
        "join immediately",
        "hurry"
    ]

    urgency_found = []

    for keyword in urgency_keywords:

        if keyword in text:
            urgency_found.append(keyword)

    if urgency_found:

        score += min(len(urgency_found) * 5, 10)

        reasons.append(
            "Urgency or pressure-based language was detected."
        )


    # ==========================================
    # 5. WHATSAPP / TELEGRAM
    # ==========================================

    communication_keywords = [
        "contact only on whatsapp",
        "contact us on whatsapp",
        "whatsapp only",
        "message on whatsapp",
        "telegram only",
        "contact only on telegram",
        "dm on instagram",
        "contact through telegram"
    ]

    communication_found = []

    for keyword in communication_keywords:

        if keyword in text:
            communication_found.append(keyword)

    if communication_found:

        score += 15

        reasons.append(
            "The recruiter appears to rely on informal communication "
            "channels such as WhatsApp or Telegram."
        )


    # ==========================================
    # 6. PERSONAL EMAIL
    # ==========================================

    personal_email_domains = [
        "@gmail.com",
        "@yahoo.com",
        "@outlook.com",
        "@hotmail.com",
        "@protonmail.com"
    ]

    personal_email_found = False

    for domain in personal_email_domains:

        if domain in text:
            personal_email_found = True
            break

    if personal_email_found:

        score += 10

        reasons.append(
            "A personal email service appears to be used instead "
            "of an official company email."
        )


    # ==========================================
    # 7. SUSPICIOUS JOB LANGUAGE
    # ==========================================

    suspicious_keywords = [
        "work from home earn",
        "part time income",
        "earn daily",
        "earn per day",
        "no interview",
        "no interview required",
        "guaranteed job",
        "guaranteed placement",
        "100% placement",
        "investment required",
        "franchise opportunity"
    ]

    suspicious_found = []

    for keyword in suspicious_keywords:

        if keyword in text:
            suspicious_found.append(keyword)

    if suspicious_found:

        score += min(len(suspicious_found) * 10, 20)

        reasons.append(
            "Suspicious or commonly abused job-offer language "
            "was detected."
        )


    # ==========================================
    # 8. LIMITED INFORMATION
    # ==========================================

    if len(company_name.strip()) < 3:

        score += 10

        reasons.append(
            "Insufficient company information was provided."
        )


    if len(description.strip()) < 50:

        score += 10

        reasons.append(
            "The job description contains very limited information."
        )


    # ==========================================
    # LIMIT SCORE TO 100
    # ==========================================

    score = min(score, 100)


    # ==========================================
    # CLASSIFICATION
    # ==========================================

    if score >= 60:

        risk_level = "High Risk"
        status = "High Risk"

    elif score >= 30:

        risk_level = "Medium Risk"
        status = "Suspicious"

    else:

        risk_level = "Low Risk"
        status = "Likely Genuine"


    # ==========================================
    # NO WARNING
    # ==========================================

    if not reasons:

        reasons.append(
            "No major suspicious indicators were detected "
            "in the submitted job information."
        )


    return {
        "risk_score": score,
        "risk_level": risk_level,
        "status": status,
        "reasons": reasons
    }