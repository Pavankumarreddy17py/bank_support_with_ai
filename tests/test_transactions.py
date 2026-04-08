from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_transaction_history(request):
    payload = {"account_id": "acc_001", "start_date": "2023-01-01", "end_date": "2023-02-01"}
    r = client.post('/api/transactions/history', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert 'account_id' in data
    assert isinstance(data.get('transactions'), list)

    transactions_len = len(data.get('transactions', []))
    metrics = {'transactions_len': transactions_len, 'accuracy': 1.0}
    request.config._test_metrics[request.node.nodeid] = metrics
    print('Transactions test metrics:', metrics)
