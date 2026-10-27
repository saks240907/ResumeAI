from pathlib import Path
import re
import html

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay
)


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "Resume.csv"
MODEL_DIR = PROJECT_DIR / "models"
MODEL_PATH = MODEL_DIR / "resume_classifier.joblib"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    """Remove HTML tags and normalize whitespace."""
    text = html.unescape(str(text))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main():
    # 1. Load the dataset
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Make sure Resume.csv is inside the data folder."
        )

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    required_columns = {"Resume_str", "Category"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Required columns: {required_columns}\n"
            f"Found columns: {list(df.columns)}"
        )

    # 2. Clean the data
    df = df.dropna(subset=["Resume_str", "Category"]).copy()

    df["Resume_str"] = df["Resume_str"].map(clean_text)
    df["Category"] = df["Category"].astype(str).str.strip()

    df = df[
        (df["Resume_str"].str.len() > 0)
        & (df["Category"].str.len() > 0)
    ].copy()

    # Remove duplicate resume text
    df = df.drop_duplicates(subset=["Resume_str"])

    # Keep categories with enough samples for a reliable split
    category_counts = df["Category"].value_counts()
    valid_categories = category_counts[category_counts >= 5].index
    df = df[df["Category"].isin(valid_categories)].copy()

    if df.empty or df["Category"].nunique() < 2:
        raise ValueError(
            "Not enough usable data. At least two categories, "
            "with five resumes per category, are required."
        )

    X = df["Resume_str"]
    y = df["Category"]

    print(f"\nUsable resumes: {len(df)}")
    print(f"Professional categories: {y.nunique()}")
    print("\nCategory counts:")
    print(y.value_counts().to_string())

    # 3. Split into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(f"\nTraining resumes: {len(X_train)}")
    print(f"Testing resumes: {len(X_test)}")

    # 4. Build the machine-learning pipeline
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                strip_accents="unicode",
                ngram_range=(1, 2),
                max_features=50000,
                sublinear_tf=True
            )
        ),
        (
            "svm",
            LinearSVC(class_weight="balanced")
        )
    ])

    # 5. Train the model
    print("\nTraining TF-IDF + Linear SVM...")
    model.fit(X_train, y_train)

    # 6. Evaluate the model on unseen test data
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"\nTest accuracy: {accuracy:.2%}")
    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # 7. Save the confusion matrix
    display = ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        xticks_rotation="vertical",
        cmap="Blues",
        colorbar=False
    )

    display.figure_.set_size_inches(16, 14)
    display.figure_.tight_layout()

    confusion_path = MODEL_DIR / "confusion_matrix.png"
    display.figure_.savefig(confusion_path, dpi=150)
    plt.close(display.figure_)

    # 8. Save the trained model
    joblib.dump(
        {
            "model": model,
            "categories": sorted(y.unique().tolist()),
            "test_accuracy": accuracy,
            "training_samples": len(X_train),
            "testing_samples": len(X_test)
        },
        MODEL_PATH
    )

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Confusion matrix saved to: {confusion_path}")
    print("\nTraining completed successfully!")


if __name__ == "__main__":
    main()