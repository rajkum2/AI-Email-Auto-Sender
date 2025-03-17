# AI Email Auto Sender

An AI-powered system for automatic email processing and lead qualification. This application uses advanced language models to analyze incoming emails, classify their intent and priority, and automatically manage leads in your CRM system.

## Features

- **AI-Powered Email Analysis**: Uses Mistral 7B/LLaMA2/Falcon models for understanding email content
- **Smart Lead Classification**: Automatically categorizes emails by intent and priority
- **CRM Integration**: Seamlessly integrates with HubSpot, Pipedrive, and Google Sheets
- **Automated Email Responses**: Sends appropriate responses based on email classification
- **RESTful API**: Easy integration with existing systems

## Prerequisites

- Python 3.11+
- CUDA-capable GPU (recommended for AI model inference)
- API keys for:
  - SendGrid
  - HubSpot or Pipedrive
  - Google Sheets API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-email-auto-sender.git
cd ai-email-auto-sender
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment template and fill in your API keys:
```bash
cp .env.example .env
```

## Configuration

Edit the `.env` file with your API keys and configuration:

```env
# API Keys
SENDGRID_API_KEY=your_sendgrid_api_key
HUBSPOT_API_KEY=your_hubspot_api_key
PIPEDRIVE_API_KEY=your_pipedrive_api_key

# Model Configuration
AI_MODEL_NAME=mistralai/Mistral-7B-v0.1
MODEL_CACHE_DIR=./model_cache

# Email Configuration
SENDER_EMAIL=your_sender_email@example.com
DEFAULT_REPLY_TO=your_reply_to@example.com

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS=your_google_sheets_credentials_json
SPREADSHEET_ID=your_spreadsheet_id

# API Configuration
DEBUG=False
```

## Usage

### Running the Application

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

### Using Docker

1. Build the Docker image:
```bash
docker build -t ai-email-auto-sender .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env ai-email-auto-sender
```

## API Endpoints

### Lead Qualification

- `POST /api/v1/leads/qualify`: Process and qualify a new lead
- `GET /api/v1/leads/status/{lead_id}`: Get the status of a lead

### Health Check

- `GET /health`: Check the application health status

## Testing

Run the test suite:
```bash
pytest
```

## Project Structure

```
📂 app
│   ├── 📂 models
│   │   ├── ai_model.py        # Loads Mistral 7B / LLaMA2 / Falcon model
│   │   ├── email_classifier.py # AI-based email analysis logic
│   ├── 📂 routes
│   │   ├── lead_qualification.py  # API routes for processing leads
│   ├── 📂 services
│   │   ├── email_service.py  # Email sending functionality (SendGrid)
│   │   ├── crm_service.py    # CRM integration (HubSpot, Pipedrive)
│   ├── main.py               # FastAPI entry point
📂 config
│   ├── config.py             # Environment variables & API keys
📂 tests
│   ├── test_api.py           # Unit tests for API
│   ├── test_model.py         # Unit tests for AI model
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Mistral AI for the Mistral 7B model
- Meta for LLaMA2
- TII for Falcon
- FastAPI team for the excellent web framework
- All other open-source contributors 