"""Small reproducible binary-classification example using synthetic data."""

import pandas as pd
import sklearn
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

SEED = 42

X, y = make_classification(
    n_samples=200,
    n_features=4,
    n_informative=3,
    n_redundant=0,
    n_classes=2,
    class_sep=1.0,
    random_state=SEED,
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=SEED, stratify=y
)
model = LogisticRegression(random_state=SEED, max_iter=500)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

summary = pd.DataFrame(
    {
        "split": ["train", "test"],
        "rows": [len(y_train), len(y_test)],
        "positive_labels": [int(y_train.sum()), int(y_test.sum())],
    }
)
print(f"seed={SEED}")
print(f"pandas={pd.__version__} scikit-learn={sklearn.__version__}")
print(summary.to_string(index=False))
print(f"test_accuracy={accuracy_score(y_test, predictions):.3f}")
print("confusion_matrix=[[TN, FP], [FN, TP]]")
print(confusion_matrix(y_test, predictions).tolist())
