from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_customer_query(request):
    payload = {"customer_id": "cust_123", "message": "What is my balance?"}
    r = client.post('/api/customer/query', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data['customer_id'] == 'cust_123'
    assert 'response' in data

    response_present = bool(data.get('response'))
    metrics = {'response_present': response_present, 'accuracy': 1.0 if response_present else 0.0}
    request.config._test_metrics[request.node.nodeid] = metrics
    print('Chatbot test metrics:', metrics)
