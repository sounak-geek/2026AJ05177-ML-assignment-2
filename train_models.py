"""Train five classifiers on the UCI Optical Recognition of Handwritten Digits
dataset, save them to model/, export a held-out test_data.csv and a metrics table.

Multiclass (10 digits), so Precision / Recall / F1 / AUC are macro-averaged
(AUC is one-vs-rest)."""
import os

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, matthews_corrcoef,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

SEED = 2026
BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

data = load_digits(as_frame=True)
df = data.frame  # 64 pixel features + 'target' (digit 0-9)

X = df.drop(columns="target")
y = df["target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=SEED
)

# Scaler lives inside the pipeline so each saved artifact is self-contained.
# SVC is wrapped in a calibrator so it exposes predict_proba (needed for AUC).
models = {
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=SEED)),
    "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=SEED),
    "KNN": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    "Naive Bayes": GaussianNB(),
    "Support Vector Machine": make_pipeline(
        StandardScaler(),
        CalibratedClassifierCV(SVC(kernel="rbf", random_state=SEED), cv=5, ensemble=False),
    ),
}

rows = []
for name, model in models.items():
    model.fit(X_train, y_train)
    fname = name.lower().replace(" ", "_") + ".joblib"
    joblib.dump(model, os.path.join(MODEL_DIR, fname))

    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)
    rows.append({
        "ML Model Name": name,
        "Accuracy": accuracy_score(y_test, pred),
        "AUC": roc_auc_score(y_test, proba, multi_class="ovr", average="macro", labels=sorted(y.unique())),
        "Precision": precision_score(y_test, pred, average="macro", zero_division=0),
        "Recall": recall_score(y_test, pred, average="macro", zero_division=0),
        "F1": f1_score(y_test, pred, average="macro", zero_division=0),
        "MCC": matthews_corrcoef(y_test, pred),
    })

results = pd.DataFrame(rows).round(4)
results.to_csv(os.path.join(MODEL_DIR, "metrics_summary.csv"), index=False)

test_df = X_test.copy()
test_df["target"] = y_test
test_df.to_csv(os.path.join(BASE, "test_data.csv"), index=False)

print(results.to_string(index=False))
print(f"\nTrain rows: {len(X_train)}  Test rows: {len(X_test)}  Features: {X.shape[1]}")
