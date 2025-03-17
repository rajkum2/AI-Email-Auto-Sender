from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, List, Optional
from app.models.ai_model import AIModel
from app.models.email_classifier import EmailClassifier, EmailClassification
from app.services.email_service import EmailService
from app.services.crm_service import CRMService
from config.config import get_settings

router = APIRouter()
settings = get_settings()

# Initialize services
ai_model = AIModel()
email_classifier = EmailClassifier()
email_service = EmailService()
crm_service = CRMService()

class LeadData(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None
    subject: str
    content: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class LeadResponse(BaseModel):
    lead_id: str
    classification: EmailClassification
    crm_status: Dict[str, Any]
    email_status: Optional[Dict[str, Any]] = None

@router.post("/qualify", response_model=LeadResponse)
async def qualify_lead(lead_data: LeadData):
    """
    Qualify a lead based on email content and create/update CRM records.
    """
    try:
        # Analyze email content using AI model
        email_analysis = ai_model.analyze_email({
            "subject": lead_data.subject,
            "content": lead_data.content,
            "sender": lead_data.email
        })
        
        # Classify email
        classification = email_classifier.classify_email({
            "subject": lead_data.subject,
            "content": lead_data.content
        })
        
        # Prepare contact data for CRM
        contact_data = {
            "email": lead_data.email,
            "firstname": lead_data.name.split()[0] if lead_data.name else None,
            "lastname": " ".join(lead_data.name.split()[1:]) if lead_data.name and len(lead_data.name.split()) > 1 else None,
            "company": lead_data.company,
            "source": lead_data.source,
            "last_activity_date": "now",
            "email_analysis": email_analysis,
            "classification": classification.dict()
        }
        
        # Create/update contact in CRM
        crm_result = crm_service.create_contact(contact_data)
        
        if crm_result["status"] == "error":
            raise HTTPException(status_code=500, detail=crm_result["message"])
        
        # If it's a sales inquiry, create a deal
        deal_result = None
        if classification.intent.value == "sales_inquiry":
            deal_data = {
                "pipeline": "default",
                "dealname": f"New Inquiry from {lead_data.email}",
                "amount": 0,  # To be updated based on actual inquiry
                "stage": "new",
                "contact_id": crm_result["contact_id"]
            }
            deal_result = crm_service.create_deal(deal_data)
        
        # Log activity in CRM
        activity_data = {
            "type": "email",
            "subject": lead_data.subject,
            "description": lead_data.content,
            "contact_id": crm_result["contact_id"],
            "deal_id": deal_result["deal_id"] if deal_result else None,
            "metadata": lead_data.metadata
        }
        crm_service.log_activity(activity_data)
        
        # Send acknowledgment email if needed
        email_result = None
        if classification.requires_immediate_response:
            email_result = email_service.send_email(
                to_email=lead_data.email,
                subject="Thank you for your inquiry",
                content=f"Dear {lead_data.name or 'there'},\n\nThank you for contacting us. We have received your inquiry and will get back to you shortly.\n\nBest regards,\nYour Company Team",
                html_content=f"""
                    <html>
                        <body>
                            <p>Dear {lead_data.name or 'there'},</p>
                            <p>Thank you for contacting us. We have received your inquiry and will get back to you shortly.</p>
                            <p>Best regards,<br>Your Company Team</p>
                        </body>
                    </html>
                """
            )
        
        return LeadResponse(
            lead_id=crm_result["contact_id"],
            classification=classification,
            crm_status={
                "contact_created": crm_result["status"] == "success",
                "deal_created": deal_result["status"] == "success" if deal_result else False
            },
            email_status=email_result
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{lead_id}")
async def get_lead_status(lead_id: str):
    """
    Get the current status of a lead.
    """
    try:
        # Get contact details from CRM
        contact_data = crm_service.get_contact(lead_id)
        if contact_data["status"] == "error":
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Get associated deals
        deals = crm_service.get_contact_deals(lead_id)
        
        # Get recent activities
        activities = crm_service.get_contact_activities(lead_id)
        
        return {
            "contact": contact_data["data"],
            "deals": deals["data"] if deals["status"] == "success" else [],
            "activities": activities["data"] if activities["status"] == "success" else []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 