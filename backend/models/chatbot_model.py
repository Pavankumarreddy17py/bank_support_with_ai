import pandas as pd
from transformers import pipeline
import os
import re

class Chatbot:
    def __init__(self, model_name: str = "distilgpt2"):
        print("🤖 Booting Bank Support AI...")
        self.generator = pipeline('text-generation', model=model_name)
        
        # --- THE ULTIMATE PATH FIX ---
        # This looks for the file starting from your Desktop folder
        self.df = None
        possible_paths = [
            r"C:\Users\vadde\Desktop\bank\bank_support_ai11\data\kaggle\creditcard.csv",
            r"C:\Users\vadde\Desktop\bank\bank_support_ai11\creditcard.csv",
            os.path.join(os.getcwd(), "data", "kaggle", "creditcard.csv"),
            "creditcard.csv"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                try:
                    self.df = pd.read_csv(path, nrows=5000)
                    self.data_path = path
                    print(f"✅ SUCCESS: Dataset found at {path}")
                    break
                except Exception as e:
                    print(f"⚠️ Found file at {path} but could not read it: {e}")

        if self.df is None:
            print("❌ FATAL ERROR: Database file not found in any location!")

    def get_facts(self, prompt: str):
        if self.df is None: return "DB_OFFLINE"
        
        p_low = prompt.lower()

        # --- 1. PRIORITY: LISTING FRAUD (Moved to top) ---
        if ("what" in p_low or "list" in p_low or "show" in p_low) and ("fraud" in p_low):
            if 'Class' in self.df.columns:
                fraudulent_rows = self.df[self.df['Class'] == 1]
                if fraudulent_rows.empty:
                    return "FACTS: I have scanned the logs and found 0 fraudulent transactions. All current records appear normal."
                
                fraud_list = []
                for _, row in fraudulent_rows.head(5).iterrows():
                    fraud_list.append(f"Time {row['Time']}: ${row['Amount']}")
                
                response = "FACTS: The detected fraudulent transactions are: " + " | ".join(fraud_list)
                if len(fraudulent_rows) > 5:
                    response += f" (plus {len(fraudulent_rows) - 5} more)."
                return response
            else:
                return "FACTS: I cannot list fraudulent transactions because the 'Class' label is missing."

        # --- 2. COUNTING FRAUD ---
        if "how many" in p_low and "fraud" in p_low:
            if 'Class' in self.df.columns:
                fraud_count = (self.df['Class'] == 1).sum()
                return f"FACTS: I have detected {fraud_count} fraudulent transactions in the current logs."
            return "FACTS: Fraud count is unavailable without 'Class' labels."

        # --- 3. GENERAL FRAUD CHECK (Fallback for just the word "fraud") ---
        if "fraud" in p_low or "suspicious" in p_low:
            if 'Class' in self.df.columns:
                fraud_count = (self.df['Class'] == 1).sum()
                return f"FACTS: My scan shows {fraud_count} suspicious cases. Ask 'What are the fraudulent transactions' to see details."

        # --- 4. DATA LOOKUPS (Time, Amount, Last) ---
        if "last" in p_low or "latest" in p_low:
            last_row = self.df.iloc[-1]
            return f"FACTS: The most recent transaction was ${last_row.get('Amount')} at Time {last_row.get('Time')}."

        time_match = re.search(r'time\s*(\d+)', p_low)
        if time_match:
            t_val = int(time_match.group(1))
            rows = self.df[self.df['Time'] == t_val]
            if not rows.empty:
                results = [f"${row['Amount']} ({'Normal' if row.get('Class',0)==0 else 'Fraud'})" for _, row in rows.iterrows()]
                return "FACTS: At Time " + str(t_val) + ", I found: " + " and ".join(results)

        amt_match = re.findall(r'[\d,]+\.\d+', prompt)
        if amt_match:
            val = float(amt_match[0].replace(',', ''))
            match = self.df[abs(self.df['Amount'] - val) < 0.1]
            if not match.empty:
                status = "Normal" if match.iloc[0].get('Class', 0) == 0 else "Fraudulent"
                return f"FACTS: The ${val} charge is {status}."

        return "NO_SPECIFIC_DATA"

    def respond(self, prompt: str) -> str:
        facts = self.get_facts(prompt)
        
        # 1. If we found a direct fact, RETURN IT IMMEDIATELY.
        # This prevents the AI from even touching the data.
        if any(k in facts for k in ["LOGIC:", "SUMMARY:", "FACTS:", "CHECK:"]):
            return facts.split(": ", 1)[-1]

        # 2. If no facts were found, give a clean human-readable error 
        # instead of sending it to the "No. No. No." AI.
        if facts == "NO_SPECIFIC_DATA":
            if "last" in prompt.lower():
                return "I can only search by Time (0-5000) or specific dollar amounts right now. Please try 'What happened at Time 1?'"
            if "isolation forest" in prompt.lower():
                return "An Isolation Forest is a machine learning algorithm that identifies anomalies by isolating outliers in the data features (V1-V28)."
            return "I couldn't find specific records for that. Please provide a transaction Time or a dollar amount to check."

        # 3. Simple Fallback (only for very basic greeting)
        return "I am your Bank Support AI. I can check transaction logs and identify fraud. How can I help?"