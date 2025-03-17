from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class EmailPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class EmailIntent(Enum):
    SALES_INQUIRY = "sales_inquiry"
    SUPPORT_REQUEST = "support_request"
    PARTNERSHIP = "partnership"
    JOB_APPLICATION = "job_application"
    OTHER = "other"

@dataclass
class EmailClassification:
    priority: EmailPriority
    intent: EmailIntent
    topics: List[str]
    sentiment: float
    requires_immediate_response: bool
    suggested_response_time: int  # in hours

class EmailClassifier:
    def __init__(self):
        self.priority_keywords = {
            EmailPriority.HIGH: ["urgent", "asap", "immediate", "critical", "emergency"],
            EmailPriority.MEDIUM: ["please", "request", "would you", "could you"],
            EmailPriority.LOW: ["whenever", "sometime", "no rush"]
        }
        
        self.intent_keywords = {
            EmailIntent.SALES_INQUIRY: ["pricing", "cost", "price", "buy", "purchase"],
            EmailIntent.SUPPORT_REQUEST: ["help", "issue", "problem", "error", "bug"],
            EmailIntent.PARTNERSHIP: ["partnership", "collaboration", "work together"],
            EmailIntent.JOB_APPLICATION: ["job", "position", "career", "resume", "cv"]
        }

    def classify_email(self, email_content: Dict[str, Any]) -> EmailClassification:
        """Classify email content and return structured classification."""
        subject = email_content.get("subject", "").lower()
        content = email_content.get("content", "").lower()
        
        # Determine priority
        priority = self._determine_priority(subject, content)
        
        # Determine intent
        intent = self._determine_intent(subject, content)
        
        # Extract topics
        topics = self._extract_topics(subject, content)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(content)
        
        # Determine response requirements
        requires_immediate = self._requires_immediate_response(priority, intent)
        response_time = self._suggest_response_time(priority, intent)
        
        return EmailClassification(
            priority=priority,
            intent=intent,
            topics=topics,
            sentiment=sentiment,
            requires_immediate_response=requires_immediate,
            suggested_response_time=response_time
        )

    def _determine_priority(self, subject: str, content: str) -> EmailPriority:
        """Determine email priority based on keywords and patterns."""
        for priority, keywords in self.priority_keywords.items():
            if any(keyword in subject or keyword in content for keyword in keywords):
                return priority
        return EmailPriority.MEDIUM

    def _determine_intent(self, subject: str, content: str) -> EmailIntent:
        """Determine email intent based on keywords and patterns."""
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in subject or keyword in content for keyword in keywords):
                return intent
        return EmailIntent.OTHER

    def _extract_topics(self, subject: str, content: str) -> List[str]:
        """Extract main topics from email content."""
        # This is a simplified implementation
        # In a real application, you might want to use NLP techniques
        words = (subject + " " + content).split()
        return list(set(words))[:5]  # Return top 5 unique words as topics

    def _analyze_sentiment(self, content: str) -> float:
        """Analyze sentiment of email content."""
        # This is a simplified implementation
        # In a real application, you might want to use a proper sentiment analysis model
        positive_words = ["great", "good", "excellent", "thank", "thanks", "appreciate"]
        negative_words = ["bad", "poor", "terrible", "issue", "problem", "wrong"]
        
        words = content.split()
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0
        return (pos_count - neg_count) / total

    def _requires_immediate_response(self, priority: EmailPriority, intent: EmailIntent) -> bool:
        """Determine if email requires immediate response."""
        return (priority == EmailPriority.HIGH and 
                intent in [EmailIntent.SALES_INQUIRY, EmailIntent.SUPPORT_REQUEST])

    def _suggest_response_time(self, priority: EmailPriority, intent: EmailIntent) -> int:
        """Suggest response time in hours based on priority and intent."""
        if priority == EmailPriority.HIGH:
            return 1
        elif priority == EmailPriority.MEDIUM:
            return 24
        else:
            return 48 