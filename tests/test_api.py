import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "AI Email Auto Sender"
    assert response.json()["version"] == "1.0.0"

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_qualify_lead_success():
    """Test successful lead qualification."""
    test_lead_data = {
        "email": "test@example.com",
        "name": "Test User",
        "company": "Test Company",
        "subject": "Product Inquiry",
        "content": "I'm interested in your product",
        "source": "website"
    }
    
    # Mock the services
    with patch("app.routes.lead_qualification.ai_model") as mock_ai_model, \
         patch("app.routes.lead_qualification.email_classifier") as mock_classifier, \
         patch("app.routes.lead_qualification.crm_service") as mock_crm_service, \
         patch("app.routes.lead_qualification.email_service") as mock_email_service:
        
        # Setup mock responses
        mock_ai_model.analyze_email.return_value = {
            "intent": "sales_inquiry",
            "sentiment": 0.8
        }
        
        mock_classifier.classify_email.return_value = MagicMock(
            intent=MagicMock(value="sales_inquiry"),
            requires_immediate_response=True
        )
        
        mock_crm_service.create_contact.return_value = {
            "status": "success",
            "contact_id": "test_contact_id"
        }
        
        mock_crm_service.create_deal.return_value = {
            "status": "success",
            "deal_id": "test_deal_id"
        }
        
        mock_crm_service.log_activity.return_value = {
            "status": "success",
            "activity_id": "test_activity_id"
        }
        
        mock_email_service.send_email.return_value = {
            "status_code": 202,
            "message": "Email sent successfully"
        }
        
        # Make the request
        response = client.post("/api/v1/leads/qualify", json=test_lead_data)
        
        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["lead_id"] == "test_contact_id"
        assert response_data["crm_status"]["contact_created"] is True
        assert response_data["crm_status"]["deal_created"] is True
        assert response_data["email_status"]["status_code"] == 202

@pytest.mark.asyncio
async def test_qualify_lead_crm_error():
    """Test lead qualification with CRM error."""
    test_lead_data = {
        "email": "test@example.com",
        "subject": "Product Inquiry",
        "content": "I'm interested in your product"
    }
    
    with patch("app.routes.lead_qualification.crm_service") as mock_crm_service:
        mock_crm_service.create_contact.return_value = {
            "status": "error",
            "message": "CRM service unavailable"
        }
        
        response = client.post("/api/v1/leads/qualify", json=test_lead_data)
        assert response.status_code == 500

@pytest.mark.asyncio
async def test_get_lead_status_success():
    """Test successful lead status retrieval."""
    test_lead_id = "test_contact_id"
    
    with patch("app.routes.lead_qualification.crm_service") as mock_crm_service:
        mock_crm_service.get_contact.return_value = {
            "status": "success",
            "data": {"email": "test@example.com", "name": "Test User"}
        }
        
        mock_crm_service.get_contact_deals.return_value = {
            "status": "success",
            "data": [{"id": "deal1", "amount": 1000}]
        }
        
        mock_crm_service.get_contact_activities.return_value = {
            "status": "success",
            "data": [{"id": "activity1", "type": "email"}]
        }
        
        response = client.get(f"/api/v1/leads/status/{test_lead_id}")
        assert response.status_code == 200
        response_data = response.json()
        assert "contact" in response_data
        assert "deals" in response_data
        assert "activities" in response_data

@pytest.mark.asyncio
async def test_get_lead_status_not_found():
    """Test lead status retrieval for non-existent lead."""
    test_lead_id = "non_existent_id"
    
    with patch("app.routes.lead_qualification.crm_service") as mock_crm_service:
        mock_crm_service.get_contact.return_value = {
            "status": "error",
            "message": "Lead not found"
        }
        
        response = client.get(f"/api/v1/leads/status/{test_lead_id}")
        assert response.status_code == 404 