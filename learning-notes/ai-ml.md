# AI / ML Learning Notes

> Personal notes as I work through Project 03 (Sentiment API).

---

## The Two Phases (Critical Mental Model)

```
TRAINING PHASE (Notebook)          SERVING PHASE (FastAPI)
──────────────────────────         ──────────────────────────
Load data                          Load saved model (once)
Clean / preprocess                 Receive request
Train model                        Run model.predict()
Evaluate (accuracy, F1)            Return result as JSON
Save model → .joblib               
```

Never mix these. Training is slow and done offline. Serving is fast and done per-request.

---

## scikit-learn Pipeline
The `Pipeline` object chains steps together. This is important because the same
preprocessing (e.g. TF-IDF) must be applied during both training AND prediction.

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression()),
])

model.fit(X_train, y_train)
model.predict(["some new text"])  # TF-IDF is applied automatically
```

---

## Saving and Loading Models

```python
import joblib

# Save
joblib.dump(model, 'model/sentiment_model.joblib')

# Load
model = joblib.load('model/sentiment_model.joblib')
```

---

## Key Metrics

| Metric | What it means |
|--------|--------------|
| Accuracy | % of correct predictions |
| Precision | Of predicted positives, how many were right |
| Recall | Of actual positives, how many did we catch |
| F1 Score | Harmonic mean of Precision + Recall |

For imbalanced data (more negatives than positives), F1 is more useful than Accuracy.

---

## Resources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Jupyter Notebook Docs](https://jupyter.org/documentation)
