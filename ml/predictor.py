import os
import joblib
import traceback


# ============================================================
# JOBSHIELD ML PREDICTOR
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "jobshield_model.pkl"
)


# ============================================================
# OPTIMIZED FAKE DETECTION THRESHOLD
# ============================================================

# Selected by ml/train.py
# based on the highest F1-score.
FAKE_THRESHOLD = 0.70


_model = None


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

def load_model():

    global _model

    if _model is None:

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(
                "JobShield ML model not found.\n"
                "Please run:\n"
                "python ml/train.py"
            )

        print("Loading JobShield ML model...")

        _model = joblib.load(
            MODEL_PATH
        )

        print(
            "JobShield ML model loaded successfully."
        )

    return _model


# ============================================================
# PREDICT JOB
# ============================================================

def predict_job(description):

    if not description:

        raise ValueError(
            "Job description cannot be empty."
        )

    model = load_model()

    # Get probability for both classes
    probabilities = model.predict_proba(
        [description]
    )[0]

    genuine_probability = probabilities[0]
    fake_probability = probabilities[1]

    # Apply optimized threshold
    if fake_probability >= FAKE_THRESHOLD:

        prediction = 1
        result = "Fake / Suspicious"

    else:

        prediction = 0
        result = "Likely Genuine"

    return {
        "prediction": prediction,
        "result": result,
        "genuine_probability": round(
            genuine_probability * 100,
            2
        ),
        "fake_probability": round(
            fake_probability * 100,
            2
        ),
        "threshold": FAKE_THRESHOLD
    }


# ============================================================
# TEST PREDICTION
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 50)
    print("       JOBSHIELD ML PREDICTION TEST")
    print("=" * 50)

    print()

    print(
        f"Fake Detection Threshold: "
        f"{FAKE_THRESHOLD * 100:.0f}%"
    )

    print()

    # ========================================================
    # SCAM / FAKE JOB TEST
    # ========================================================

    test_job = """
    Urgent hiring for work from home data entry jobs.

    No experience required.

    Earn ₹50000 per day.

    Pay ₹3000 registration fee to confirm your position.

    Contact only through WhatsApp.

    Send your bank details and OTP for verification.
    """

    try:

        result = predict_job(
            test_job
        )

        print()

        print("Prediction:")
        print(
            result["result"]
        )

        print()

        print("Genuine Probability:")
        print(
            f'{result["genuine_probability"]}%'
        )

        print()

        print("Fake Probability:")
        print(
            f'{result["fake_probability"]}%'
        )

        print()

        print("Decision Threshold:")
        print(
            f'{result["threshold"] * 100:.0f}%'
        )

        print()

        print("=" * 50)
        print("       PREDICTION TEST COMPLETE")
        print("=" * 50)

    except Exception as e:

        print()

        print("Prediction Error:")
        print(
            repr(e)
        )

        print()

        print("Detailed Error:")

        traceback.print_exc()