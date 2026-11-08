# Handwritten Digit Classification - ML Assignment 2

## a. Problem statement

Build and compare five classification models that recognise handwritten digits (0-9) from the pixel intensities of a small scanned image. This is a **multi-class** problem with 10 classes. The models are evaluated with Accuracy, AUC, Precision, Recall, F1 and MCC, and are demonstrated in an interactive Streamlit app deployed on Streamlit Community Cloud.

## b. Dataset description

- **Source:** UCI Machine Learning Repository, *Optical Recognition of Handwritten Digits*. The copy used here is the 1,797-sample subset distributed with scikit-learn (`sklearn.datasets.load_digits`), which corresponds to the UCI test portion of the data.
- **Task:** multi-class classification, target = the digit (0-9).
- **Instances:** 1,797 (about 180 per class). Minimum of 500 is met.
- **Features:** 64 numeric features, one per pixel of an 8x8 image, with integer values from 0 to 16 (minimum of 12 is met). Columns are named `pixel_<row>_<col>`.
- **Missing values:** none.
- **Split:** stratified 70/30 train/test split with `random_state=2026` (1,257 train rows, 540 test rows, 52-55 samples per digit in the test set). The test split is saved as `test_data.csv` (64 features + `target`).
- **Preprocessing:** `StandardScaler` is part of the Logistic Regression, KNN and SVM pipelines, so each saved `.joblib` file is self-contained. The SVM is wrapped in `CalibratedClassifierCV` so it can output class probabilities for AUC.
- **Multi-class metrics:** Precision, Recall, F1 and AUC are **macro-averaged** over the 10 classes (AUC is one-vs-rest). Accuracy and MCC are the standard multi-class versions.

## c. GitHub repository link & Streamlit App link

* **GitHub Repository:** [https://github.com/sounak-geek/2026AJ05177-ML-assignment-2](https://github.com/sounak-geek/2026AJ05177-ML-assignment-2)
* **Live Streamlit App:** [https://2026aj05177-ml-assignment-2.streamlit.app/](https://2026aj05177-ml-assignment-2.streamlit.app/)

Repository structure:

```
ml-assignment-2/
|-- app.py
|-- theme.py
|-- train_models.py
|-- .streamlit/
|   |-- config.toml
|-- requirements.txt
|-- README.md
|-- test_data.csv
|-- model/
    |-- logistic_regression.joblib
    |-- decision_tree.joblib
    |-- knn.joblib
    |-- naive_bayes.joblib
    |-- support_vector_machine.joblib
    |-- metrics_summary.csv
```

## d. Models used

All five models were trained on the same training split and evaluated on the same test split (540 rows).

| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.9704 | 0.9986 | 0.9705 | 0.9704 | 0.9704 | 0.9671 |
| Decision Tree | 0.8685 | 0.9257 | 0.8698 | 0.8685 | 0.8683 | 0.8541 |
| KNN | 0.9778 | 0.9948 | 0.9783 | 0.9774 | 0.9776 | 0.9754 |
| Naive Bayes | 0.8111 | 0.9742 | 0.8484 | 0.8095 | 0.8142 | 0.7945 |
| Support Vector Machine | 0.9833 | 0.9946 | 0.9840 | 0.9833 | 0.9834 | 0.9815 |

Hyperparameters: Logistic Regression (`max_iter=2000`), Decision Tree (`max_depth=10`), KNN (`k=5`), Gaussian Naive Bayes (defaults), SVM (RBF kernel, defaults, probability-calibrated with 5-fold `CalibratedClassifierCV`).

### Observations on model performance

| ML Model Name | Observation about model performance |
|---|---|
| Logistic Regression | Very strong: accuracy 0.9704 (16 errors out of 540) and the highest AUC (0.9986). Pixel intensities of different digits are largely separable by a linear boundary once standardised. Its weakest class is digit 9 (recall 0.926). |
| Decision Tree | Accuracy 0.8685 (71 errors) and the lowest AUC (0.9257). Single pixels are weak individual features for images, so a depth-10 tree needs many axis-aligned splits and ends up fitting noisy pixel patterns. Digit 8 is its weakest class (recall 0.808). |
| KNN | Accuracy 0.9778 (12 errors), close to the best. Handwritten digits form tight clusters in pixel space, so nearest neighbours work well; it depends on scaling, which the pipeline provides. Digit 8 is the weakest class (recall 0.904), occasionally mistaken for 1. |
| Naive Bayes | Weakest model: accuracy 0.8111 (102 errors) and MCC 0.7945. Neighbouring pixels are strongly correlated, which breaks the independence assumption. Digit 8 is badly affected (recall 0.519, 19 of the 8s predicted as 1). Its AUC (0.9742) is still high, so the probability ranking is reasonable even though the predicted labels are often wrong. |
| Support Vector Machine | Best on accuracy (0.9833), F1 (0.9834) and MCC (0.9815) with only 9 errors out of 540. The RBF kernel captures the non-linear structure in the pixel space. Its AUC (0.9946) is marginally below Logistic Regression and KNN, which is a side effect of the probability calibration step. |
| Overall, Winner for your dataset? | **Support Vector Machine** (accuracy 0.9833, MCC 0.9815), followed by KNN and Logistic Regression. The top three are within 7 test errors of each other, so the ranking is based on a single split. The Decision Tree and Naive Bayes are clearly behind. |

## Streamlit app

`app.py` provides:

1. CSV upload for test data (must contain all 64 pixel features and the `target` column).
2. Model selection dropdown for the five classifiers.
3. Display of Accuracy, AUC, Precision, Recall, F1 and MCC (macro-averaged for the multi-class case).
4. A 10x10 confusion matrix and a per-class classification report.
5. A comparison table of all five models on the uploaded data (best value per metric highlighted).
6. A custom blue / peacock / teal / cyan / green look and feel (`theme.py` and `.streamlit/config.toml`).

Saved models are loaded from `model/`; nothing is retrained on the uploaded data.

### Run locally

```
pip install -r requirements.txt
python train_models.py     # optional: regenerates model/ and test_data.csv
streamlit run app.py
```

### Deploy on Streamlit Community Cloud

1. Go to https://streamlit.io/cloud and sign in with GitHub.
2. Click "New app", select this repository, branch `main`, main file `app.py`.
3. Click Deploy.
