import os

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Handwritten Digits Classifier", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, "model")
TARGET = "target"

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
st.caption(f"Selected model: {choice}")
