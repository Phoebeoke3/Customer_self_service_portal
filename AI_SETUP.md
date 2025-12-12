# AI Features Setup Guide

This guide explains how to set up and use the AI-powered features in the SwissAxa Portal.

## Prerequisites

1. **OpenAI API Key** - Required for AI features
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Create an API key from [API Keys page](https://platform.openai.com/api-keys)
   - Copy your API key

## Setup Instructions

### 1. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Create .env File (Recommended)

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
GOOGLE_MAPS_API_KEY=your-google-maps-key-here
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

And update `app.py` to load environment variables:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. Verify Setup

1. Start the application
2. Check the console for AI service status
3. Try uploading a document with "Auto-detect" option
4. Test the chatbot in the bottom-right corner

## Available AI Features

### ✅ Implemented Features

1. **AI Policy Comparison**
   - Location: Policies page → External Policies → Compare button
   - Uses OpenAI to compare external policies with SwissAxa products
   - Provides match scores and recommendations

2. **AI Document Auto-Tagging**
   - Location: Documents page → Upload Document
   - Select "Auto-detect (AI)" option
   - AI automatically tags documents (policy, claim, invoice, report, etc.)

3. **AI Claims Analysis**
   - Location: Claims page → File a New Claim
   - Upload photos/videos of damage
   - AI analyzes damage type and severity
   - Pre-fills claim description based on analysis
   - Sets priority (urgent/normal)

4. **AI Policy Recommendations**
   - Location: Policy Management page
   - Click "Get AI Recommendations"
   - Get personalized policy suggestions based on your profile

5. **AI Data Validation**
   - Location: Information page → Update Information
   - AI checks for inconsistencies in address/identity data
   - Prompts re-authentication if needed

6. **AI Chatbot**
   - Location: Bottom-right corner (robot icon)
   - 24/7 AI assistant for customer support
   - Answers questions about policies, claims, documents

### 🔄 Coming Soon

- AI Appointment Suggestions
- AI Transaction Monitoring
- Enhanced image analysis for claims

## API Costs

**Note:** OpenAI API usage incurs costs based on:
- Model used (gpt-4o-mini is cost-effective)
- Number of tokens processed
- Number of API calls

**Estimated costs:**
- Policy comparison: ~$0.001-0.01 per comparison
- Document tagging: ~$0.0001-0.001 per document
- Claims analysis: ~$0.001-0.01 per claim
- Chatbot: ~$0.001-0.01 per message

**Cost-saving tips:**
- The system includes fallback mechanisms when AI is unavailable
- Responses are cached where appropriate
- Use gpt-4o-mini for most operations (cost-effective)

## Troubleshooting

### AI Features Not Working

1. **Check API Key:**
   ```python
   import os
   print(os.getenv('OPENAI_API_KEY'))
   ```

2. **Check API Balance:**
   - Visit [OpenAI Usage Dashboard](https://platform.openai.com/usage)
   - Ensure you have credits available

3. **Check Console Logs:**
   - Look for "AI services are currently unavailable" messages
   - Check for API error messages

### Fallback Behavior

If OpenAI API is not configured or unavailable:
- Policy comparison uses mock data
- Document tagging uses filename-based guessing
- Claims analysis uses basic processing
- Chatbot shows "unavailable" message
- All other features work normally

## Security & Privacy

- API keys are stored in environment variables (never in code)
- Personal data sent to OpenAI is minimized
- AI responses are logged for audit purposes
- Users can opt-out of AI features (coming soon)

## Support

For issues with AI features:
1. Check this guide
2. Review console logs
3. Verify API key is set correctly
4. Check OpenAI service status

