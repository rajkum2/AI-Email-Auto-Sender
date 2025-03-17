from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
from typing import Dict, Any, List, Optional
from config.config import get_settings

settings = get_settings()

class EmailService:
    def __init__(self):
        self.sg_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.sender_email = Email(settings.SENDER_EMAIL)
        self.reply_to = settings.DEFAULT_REPLY_TO

    def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        html_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email using SendGrid.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            content: Plain text content
            html_content: Optional HTML content
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            reply_to: Optional reply-to email address
            
        Returns:
            Dict containing response status and message
        """
        try:
            to_email = To(to_email)
            
            # Create email content
            if html_content:
                content = HtmlContent(html_content)
            else:
                content = Content("text/plain", content)
            
            # Create mail object
            mail = Mail(
                from_email=self.sender_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=content if not html_content else None,
                html_content=html_content if html_content else None,
                reply_to=reply_to or self.reply_to
            )
            
            # Add CC recipients if provided
            if cc:
                mail.add_cc(cc)
            
            # Add BCC recipients if provided
            if bcc:
                mail.add_bcc(bcc)
            
            # Send email
            response = self.sg_client.send(mail)
            
            return {
                "status_code": response.status_code,
                "message": "Email sent successfully" if response.status_code == 202 else "Failed to send email",
                "response_body": response.body
            }
            
        except Exception as e:
            return {
                "status_code": 500,
                "message": f"Error sending email: {str(e)}",
                "response_body": None
            }

    def send_template_email(
        self,
        to_email: str,
        template_id: str,
        template_data: Dict[str, Any],
        subject: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email using a SendGrid template.
        
        Args:
            to_email: Recipient email address
            template_id: SendGrid template ID
            template_data: Data to populate template variables
            subject: Optional subject (if not in template)
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            reply_to: Optional reply-to email address
            
        Returns:
            Dict containing response status and message
        """
        try:
            to_email = To(to_email)
            
            # Create mail object with template
            mail = Mail(
                from_email=self.sender_email,
                to_emails=to_email,
                subject=subject,
                template_id=template_id,
                dynamic_template_data=template_data,
                reply_to=reply_to or self.reply_to
            )
            
            # Add CC recipients if provided
            if cc:
                mail.add_cc(cc)
            
            # Add BCC recipients if provided
            if bcc:
                mail.add_bcc(bcc)
            
            # Send email
            response = self.sg_client.send(mail)
            
            return {
                "status_code": response.status_code,
                "message": "Template email sent successfully" if response.status_code == 202 else "Failed to send template email",
                "response_body": response.body
            }
            
        except Exception as e:
            return {
                "status_code": 500,
                "message": f"Error sending template email: {str(e)}",
                "response_body": None
            }

    def send_bulk_emails(
        self,
        recipients: List[Dict[str, Any]],
        subject: str,
        content: str,
        html_content: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Send emails to multiple recipients.
        
        Args:
            recipients: List of recipient dictionaries containing email and optional personalization data
            subject: Email subject
            content: Plain text content
            html_content: Optional HTML content
            
        Returns:
            List of response dictionaries for each email
        """
        results = []
        for recipient in recipients:
            result = self.send_email(
                to_email=recipient["email"],
                subject=subject,
                content=content,
                html_content=html_content,
                cc=recipient.get("cc"),
                bcc=recipient.get("bcc")
            )
            results.append(result)
        return results 