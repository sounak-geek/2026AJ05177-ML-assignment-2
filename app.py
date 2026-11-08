import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, matthews_corrcoef,
                             precision_score, recall_score, roc_auc_score)

st.set_page_config(page_title="Handwritten Digits Classifier", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, "model")
TARGET = "target"
LABELS = list(range(10))
CLASS_NAMES = [str(d) for d in LABELS]

MODEL_FILES = {
    "Logistic Regression": "logistic_regression.joblib",
    "Decision Tree": "decision_tree.joblib",
    "KNN": "knn.joblib",
    "Naive Bayes": "naive_bayes.joblib",
    "Support Vector Machine": "support_vector_machine.joblib",
}


@st.cache_resource
def load_model(name):
    return joblib.load(os.path.join(MODEL_DIR, MODEL_FILES[name]))


def compute_metrics(model, X, y):
    pred = model.predict(X)
    return {
        "Accuracy": accuracy_score(y, pred),
        "AUC": roc_auc_score(y, model.predict_proba(X), multi_class="ovr",
                             average="macro", labels=LABELS),
        "Precision": precision_score(y, pred, average="macro", zero_division=0),
        "Recall": recall_score(y, pred, average="macro", zero_division=0),
        "F1": f1_score(y, pred, average="macro", zero_division=0),
        "MCC": matthews_corrcoef(y, pred),
    }, pred


st.title("Handwritten Digits (UCI Optical Recognition) - Classification Models")
st.write(
    "Upload the test CSV (64 pixel columns plus a `target` digit 0-9), pick a model and inspect "
    "its evaluation. Precision, Recall, F1 and AUC are macro-averaged over the 10 classes "
    "(AUC is one-vs-rest)."
)

# (a) dataset upload
uploaded = st.file_uploader("Upload test CSV", type=["csv"])
if uploaded is None:
    st.info("Upload `test_data.csv` from the repository to begin.")
    st.stop()

data = pd.read_csv(uploaded)
if TARGET not in data.columns:
    st.error(f"The CSV must contain a '{TARGET}' column.")
    st.stop()

X = data.drop(columns=TARGET)
y = data[TARGET]

# make sure the columns match what the models were trained on
ref = load_model("Logistic Regression")
expected = list(ref.feature_names_in_)
missing = [c for c in expected if c not in X.columns]
if missing:
    st.error(f"Missing feature columns: {missing}")
    st.stop()
X = X[expected]

st.subheader("Data preview")
st.write(f"{X.shape[0]} rows x {X.shape[1]} features")
st.dataframe(data.head())

# (b) model selection dropdown
choice = st.selectbox("Select a model", list(MODEL_FILES.keys()))
model = load_model(choice)
metrics, pred = compute_metrics(model, X, y)

# (c) evaluation metrics
st.subheader(f"Evaluation metrics - {choice}")
cols = st.columns(len(metrics))
for col, (k, v) in zip(cols, metrics.items()):
    col.metric(k, f"{v:.4f}")

# (d) confusion matrix + classification report
left, right = st.columns(2)
with left:
    st.subheader("Confusion matrix")
    cm = confusion_matrix(y, pred, labels=LABELS)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)
    st.markdown(
        "**How to read:** Rows are the true digits; columns are the model's predictions. "
        "Diagonal counts are correct predictions, while off-diagonal counts are errors. "
        "Darker cells contain more samples."
    )
with right:
    st.subheader("Classification report")
    report = classification_report(y, pred, labels=LABELS, target_names=CLASS_NAMES,
                                   output_dict=True, zero_division=0)
    st.dataframe(pd.DataFrame(report).T.round(4))
    st.markdown(
        "**How to read:** Each digit has its own precision, recall, and F1 score. "
        "Support is the number of true samples for that digit. Macro averages weight "
        "digits equally; weighted averages account for their sample counts."
    )

# comparison of all models on the uploaded test data
st.subheader("All models on the uploaded test data")
rows = []
for name in MODEL_FILES:
    m, _ = compute_metrics(load_model(name), X, y)
    rows.append({"ML Model Name": name, **m})
compare = pd.DataFrame(rows).set_index("ML Model Name").round(4)
st.dataframe(compare.style.format("{:.4f}").highlight_max(axis=0, color="#BDF5EA"))
st.markdown(
    "**How to read:** The highlighted cell marks the highest score in that metric column. "
    "Higher is better for every metric shown."
)
