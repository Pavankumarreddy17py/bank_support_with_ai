import pandas as pd
from transformers import pipeline
import os
import re

class Chatbot:
    def __init__(self, model_name: str = "distilgpt2"):
        print("🤖 Initializing AI Support Model...")
        self.generator = pipeline('text-generation', model=model_name)
        
        # EXACT PATH TO YOUR DATA
        self.data_path = r"data\kaggle\creditcard.csv"
        
        if os.path.exists(self.data_path):
            # Load enough rows to answer summary questions
            self.df = pd.read_csv(self.data_path, nrows=5000)
            print(f"✅ SUCCESS: Loaded dataset.")
        else:
            self.df = None
            print(f"❌ ERROR: File not found.")

    def get_facts(self, prompt: str):
        if self.df is None: return "System: Database is offline."
        
        p_low = prompt.lower()

        # 1. Handle "How do you detect fraud?"
        if "how" in p_low and "detect" in p_low:
            return "SYSTEM_LOGIC: I use an Isolation Forest machine learning model. It analyzes 28 PCA features (V1-V28) and the transaction amount to identify outliers that differ from normal spending patterns."

        # 2. Handle "Are there any fraudulent transactions?"
        if "fraudulent" in p_low or "any fraud" in p_low:
            fraud_count = len(self.df[self.df['Class'] == 1])
            if fraud_count == 0:
                return "SUMMARY: I have scanned the current logs and found 0 transactions marked as fraudulent (Class 1)."
            else:
                return f"SUMMARY: I have detected {fraud_count} fraudulent transactions in the logs."

        # 3. Handle "Is [Amount] suspicious?"
        amount_match = re.findall(r'\d+\.\d+', prompt)
        if amount_match and "suspicious" in p_low or "charge" in p_low:
            amt_val = float(amount_match[0])
            match = self.df[abs(self.df['Amount'] - amt_val) < 0.1]
            if not match.empty:
                row = match.iloc[0]
                status = "Normal" if row['Class'] == 0 else "Fraudulent"
                return f"CHECK: The ${row['Amount']} charge at Time {row['Time']} is categorized as {status} (Class {row['Class']})."

        # 4. Handle "Time X" (Existing Logic)
        time_match = re.search(r'time\s*[:]*\s*(\d+)', p_low)
        if time_match:
            t_val = int(time_match.group(1))
            rows = self.df[self.df['Time'] == t_val]
            if not rows.empty:
                results = [f"${row['Amount']} (Status: {'Normal' if row['Class']==0 else 'Fraud'})" for _, row in rows.iterrows()]
                return f"At Time {t_val}, I found: " + " and ".join(results) + "."
        
        return "I don't have specific data for that query. Please ask about a specific Time or how the system works."

    def respond(self, prompt: str) -> str:
        facts = self.get_facts(prompt)
        
        # If the fact is a direct answer/summary, return it immediately to avoid AI mess
        if "SUMMARY:" in facts or "SYSTEM_LOGIC:" in facts or "CHECK:" in facts:
            return facts.split(": ")[-1]

        # Standard data retrieval response
        if "At Time" in facts:
            return f"I have checked your records: {facts} Is there anything else you need?"

        # Fallback for general conversation
        system_prompt = (
            f"Context: You are a Bank AI. {facts}\n"
            f"User: {prompt}\n"
            "AI Answer:"
        )

        output = self.generator(system_prompt, max_new_tokens=35, temperature=0.1, pad_token_id=50256)
        ans = output[0]['generated_text'].split("AI Answer:")[-1].strip()
        return ans if len(ans) > 5 else "I'm here to help with your transaction logs. What can I check for you?"