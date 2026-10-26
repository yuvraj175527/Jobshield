import os
import sys


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# IMPORT JOBSHIELD MODULES
# ============================================================

from utils.risk_analyzer import analyze_job
from ml.predictor import predict_job


# ============================================================
# JOBSHIELD HYBRID ANALYZER
# ============================================================

def analyze_job_hybrid(
    company_name="",
    job_title="",
    recruiter_name="",
    job_url="",
    salary="",
    description=""
):

    # ========================================================
    # RULE-BASED ANALYSIS
    # ========================================================

    rule_result = analyze_job(
        company_name=company_name,
        job_title=job_title,
        recruiter_name=recruiter_name,
        job_url=job_url,
        salary=salary,
        description=description
    )

    # ========================================================
    # MACHINE LEARNING ANALYSIS
    # ========================================================

    ml_result = predict_job(
        description
    )

    # ========================================================
    # EXTRACT RULE RESULTS
    # ========================================================

    rule_score = int(
        rule_result.get(
            "risk_score",
            0
        )
    )

    rule_level = rule_result.get(
        "risk_level",
        "Unknown"
    )

    rule_status = rule_result.get(
        "status",
        "Unknown"
    )

    rule_reasons = rule_result.get(
        "reasons",
        []
    )

    # ========================================================
    # EXTRACT ML RESULTS
    # ========================================================

    ml_fake_probability = float(
        ml_result.get(
            "fake_probability",
            0
        )
    )

    ml_genuine_probability = float(
        ml_result.get(
            "genuine_probability",
            0
        )
    )

    ml_result_text = ml_result.get(
        "result",
        "Unknown"
    )

    ml_threshold = float(
        ml_result.get(
            "threshold",
            0.70
        )
    )

    # ========================================================
    # ML RISK SCORE
    # ========================================================

    ml_risk_score = round(
        ml_fake_probability
    )

    # ========================================================
    # HYBRID SCORE
    # ========================================================

    hybrid_score = round(
        (rule_score * 0.60)
        +
        (ml_risk_score * 0.40)
    )

    # Keep score between 0 and 100
    hybrid_score = max(
        0,
        min(
            100,
            hybrid_score
        )
    )

    # ========================================================
    # FINAL RISK LEVEL
    # ========================================================

    if hybrid_score >= 60:

        hybrid_level = "High Risk"
        hybrid_status = "Fake / Suspicious"

    elif hybrid_score >= 30:

        hybrid_level = "Suspicious"
        hybrid_status = "Needs Verification"

    else:

        hybrid_level = "Low Risk"
        hybrid_status = "Likely Genuine"

    # ========================================================
    # COMBINE DETECTION REASONS
    # ========================================================

    combined_reasons = []

    if isinstance(
        rule_reasons,
        list
    ):

        combined_reasons.extend(
            rule_reasons
        )

    elif rule_reasons:

        combined_reasons.append(
            str(rule_reasons)
        )

    # Add ML explanation
    if ml_fake_probability >= 70:

        combined_reasons.append(
            "Machine learning model detected a strong "
            "similarity to fraudulent job patterns."
        )

    elif ml_fake_probability >= 50:

        combined_reasons.append(
            "Machine learning model detected some "
            "patterns associated with fraudulent jobs."
        )

    else:

        combined_reasons.append(
            "Machine learning model found a lower "
            "probability of fraudulent job patterns."
        )

    # Remove duplicate reasons
    combined_reasons = list(
        dict.fromkeys(
            combined_reasons
        )
    )

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "risk_score": hybrid_score,

        "risk_level": hybrid_level,

        "status": hybrid_status,

        "reasons": combined_reasons,

        # Rule-based results
        "rule_score": rule_score,

        "rule_level": rule_level,

        "rule_status": rule_status,

        # ML results
        "ml_prediction": ml_result_text,

        "ml_fake_probability": round(
            ml_fake_probability,
            2
        ),

        "ml_genuine_probability": round(
            ml_genuine_probability,
            2
        ),

        "ml_threshold": round(
            ml_threshold * 100,
            2
        )
    }


# ============================================================
# TEST HYBRID SYSTEM
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       JOBSHIELD HYBRID ANALYZER TEST")
    print("=" * 60)
    print()

    # ========================================================
    # SCAM JOB TEST
    # ========================================================

    result = analyze_job_hybrid(

        company_name="ABC Online Services",

        job_title="Work From Home Data Entry",

        recruiter_name="HR Manager",

        job_url="",

        salary="₹50,000 per day",

        description="""
        Urgent hiring for work from home data entry jobs.

        No experience required.

        Earn ₹50000 per day.

        Pay ₹3000 registration fee to confirm your position.

        Contact only through WhatsApp.

        Send your bank details and OTP for verification.
        """
    )

    print("RULE-BASED SCORE:")
    print(
        f'{result["rule_score"]}/100'
    )

    print()

    print("ML FAKE PROBABILITY:")
    print(
        f'{result["ml_fake_probability"]}%'
    )

    print()

    print("ML GENUINE PROBABILITY:")
    print(
        f'{result["ml_genuine_probability"]}%'
    )

    print()

    print("ML THRESHOLD:")
    print(
        f'{result["ml_threshold"]}%'
    )

    print()

    print("HYBRID SCORE:")
    print(
        f'{result["risk_score"]}/100'
    )

    print()

    print("FINAL RISK LEVEL:")
    print(
        result["risk_level"]
    )

    print()

    print("FINAL STATUS:")
    print(
        result["status"]
    )

    print()

    print("DETECTED REASONS:")

    for reason in result["reasons"]:

        print(
            f"- {reason}"
        )

    print()

    print("=" * 60)
    print("       HYBRID TEST COMPLETE")
    print("=" * 60)