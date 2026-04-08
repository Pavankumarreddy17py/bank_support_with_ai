const API_BASE_URL = 'http://localhost:8000/api';

export const chatbotService = {
  async sendMessage(customerId, message) {
    const response = await fetch(`${API_BASE_URL}/customer/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_id: customerId, message: message }),
    });
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  }
};

export const transactionService = {
  async getHistory(accountId, startDate, endDate) {
    const response = await fetch(`${API_BASE_URL}/transactions/history`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ account_id: accountId, start_date: startDate, end_date: endDate }),
    });
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  }
};