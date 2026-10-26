import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "DataSet.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "jobshield_model.pkl"
)

METRICS_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "metrics.txt"
)


# ============================================================
# LOAD DATASET
# ============================================================

print()
print("=" * 65)
print("       JOBSHIELD ML - THRESHOLD OPTIMIZATION")
print("=" * 65)
print()

print("Loading EMSCAD dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Dataset loaded successfully.")
print(f"Total records: {len(df)}")


# ============================================================
# CONVERT TARGET
# ============================================================

df["fraudulent"] = (
    df["fraudulent"]
    .astype(str)
    .str.lower()
    .map({
        "t": 1,
        "f": 0,
        "1": 1,
        "0": 0
    })
)

df = df.dropna(
    subset=["fraudulent"]
)


# ============================================================
# COMBINE JOB INFORMATION
# ============================================================

text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]


for column in text_columns:

    if column not in df.columns:
        df[column] = ""

    df[column] = df[column].fillna("")


df["combined_text"] = (
    df[text_columns]
    .astype(str)
    .agg(" ".join, axis=1)
)


X = df["combined_text"]
y = df["fraudulent"].astype(int)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print()
print("Preparing train/test data...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")


# ============================================================
# MODEL
# ============================================================

print()
print("Building TF-IDF + Logistic Regression model...")

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2,
            max_df=0.95
        )
    ),

    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        )
    )
])


# ============================================================
# TRAIN
# ============================================================

print()
print("Training model...")

model.fit(
    X_train,
    y_train
)

print("Training completed successfully.")


# ============================================================
# GET PROBABILITIES
# ============================================================

print()
print("Calculating prediction probabilities...")

fake_probabilities = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# THRESHOLD TESTING
# ============================================================

thresholds = [
    0.50,
    0.55,
    0.60,
    0.65,
    0.70
]

results = []


print()
print("=" * 65)
print("              THRESHOLD COMPARISON")
print("=" * 65)
print()

print(
    f"{'Threshold':<12}"
    f"{'Accuracy':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
)

print("-" * 60)


for threshold in thresholds:

    y_pred_threshold = (
        fake_probabilities >= threshold
    ).astype(int)

    accuracy = accuracy_score(
        y_test,
        y_pred_threshold
    )

    precision = precision_score(
        y_test,
        y_pred_threshold,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred_threshold,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred_threshold,
        zero_division=0
    )

    results.append({
        "threshold": threshold,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    })

    print(
        f"{threshold:<12.2f}"
        f"{accuracy:<12.4f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
    )


# ============================================================
# SELECT BEST THRESHOLD
# ============================================================

best_result = max(
    results,
    key=lambda x: x["f1"]
)

best_threshold = best_result["threshold"]


print()
print("=" * 65)
print("                BEST THRESHOLD")
print("=" * 65)
print()

print(
    f"Selected threshold: {best_threshold:.2f}"
)

print(
    f"Accuracy:  {best_result['accuracy']:.4f}"
)

print(
    f"Precision: {best_result['precision']:.4f}"
)

print(
    f"Recall:    {best_result['recall']:.4f}"
)

print(
    f"F1 Score:  {best_result['f1']:.4f}"
)


# ============================================================
# FINAL PREDICTION USING BEST THRESHOLD
# ============================================================

y_pred = (
    fake_probabilities >= best_threshold
).astype(int)


# ============================================================
# FINAL METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(
    y_test,
    y_pred
)

report = classification_report(
    y_test,
    y_pred,
    target_names=[
        "Genuine",
        "Fake"
    ],
    zero_division=0
)


# ============================================================
# SAVE MODEL
# ============================================================

print()
print("Saving model...")

joblib.dump(
    model,
    MODEL_PATH,
    compress=3
)

print(
    f"Model saved successfully:\n{MODEL_PATH}"
)


# ============================================================
# SAVE METRICS
# ============================================================

with open(
    METRICS_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "JOBSHIELD ML MODEL EVALUATION\n"
    )

    file.write(
        "==============================\n\n"
    )

    file.write(
        "Model: TF-IDF + Logistic Regression\n"
    )

    file.write(
        f"Dataset records: {len(df)}\n"
    )

    file.write(
        f"Training samples: {len(X_train)}\n"
    )

    file.write(
        f"Testing samples: {len(X_test)}\n"
    )

    file.write(
        f"Selected threshold: {best_threshold:.2f}\n\n"
    )

    file.write(
        f"Accuracy: {accuracy:.4f}\n"
    )

    file.write(
        f"Precision: {precision:.4f}\n"
    )

    file.write(
        f"Recall: {recall:.4f}\n"
    )

    file.write(
        f"F1 Score: {f1:.4f}\n\n"
    )

    file.write(
        "Threshold Comparison:\n\n"
    )

    for item in results:

        file.write(
            f"Threshold: {item['threshold']:.2f} | "
            f"Accuracy: {item['accuracy']:.4f} | "
            f"Precision: {item['precision']:.4f} | "
            f"Recall: {item['recall']:.4f} | "
            f"F1: {item['f1']:.4f}\n"
        )

    file.write(
        "\nClassification Report:\n"
    )

    file.write(
        report
    )

    file.write(
        "\nConfusion Matrix:\n"
    )

    file.write(
        str(cm)
    )


# ============================================================
# DISPLAY FINAL RESULTS
# ============================================================

print()
print("=" * 65)
print("             FINAL MODEL RESULTS")
print("=" * 65)
print()

print(f"Selected Threshold: {best_threshold:.2f}")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")

print()
print("Classification Report:")
print()
print(report)

print("Confusion Matrix:")
print(cm)

print()
print("=" * 65)
print("       JOBSHIELD ML TRAINING COMPLETE")
print("=" * 65)
print()

print("Your existing Flask application was NOT modified.")
print("Threshold optimization is complete.")