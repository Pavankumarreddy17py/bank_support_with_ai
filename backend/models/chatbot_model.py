from transformers import pipeline

class Chatbot:
    def __init__(self, model_name: str = "distilgpt2"):
        # This downloads a lightweight AI model the first time you run it
        self.generator = pipeline('text-generation', model=model_name)

    def respond(self, prompt: str) -> str:
        # 1. Define a System Context to keep the AI focused on banking
        # This prevents the "bank of a river" style responses
        system_context = (
            "You are a professional and helpful Bank Support AI. "
            "Assist the customer with their banking queries accurately.\n"
            f"Customer: {prompt}\n"
            "Assistant:"
        )

        # 2. Generate a response with the context
        output = self.generator(
            system_context, 
            max_new_tokens=40, 
            num_return_sequences=1,
            truncation=True,
            pad_token_id=50256 # Standard for GPT-2 models
        )
        
        full_text = output[0]['generated_text']
        
        # 3. Extract only the AI's new response
        # We find where our prompt ended and take everything after "Assistant:"
        response = full_text.split("Assistant:")[-1].strip()
        
        return response