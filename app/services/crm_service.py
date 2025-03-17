from typing import Dict, Any, List, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from hubspot import HubSpot
from pipedrive.client import Client as PipedriveClient
from config.config import get_settings

settings = get_settings()

class CRMService:
    def __init__(self):
        self.hubspot_client = HubSpot(api_key=settings.HUBSPOT_API_KEY) if settings.HUBSPOT_API_KEY else None
        self.pipedrive_client = PipedriveClient(api_token=settings.PIPEDRIVE_API_KEY) if settings.PIPEDRIVE_API_KEY else None
        self.sheets_service = self._setup_google_sheets()

    def _setup_google_sheets(self):
        """Setup Google Sheets API service."""
        try:
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(settings.GOOGLE_SHEETS_CREDENTIALS),
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(f"Error setting up Google Sheets: {str(e)}")
            return None

    def create_contact(self, contact_data: Dict[str, Any], crm_type: str = "hubspot") -> Dict[str, Any]:
        """Create a contact in the specified CRM."""
        try:
            if crm_type == "hubspot" and self.hubspot_client:
                response = self.hubspot_client.crm.contacts.basic_api.create(
                    properties=contact_data
                )
                return {"status": "success", "contact_id": response.id}
            
            elif crm_type == "pipedrive" and self.pipedrive_client:
                response = self.pipedrive_client.contacts.create_contact(
                    data=contact_data
                )
                return {"status": "success", "contact_id": response["data"]["id"]}
            
            else:
                return {"status": "error", "message": f"CRM {crm_type} not configured"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_contact(self, contact_id: str, contact_data: Dict[str, Any], crm_type: str = "hubspot") -> Dict[str, Any]:
        """Update a contact in the specified CRM."""
        try:
            if crm_type == "hubspot" and self.hubspot_client:
                response = self.hubspot_client.crm.contacts.basic_api.update(
                    contact_id=contact_id,
                    properties=contact_data
                )
                return {"status": "success", "contact_id": response.id}
            
            elif crm_type == "pipedrive" and self.pipedrive_client:
                response = self.pipedrive_client.contacts.update_contact(
                    id=contact_id,
                    data=contact_data
                )
                return {"status": "success", "contact_id": response["data"]["id"]}
            
            else:
                return {"status": "error", "message": f"CRM {crm_type} not configured"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_deal(self, deal_data: Dict[str, Any], crm_type: str = "hubspot") -> Dict[str, Any]:
        """Create a deal in the specified CRM."""
        try:
            if crm_type == "hubspot" and self.hubspot_client:
                response = self.hubspot_client.crm.deals.basic_api.create(
                    properties=deal_data
                )
                return {"status": "success", "deal_id": response.id}
            
            elif crm_type == "pipedrive" and self.pipedrive_client:
                response = self.pipedrive_client.deals.create_deal(
                    data=deal_data
                )
                return {"status": "success", "deal_id": response["data"]["id"]}
            
            else:
                return {"status": "error", "message": f"CRM {crm_type} not configured"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_deal(self, deal_id: str, deal_data: Dict[str, Any], crm_type: str = "hubspot") -> Dict[str, Any]:
        """Update a deal in the specified CRM."""
        try:
            if crm_type == "hubspot" and self.hubspot_client:
                response = self.hubspot_client.crm.deals.basic_api.update(
                    deal_id=deal_id,
                    properties=deal_data
                )
                return {"status": "success", "deal_id": response.id}
            
            elif crm_type == "pipedrive" and self.pipedrive_client:
                response = self.pipedrive_client.deals.update_deal(
                    id=deal_id,
                    data=deal_data
                )
                return {"status": "success", "deal_id": response["data"]["id"]}
            
            else:
                return {"status": "error", "message": f"CRM {crm_type} not configured"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def log_activity(self, activity_data: Dict[str, Any], crm_type: str = "hubspot") -> Dict[str, Any]:
        """Log an activity in the specified CRM."""
        try:
            if crm_type == "hubspot" and self.hubspot_client:
                response = self.hubspot_client.crm.activities.basic_api.create(
                    properties=activity_data
                )
                return {"status": "success", "activity_id": response.id}
            
            elif crm_type == "pipedrive" and self.pipedrive_client:
                response = self.pipedrive_client.activities.create_activity(
                    data=activity_data
                )
                return {"status": "success", "activity_id": response["data"]["id"]}
            
            else:
                return {"status": "error", "message": f"CRM {crm_type} not configured"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_spreadsheet(self, data: List[List[Any]], range_name: str) -> Dict[str, Any]:
        """Update Google Spreadsheet with provided data."""
        try:
            if not self.sheets_service:
                return {"status": "error", "message": "Google Sheets service not configured"}

            body = {
                'values': data
            }
            
            result = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=settings.SPREADSHEET_ID,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return {
                "status": "success",
                "updated_cells": result.get('updatedCells', 0)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)} 