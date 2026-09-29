# Insurance Fraud Detection — Complete ML Project

## Contents
- `insurance_fraud_data.csv` — raw dataset (12,002 claims)
- `cleaned_data.csv` — cleaned dataset after preprocessing (9,530 claims)
- `Insurance_Fraud_Complete_Project.ipynb` — full notebook covering Task 1–6:
  - Task 1: EDA
  - Task 2: Data Cleaning & Preprocessing
  - Task 3: Logistic Regression (sklearn) + Logistic Regression from scratch (NumPy, no library — SOP mandatory constraint)
  - Task 4: Model Evaluation (accuracy, precision, recall, F1, overfitting check)
  - Task 5: 5-fold Cross-Validation, comparison vs Random Forest / AdaBoost / Gradient Boosting, GridSearchCV tuning
  - Task 6: Final model saved for deployment
- `fraud_logistic_regression.pkl` — final trained pipeline (tuned Logistic Regression, class-balanced)
- `app.py` — Streamlit web app for live predictions
- `requirements.txt` — dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click "New app" → select the repo, branch `main`, and `app.py`.
4. Click "Deploy". You'll get a public `*.streamlit.app` link.
5. Any future `git push` auto-redeploys.

## Model Notes
- Final model: Logistic Regression, `class_weight='balanced'`, tuned via GridSearchCV (best C and solver).
- Uses 10 categorical + 15 numeric claim features (vs. the original 10-categorical-only version).
- Chosen over accuracy-only metrics because the dataset is imbalanced (~74% genuine, ~26% fraud) —
  Recall/F1 on the fraud class is the metric that matters for this problem.
