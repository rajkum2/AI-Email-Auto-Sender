import pytest
from app.models.ai_model import AIModel
from app.models.email_classifier import EmailClassifier, EmailPriority, EmailIntent
from unittest.mock import patch, MagicMock

@pytest.fixture
def ai_model():
    """Fixture for AI model instance."""
    with patch("app.models.ai_model.AutoModelForCausalLM") as mock_model, \
         patch("app.models.ai_model.AutoTokenizer") as mock_tokenizer:
        mock_model.from_pretrained.return_value = MagicMock()
        mock_tokenizer.from_pretrained.return_value = MagicMock()
        return AIModel()

@pytest.fixture
def email_classifier():
    """Fixture for email classifier instance."""
    return EmailClassifier()

def test_ai_model_initialization(ai_model):
    """Test AI model initialization."""
    assert ai_model.model is not None
    assert ai_model.tokenizer is not None
    assert ai_model.device in ["cuda", "cpu"]

def test_ai_model_generate_response(ai_model):
    """Test AI model response generation."""
    test_prompt = "Test prompt"
    test_response = "Test response"
    
    # Mock the tokenizer and model
    ai_model.tokenizer.return_value = {"input_ids": [1, 2, 3]}
    ai_model.model.generate.return_value = [[1, 2, 3, 4]]
    ai_model.tokenizer.decode.return_value = test_response
    
    response = ai_model.generate_response(test_prompt)
    assert response == test_response

def test_ai_model_analyze_email(ai_model):
    """Test email analysis functionality."""
    test_email = {
        "subject": "Product Inquiry",
        "content": "I'm interested in your product",
        "sender": "test@example.com"
    }
    
    # Mock the generate_response method
    ai_model.generate_response.return_value = """
    Intent: sales_inquiry
    Topics: product, pricing, features
    Sentiment: positive
    Priority: high
    """
    
    analysis = ai_model.analyze_email(test_email)
    assert isinstance(analysis, dict)
    assert "intent" in analysis
    assert "topics" in analysis
    assert "sentiment" in analysis
    assert "priority" in analysis

def test_email_classifier_initialization(email_classifier):
    """Test email classifier initialization."""
    assert email_classifier.priority_keywords is not None
    assert email_classifier.intent_keywords is not None

def test_email_classifier_priority_determination(email_classifier):
    """Test email priority classification."""
    # Test high priority
    high_priority_email = {
        "subject": "URGENT: Product Issue",
        "content": "Critical problem needs immediate attention"
    }
    classification = email_classifier.classify_email(high_priority_email)
    assert classification.priority == EmailPriority.HIGH
    
    # Test medium priority
    medium_priority_email = {
        "subject": "Product Question",
        "content": "Please help with product information"
    }
    classification = email_classifier.classify_email(medium_priority_email)
    assert classification.priority == EmailPriority.MEDIUM
    
    # Test low priority
    low_priority_email = {
        "subject": "General Inquiry",
        "content": "When you have time, please respond"
    }
    classification = email_classifier.classify_email(low_priority_email)
    assert classification.priority == EmailPriority.LOW

def test_email_classifier_intent_determination(email_classifier):
    """Test email intent classification."""
    # Test sales inquiry
    sales_email = {
        "subject": "Product Pricing",
        "content": "What are your product prices?"
    }
    classification = email_classifier.classify_email(sales_email)
    assert classification.intent == EmailIntent.SALES_INQUIRY
    
    # Test support request
    support_email = {
        "subject": "Technical Issue",
        "content": "Need help with product problem"
    }
    classification = email_classifier.classify_email(support_email)
    assert classification.intent == EmailIntent.SUPPORT_REQUEST
    
    # Test partnership
    partnership_email = {
        "subject": "Partnership Opportunity",
        "content": "Let's work together"
    }
    classification = email_classifier.classify_email(partnership_email)
    assert classification.intent == EmailIntent.PARTNERSHIP

def test_email_classifier_sentiment_analysis(email_classifier):
    """Test email sentiment analysis."""
    # Test positive sentiment
    positive_email = {
        "subject": "Great Product",
        "content": "Thank you for the excellent service"
    }
    classification = email_classifier.classify_email(positive_email)
    assert classification.sentiment > 0
    
    # Test negative sentiment
    negative_email = {
        "subject": "Poor Service",
        "content": "Terrible experience with your product"
    }
    classification = email_classifier.classify_email(negative_email)
    assert classification.sentiment < 0

def test_email_classifier_response_time(email_classifier):
    """Test response time suggestions."""
    # Test immediate response
    urgent_email = {
        "subject": "URGENT: Sales Inquiry",
        "content": "Need pricing information ASAP"
    }
    classification = email_classifier.classify_email(urgent_email)
    assert classification.requires_immediate_response is True
    assert classification.suggested_response_time == 1
    
    # Test delayed response
    non_urgent_email = {
        "subject": "General Question",
        "content": "When you have time"
    }
    classification = email_classifier.classify_email(non_urgent_email)
    assert classification.requires_immediate_response is False
    assert classification.suggested_response_time == 48 