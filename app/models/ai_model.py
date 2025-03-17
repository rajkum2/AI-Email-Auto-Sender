from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Dict, Any
from config.config import get_settings

settings = get_settings()

class AIModel:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.load_model()

    def load_model(self):
        """Load the AI model and tokenizer."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.AI_MODEL_NAME,
                cache_dir=settings.MODEL_CACHE_DIR
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.AI_MODEL_NAME,
                cache_dir=settings.MODEL_CACHE_DIR,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto"
            )
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    def generate_response(self, prompt: str, max_length: int = 200) -> str:
        """Generate a response from the model."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")

    def analyze_email(self, email_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze email content and return insights."""
        prompt = f"""
        Analyze the following email and provide insights:
        Subject: {email_content.get('subject', '')}
        Content: {email_content.get('content', '')}
        Sender: {email_content.get('sender', '')}
        
        Please provide:
        1. Intent classification
        2. Key topics
        3. Sentiment analysis
        4. Priority level
        """
        
        try:
            response = self.generate_response(prompt)
            # Parse the response into structured data
            # This is a simplified example - you might want to use more sophisticated parsing
            return {
                "raw_analysis": response,
                "intent": self._extract_intent(response),
                "topics": self._extract_topics(response),
                "sentiment": self._extract_sentiment(response),
                "priority": self._extract_priority(response)
            }
        except Exception as e:
            raise Exception(f"Failed to analyze email: {str(e)}")

    def _extract_intent(self, response: str) -> str:
        # Implement intent extraction logic
        return "unknown"

    def _extract_topics(self, response: str) -> list:
        # Implement topic extraction logic
        return []

    def _extract_sentiment(self, response: str) -> str:
        # Implement sentiment extraction logic
        return "neutral"

    def _extract_priority(self, response: str) -> str:
        # Implement priority extraction logic
        return "medium" 