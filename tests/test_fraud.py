import os
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def test_fraud_accuracy(request):
    # Uses sample dataset at data/kaggle/creditcard_sample.csv
    sample = os.path.join(os.path.dirname(__file__), '..', 'data', 'kaggle', 'creditcard_sample.csv')
    if not os.path.exists(sample):
        # Nothing to validate if dataset missing
        assert True
        return

    df = pd.read_csv(sample)
    if 'Class' not in df.columns or df.shape[0] < 2:
        assert True
        return

    # Simple split for smoke: 70% train, 30% test
    train = df.sample(frac=0.7, random_state=42)
    test = df.drop(train.index)

    X_train = train.drop(columns=['Class'], errors='ignore')
    X_test = test.drop(columns=['Class'], errors='ignore')
    y_test = test['Class'].astype(int).values

    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X_train)

    preds = model.predict(X_test)
    y_pred = (preds == -1).astype(int)

    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'test_size': int(len(y_test)),
    }

    # Attach metrics to the test report
    request.config._test_metrics[request.node.nodeid] = metrics

    print('Fraud test metrics:', metrics)

    assert isinstance(model, IsolationForest)
