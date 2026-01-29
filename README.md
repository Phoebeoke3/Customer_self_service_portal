# SwissAxa Customer Self-Service Portal

A comprehensive customer self-service portal for SwissAxa insurance company in Nord-Rhein Westfalen (NRW), Germany.

## Features

### 1. myPolicies
- **SwissAxa Policies**: List view of all policies purchased from SwissAxa with expiration dates
- **External Policies**: Upload and manage external insurance policies
- **AI-Powered Comparison**: Compare external policies with SwissAxa products using OpenAI AI technology
  - Get match scores and detailed recommendations
  - Compare coverage and premiums
  - Receive personalized suggestions

### 2. myDocuments
- Upload documents required for policy and claims processing
- Download documents uploaded by customers
- **AI-Powered Auto-Tagging**: Documents are automatically tagged by AI
  - Detects document types: policy, claim, invoice, report, identity, medical, proof_of_ownership, repair_invoice, police_report
  - Select "Auto-detect (AI)" option when uploading

### 3. myBank
- Connect bank accounts (Sparkasse, N26, Deutsche Bank, etc.)
- Initiate debit/credit transactions
- Note: Loans and overdrafts are not available through this channel

### 4. myServices
- **Claims Management**: File claims, upload photos/videos of damages, capture geolocation using Google Maps
  - **AI-Powered Claims Analysis**: AI analyzes uploaded photos/videos
    - Detects damage type (water, fire, theft, collision, etc.)
    - Assesses severity (low, medium, high, critical)
    - Pre-fills claim descriptions automatically
    - Sets priority levels (urgent, normal, low)
    - Estimates claim value ranges
- **Policy Management**: Access policies, upgrade policies, make policy change requests
  - **AI-Powered Recommendations**: Get personalized policy recommendations based on your profile and history
- **Contact Management**: Send emails to SwissAxa Customer Service Desk or Insurance Agent
- **Scheduling**: Book appointments with Customer Service Desk or Insurance Agent
  - **AI-Powered Appointment Suggestions**: Get optimal appointment times based on agent availability patterns

### 5. myInformation
- View and edit personal details
- Manage personal data (name, addresses, email, phone, bank account)
- Update correspondence address
- **AI-Powered Data Validation**: AI checks for inconsistencies in address or identity information
  - Validates address and phone number formats
  - Detects inconsistencies between addresses
  - Prompts re-authentication for sensitive changes

### 6. AI Chatbot 🤖
- **24/7 AI Assistant**: Available in the bottom-right corner of every page
- Answers questions about policies, claims, documents, and general inquiries
- Maintains conversation history for context
- Modern, user-friendly chat interface

## Prerequisites

Before installing, ensure you have the following installed on your system:

- **Python 3.8 or higher** (Python 3.12 recommended)
  - Check your Python version: `python --version` or `python3 --version`
  - Download from [python.org](https://www.python.org/downloads/) if needed
- **pip** (Python package manager - usually comes with Python)
  - Verify installation: `pip --version`
- **Git** (optional, if cloning from repository)

### Installation Quick Reference

| Step | Action | Required? | Time |
|------|--------|-----------|------|
| 1 | Navigate to project directory | ✅ Yes | 1 min |
| 2 | Create virtual environment | ✅ Yes | 1 min |
| 3 | Activate virtual environment | ✅ Yes | - |
| 4 | Install dependencies | ✅ Yes | 2-5 min |
| 5 | Initialize database | ✅ Auto | - |
| 6.1 | Set OpenAI API key | ⚠️ Optional | 2 min |
| 6.2 | Configure email service | ⚠️ Optional | 3 min |
| 6.3 | Set Google Maps API key | ⚠️ Optional | 2 min |
| 7 | Run the application | ✅ Yes | - |
| 8 | Access in browser | ✅ Yes | - |

**Total time (minimal setup):** ~5 minutes  
**Total time (full setup with all features):** ~15 minutes

## Installation

Follow these steps to set up and run the SwissAxa Customer Portal:

### Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project directory:

```bash
cd "C:\Users\User\Desktop\Customer self service portal"
```

Or if you cloned the repository:

```bash
cd "path/to/Customer self service portal"
```

### Step 2: Create Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```bash
python -m venv venv
```

**Note**: If `python` doesn't work, try `python3` on Linux/Mac.

### Step 3: Activate Virtual Environment

Activate the virtual environment before installing dependencies:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Verify activation**: Your terminal prompt should show `(venv)` at the beginning.

### Step 4: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

**Expected output**: You should see packages being installed. This may take a few minutes.

**Verify installation**: Check that Flask is installed:
```bash
pip list | findstr Flask
```
(On Linux/Mac, use: `pip list | grep Flask`)

### Step 5: Initialize Database (Automatic)

The database will be automatically created when you first run the application. No manual setup required.

### Step 6: Configure Optional Features

#### 6.1 OpenAI API Key (Optional - for AI features)

The application works without an API key, but AI features will use mock data.

**To enable AI features:**

1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set the environment variable in your current terminal session:

   **Windows PowerShell:**
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```

   **Windows CMD:**
   ```cmd
   set OPENAI_API_KEY=your-api-key-here
   ```

   **Linux/Mac:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **To make it permanent** (Windows PowerShell):
   ```powershell
   [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'your-api-key-here', 'User')
   ```

   **Linux/Mac** (add to `~/.bashrc` or `~/.zshrc`):
   ```bash
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
   source ~/.bashrc
   ```

**See `AI_SETUP.md` for detailed setup instructions.**

#### 6.2 Email Service (Optional)

Email functionality works without configuration (emails are simulated).

**To enable actual email sending:**

**Windows PowerShell:**
```powershell
$env:MAIL_SERVER="smtp.gmail.com"
$env:MAIL_PORT="587"
$env:MAIL_USE_TLS="True"
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
$env:MAIL_DEFAULT_SENDER="noreply@swissaxa.de"
```

**Linux/Mac:**
```bash
export MAIL_SERVER=smtp.gmail.com
export MAIL_PORT=587
export MAIL_USE_TLS=True
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
export MAIL_DEFAULT_SENDER=noreply@swissaxa.de
```

**See `FEATURE_IMPLEMENTATION_GUIDE.md` for detailed setup.**

#### 6.3 Google Maps API (Optional - for geolocation in claims)

1. Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Edit `templates/claims.html` and replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual key:
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&callback=initMap" async defer></script>
   ```

### Step 7: Run the Application

Start the Flask development server:

**Windows (PowerShell) - Recommended:**
```powershell
.\run_server.ps1
```

**Windows (Command Prompt):**
```cmd
run_server.bat
```

**Linux/Mac:**
```bash
python app.py
```

**Or directly (all platforms):**
```bash
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

**Note**: The server runs on port 5000 by default. If port 5000 is in use, you'll see an error. See [Troubleshooting](#troubleshooting) section.

**To stop the server:** Press `Ctrl+C` in the terminal where the server is running.

### Step 8: Access the Application

1. Open your web browser
2. Navigate to: **http://localhost:5000** or **http://127.0.0.1:5000**
3. You should see the login page

**First-time setup:**
- Register a new account by clicking "Register" or "Sign Up"
- Or use existing credentials if you have them

### Step 9: Verify Installation

To verify everything is working:

1. ✅ Server starts without errors
2. ✅ Browser can access `http://localhost:5000`
3. ✅ Login/Register page loads
4. ✅ Can create a new account
5. ✅ Can log in and see the dashboard

**Quick Test:**
```bash
# In a new terminal (while server is running)
curl http://localhost:5000
# Should return HTML content
```

## Quick Start (Minimal Setup)

For a quick start with minimal configuration:

```bash
# 1. Navigate to project
cd "path/to/Customer self service portal"

# 2. Create and activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or: source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser to http://localhost:5000
```

The application will work with mock AI features and simulated emails. All core functionality is available!

## First Steps After Installation

Once the application is running:

1. **Register a new account:**
   - Go to `http://localhost:5000`
   - Click "Register" or "Sign Up"
   - Fill in your details and create an account

2. **Explore the dashboard:**
   - After logging in, you'll see the main dashboard
   - View overview of policies, documents, claims, and appointments

3. **Try the features:**
   - **myPolicies**: View and manage insurance policies
   - **myDocuments**: Upload and download documents
   - **myBank**: Connect bank accounts (simulated)
   - **myServices**: File claims, manage policies, schedule appointments
   - **myInformation**: Update your personal details

4. **Test AI features:**
   - Click "Show Features" button in the dashboard
   - Try uploading a document with "Auto-detect (AI)" tag
   - Use the AI chatbot in the bottom-right corner
   - Upload a claim with photos for AI analysis

5. **Access advanced features:**
   - Analytics dashboard: `/admin/analytics`
   - Mobile API endpoints: `/api/mobile/*`
   - View UML diagrams: Open `view_uml_diagrams.html` in browser

## Dashboard Wireframe & User Interaction Guide

The dashboard is the central hub where customers can access all portal features. Below is a detailed wireframe showing the layout and how customers interact with each component.

### Dashboard Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  NAVIGATION BAR (Top)                                                       │
│  [SwissAxa Portal] [Dashboard] [myPolicies] [myDocuments] [myBank]           │
│  [myServices ▼] [myInformation]                    [User Name ▼] [Logout]  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  DASHBOARD CONTENT AREA                                                     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Welcome Header                                                       │  │
│  │  🏠 Welcome, [Customer Name]!                                        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ STAT CARD 1  │  │ STAT CARD 2  │  │ STAT CARD 3  │  │ STAT CARD 4  │  │
│  │              │  │              │  │              │  │              │  │
│  │ 📄 Policies  │  │ 📁 Documents │  │ ⚠️  Claims   │  │ 📅 Appts     │  │
│  │     [Count]  │  │     [Count]  │  │     [Count]  │  │     [Count]  │  │
│  │              │  │              │  │              │  │              │  │
│  │ [View →]     │  │ [View →]     │  │ [View →]     │  │ [View →]     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                                              │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐       │
│  │  Recent Policies Card        │  │  Recent Claims Card          │       │
│  │  ────────────────────────    │  │  ────────────────────────    │       │
│  │  📄 Policy #12345            │  │  ⚠️  Claim #CLM-001         │       │
│  │     Auto Insurance           │  │     Water damage...          │       │
│  │     [Active]                 │  │     [Submitted]             │       │
│  │                              │  │                              │       │
│  │  📄 Policy #67890            │  │  ⚠️  Claim #CLM-002         │       │
│  │     Health Insurance         │  │     Theft incident...        │       │
│  │     [Active]                 │  │     [Processing]             │       │
│  │                              │  │                              │       │
│  │  [View All Policies →]      │  │  [View All Claims →]         │       │
│  └──────────────────────────────┘  └──────────────────────────────┘       │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  AI-Powered Features Section (Collapsible)                          │  │
│  │  ────────────────────────────────────────────────────────────────    │  │
│  │  🤖 AI-Powered Features                    [▼ Show Features]       │  │
│  │                                                                    │  │
│  │  [When Expanded:]                                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │ AI Policy │  │ AI Doc   │  │ AI Claims│  │ AI Policy│          │  │
│  │  │ Compare  │  │ Tagging  │  │ Analysis│  │ Recommend│          │  │
│  │  │ [Try It] │  │ [View]   │  │ [File]  │  │ [View]   │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │  │
│  │                                                                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                        │  │
│  │  │ AI Appt  │  │ AI Fraud │  │ AI       │                        │  │
│  │  │ Suggest │  │ Detection│  │ Chatbot  │                        │  │
│  │  │ [Schedule]│  │ [View]  │  │ [Bottom] │                        │  │
│  │  └──────────┘  └──────────┘  └──────────┘                        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  AI CHATBOT WIDGET (Fixed Bottom-Right)                                     │
│                                                                              │
│                                    ┌─────────────┐                          │
│                                    │  🤖 [Badge] │  ← Click to open chat    │
│                                    └─────────────┘                          │
│                                    ┌─────────────┐                          │
│                                    │ AI Assistant│                          │
│                                    │ ─────────── │                          │
│                                    │ [Messages]  │                          │
│                                    │ [Input Box] │                          │
│                                    │ [Send]      │                          │
│                                    └─────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Guide

#### 1. Navigation Bar (Top)
- **Purpose**: Primary navigation to all portal sections
- **Components**:
  - **Brand Logo**: Click to return to dashboard
  - **Menu Items**: 
    - `Dashboard` → Main dashboard (current page)
    - `myPolicies` → View/manage insurance policies
    - `myDocuments` → Upload/download documents
    - `myBank` → Bank account management
    - `myServices` (Dropdown) → Claims, Policy Management, Contact, Scheduling
    - `myInformation` → Personal profile management
  - **User Menu** (Right): Profile settings and logout

**User Actions:**
- Click any menu item to navigate to that section
- Hover over `myServices` to see dropdown menu
- Click user name to access profile/logout options

#### 2. Welcome Header
- **Purpose**: Personalized greeting
- **Content**: "Welcome, [Customer Name]!"
- **User Actions**: None (informational only)

#### 3. Stat Cards (4 Cards in Row)
- **Purpose**: Quick overview of key metrics
- **Cards**:
  1. **SwissAxa Policies** (Blue)
     - Shows count of active policies
     - **Click "View Policies"** → Navigate to policies page
  2. **Documents** (Green)
     - Shows count of uploaded documents
     - **Click "View Documents"** → Navigate to documents page
  3. **Active Claims** (Yellow/Orange)
     - Shows count of submitted claims
     - **Click "View Claims"** → Navigate to claims page
  4. **Appointments** (Cyan)
     - Shows count of scheduled appointments
     - **Click "View Appointments"** → Navigate to scheduling page

**User Actions:**
- Click any card's "View [Section]" button to navigate to detailed view
- Cards are color-coded for quick visual identification

#### 4. Recent Policies Card (Left)
- **Purpose**: Quick view of latest policies
- **Content**: 
  - List of up to 5 most recent policies
  - Each shows: Policy number, type, and status badge
- **User Actions**:
  - **Click "View All Policies"** → Navigate to full policies page
  - Click individual policy items (if clickable) → View policy details

#### 5. Recent Claims Card (Right)
- **Purpose**: Quick view of latest claims
- **Content**:
  - List of up to 5 most recent claims
  - Each shows: Claim number, description preview, and status badge
- **User Actions**:
  - **Click "View All Claims"** → Navigate to full claims page
  - **Click "File a Claim"** (if no claims exist) → Navigate to file claim page
  - Click individual claim items (if clickable) → View claim details

#### 6. AI-Powered Features Section (Collapsible)
- **Purpose**: Showcase and access AI features
- **Default State**: Collapsed (hidden)
- **Components**:
  - Header with "Show Features" button
  - When expanded: Grid of 7 AI feature cards

**User Actions:**
- **Click "Show Features" button** → Expands to show all AI features
- **Click "Hide Features" button** → Collapses the section
- **Click feature cards**:
  - "AI Policy Comparison" → Navigate to policies page
  - "AI Document Tagging" → Navigate to documents page
  - "AI Claims Analysis" → Navigate to claims page
  - "AI Policy Recommendations" → Navigate to policy management
  - "AI Appointment Suggestions" → Navigate to scheduling
  - "AI Fraud Detection" → Navigate to bank page
  - "AI Chatbot" → Opens chatbot widget (see below)

**AI Feature Cards:**
Each card shows:
- Feature name with icon
- Brief description
- "Try It" or "View" button
- Status badge (Available/Coming Soon)

#### 7. AI Chatbot Widget (Fixed Bottom-Right)
- **Purpose**: 24/7 AI-powered customer support
- **Default State**: Minimized (shows robot icon only)
- **Components**:
  - Toggle button with robot icon
  - Notification badge (shows unread count)
  - Chat window (when opened):
    - Header with "AI Assistant" title
    - Message area with conversation history
    - Input box for typing messages
    - Send button

**User Actions:**
- **Click robot icon** → Opens chat window
- **Click close button (X)** → Closes chat window
- **Type message and click Send** → Sends message to AI
- **View conversation history** → Scroll through previous messages
- Chat window can be dragged/resized (if implemented)

### User Journey Examples

#### Example 1: Viewing Policies
```
1. User sees "SwissAxa Policies" stat card showing "5" policies
2. User clicks "View Policies" button on the card
3. → Navigates to /policies page
```

#### Example 2: Filing a Claim with AI Analysis
```
1. User clicks "View Claims" on Active Claims stat card
2. → Navigates to /claims page
3. User clicks "File New Claim" button
4. User uploads damage photos
5. User selects "AI Analysis" option
6. AI analyzes photos and pre-fills claim form
7. User reviews and submits claim
```

#### Example 3: Using AI Chatbot
```
1. User notices robot icon in bottom-right corner
2. User clicks robot icon
3. Chat window opens
4. User types: "What is my policy coverage?"
5. AI responds with policy information
6. User continues conversation
7. User clicks X to close chat
```

#### Example 4: Exploring AI Features
```
1. User scrolls down to "AI-Powered Features" section
2. User clicks "Show Features" button
3. Section expands showing 7 AI feature cards
4. User clicks "AI Policy Comparison" card
5. → Navigates to policies page with comparison feature
6. User uploads external policy for AI comparison
```

### Responsive Design Notes

- **Desktop View**: All components visible in full layout
- **Tablet View**: Stat cards rearrange to 2x2 grid
- **Mobile View**: 
  - Stat cards stack vertically
  - Navigation collapses to hamburger menu
  - Recent Policies/Claims cards stack vertically
  - AI Features section remains collapsible
  - Chatbot widget remains accessible

### Visual Hierarchy

1. **Primary Actions** (Most Prominent):
   - Stat card buttons ("View Policies", "View Documents", etc.)
   - Navigation menu items

2. **Secondary Actions**:
   - "View All" buttons in Recent sections
   - AI feature card buttons
   - "Show Features" toggle

3. **Tertiary Actions**:
   - Individual list items (policies, claims)
   - Chatbot widget toggle

### Accessibility Features

- All interactive elements have hover states
- Color-coded sections for visual identification
- Icons accompany text labels
- Keyboard navigation supported
- Screen reader friendly structure

## Troubleshooting

### Common Issues and Solutions

#### Issue: "ERR_CONNECTION_REFUSED" or Cannot Connect to Server

**Symptoms:** Browser shows connection error when accessing `http://localhost:5000`

**Solutions:**

1. **Check if the server is running:**
   - Look at your terminal - you should see "Running on http://0.0.0.0:5000"
   - If not, start the server: `python app.py`

2. **Check if port 5000 is already in use:**

   **Windows:**
   ```powershell
   netstat -ano | findstr :5000
   ```

   **Linux/Mac:**
   ```bash
   lsof -i :5000
   # or
   netstat -an | grep 5000
   ```

3. **Kill process using port 5000:**

   **Windows:**
   ```powershell
   # Find the PID from step 2, then:
   taskkill /F /PID <process_id>
   ```

   **Linux/Mac:**
   ```bash
   kill -9 <PID>
   ```

4. **Try a different port:**
   - Edit `app.py` line 833: `app.run(debug=True, host='0.0.0.0', port=5001)`
   - Access at `http://localhost:5001`

5. **Verify server is responding:**
   ```powershell
   # Windows PowerShell
   Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing
   ```
   ```bash
   # Linux/Mac
   curl http://localhost:5000
   ```

#### Issue: "ModuleNotFoundError" or Import Errors

**Symptoms:** Error messages about missing modules when running the application

**Solutions:**

1. **Ensure virtual environment is activated:**
   - Your terminal prompt should show `(venv)`
   - If not, activate it: `.\venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Linux/Mac)

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

#### Issue: Database Errors

**Symptoms:** Errors related to database or SQLite

**Solutions:**

1. **Delete existing database and recreate:**
   ```bash
   # Stop the server first (Ctrl+C)
   # Delete the database file
   rm instance/swissaxa_portal.db  # Linux/Mac
   del instance\swissaxa_portal.db  # Windows
   # Restart the server - database will be recreated
   ```

2. **Check file permissions:**
   - Ensure the `instance/` directory is writable
   - On Linux/Mac: `chmod 755 instance/`

#### Issue: "Permission Denied" on Windows PowerShell

**Symptoms:** Cannot run scripts in PowerShell

**Solutions:**

1. **Change execution policy (run PowerShell as Administrator):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Or use Command Prompt instead:**
   ```cmd
   run_server.bat
   ```

#### Issue: AI Features Not Working

**Symptoms:** AI features return mock data or error messages

**Solutions:**

1. **Check if API key is set:**
   ```powershell
   # Windows PowerShell
   echo $env:OPENAI_API_KEY
   ```
   ```bash
   # Linux/Mac
   echo $OPENAI_API_KEY
   ```

2. **Set the API key** (see Step 6.1 in Installation)

3. **Verify API key is valid:**
   - Check your OpenAI account at [platform.openai.com](https://platform.openai.com)
   - Ensure you have credits available

4. **Note:** The application works without an API key - AI features will use fallback/mock data

#### Issue: Test Failures

**Symptoms:** Tests fail when running `pytest`

**Solutions:**

1. **Ensure virtual environment is activated:**
   ```bash
   # Check for (venv) in prompt
   ```

2. **Reinstall test dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests with verbose output:**
   ```bash
   pytest tests/ -v
   ```

4. **Check test database permissions:**
   - Tests use a temporary database
   - Ensure you have write permissions in the project directory

5. **Run specific test file:**
   ```bash
   pytest tests/test_auth.py -v
   ```

#### Issue: Email Not Sending

**Symptoms:** Emails are not being sent

**Solutions:**

1. **Check email configuration:**
   - Verify environment variables are set (see Step 6.2 in Installation)
   - For Gmail, use an "App Password" not your regular password

2. **Check SMTP settings:**
   - Verify server, port, and TLS settings
   - Some email providers require specific configurations

3. **Note:** Without email configuration, emails are simulated (logged to console)

### Getting Help

If you continue to experience issues:

1. **Check the logs:**
   - Server output in terminal shows detailed error messages
   - Look for Python tracebacks

2. **Verify installation:**
   - Python version: `python --version` (should be 3.8+)
   - All dependencies installed: `pip list`
   - Virtual environment activated: prompt shows `(venv)`

3. **Common checks:**
   - ✅ Virtual environment is activated
   - ✅ All dependencies installed (`pip install -r requirements.txt`)
   - ✅ Server is running (check terminal output)
   - ✅ Port 5000 is not in use by another application
   - ✅ Browser is accessing correct URL (`http://localhost:5000`)

### Still Having Issues?

- Review the error messages in your terminal
- Check that you followed all installation steps
- Ensure you're using the correct Python version (3.8+)
- Try running `python app.py` directly to see detailed error messages

## Project Structure

```
Customer self service portal/
├── app.py                      # Main Flask application
├── ai_services.py              # AI service module (OpenAI integration)
├── init_sample_data.py         # Sample data initialization script
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── run_tests.py                # Test runner script
├── run_tests.ps1               # PowerShell test script
├── run_tests.bat               # Windows batch test script
├── run_server.ps1              # PowerShell server script
├── run_server.bat              # Windows batch server script
├── FUNCTIONAL_REQUIREMENTS.md  # Functional requirements document
├── AI_SETUP.md                 # AI features setup guide
├── AI_IMPLEMENTATION_SUMMARY.md # AI implementation details
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── policies.html
│   ├── documents.html
│   ├── bank.html
│   ├── services.html
│   ├── claims.html
│   ├── policy_management.html
│   ├── contact.html
│   ├── scheduling.html
│   └── information.html
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── README.md               # Test documentation
│   ├── test_models.py
│   ├── test_auth.py
│   ├── test_policies.py
│   ├── test_claims.py
│   ├── test_documents.py
│   ├── test_services.py
│   ├── test_information.py
│   └── test_bank.py
├── uploads/                    # Uploaded files
│   ├── documents/
│   ├── policies/
│   └── claims/
├── instance/                   # Instance folder (database)
│   └── swissaxa_portal.db      # SQLite database (created on first run)
└── venv/                       # Virtual environment (not in repo)
```

## Database Models

The application uses SQLAlchemy with SQLite database and includes the following models:
- **User**: Customer accounts
- **Agent**: Insurance agents
- **SwissAxaPolicy**: SwissAxa insurance policies
- **ExternalPolicy**: External insurance policies
- **Document**: Uploaded documents
- **Claim**: Insurance claims
- **ClaimMedia**: Photos/videos for claims
- **PolicyChangeRequest**: Policy change requests
- **Appointment**: Scheduled appointments
- **BankAccount**: Connected bank accounts

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Dashboard**: View overview of policies, documents, claims, and appointments
3. **myPolicies**: View SwissAxa policies and upload external policies for comparison
4. **myDocuments**: Upload and download documents
5. **myBank**: Connect bank accounts and initiate transactions
6. **myServices**: Access claims, policy management, contact, and scheduling features
7. **myInformation**: Update personal details

## Technology Stack

- **Backend**: Flask (Python 3.12)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript (jQuery)
- **Icons**: Font Awesome 6
- **Maps**: Google Maps API (for geolocation)
- **Authentication**: Flask-Login
- **Email**: Flask-Mail (SMTP email sending)
- **Internationalization**: Flask-Babel (multi-language support)
- **Testing**: pytest, pytest-cov, pytest-flask, pytest-mock
- **AI Integration**: OpenAI API
  - GPT-4o-mini (text analysis)
  - GPT-4o Vision (image analysis)
  - AI Policy Comparison
  - AI Document Auto-Tagging
  - AI Claims Analysis (with Vision API)
  - AI Policy Recommendations
  - AI Appointment Suggestions
  - AI Data Validation
  - AI Chatbot
  - AI Fraud Detection
- **Analytics**: Custom analytics tracking system
- **Notifications**: In-app notification system
- **Mobile API**: RESTful API for mobile apps

## Security Notes

- Passwords are hashed using Werkzeug's password hashing
- File uploads are validated and stored securely
- User authentication required for all features
- SQL injection protection via SQLAlchemy ORM

## Testing

The project includes a comprehensive unit test suite using pytest with **76 passing tests** covering all major functionality. All tests are currently passing with **77% code coverage**.

### Quick Start

**Run all tests:**
```bash
pytest tests/ -v
```

**Run with coverage report:**
```bash
python run_tests.py
```

**Run specific test module:**
```bash
pytest tests/test_auth.py -v
```

### Test Scripts

**Windows (PowerShell):**
```powershell
.\run_tests.ps1
```

**Windows (Command Prompt):**
```cmd
run_tests.bat
```

**Linux/Mac:**
```bash
python run_tests.py
```

### Test Coverage

**Latest Test Results**: ✅ **76/76 tests passing** (100% pass rate)  
**Code Coverage**: **77%** (550 statements, 128 missing)

The test suite includes **76 tests** covering:

- ✅ **Database Models** (11 tests)
  - User, Agent, Policy, Claim, Document, BankAccount, Appointment models
  - Relationships and data integrity

- ✅ **Authentication** (13 tests)
  - Login, registration, logout
  - Password hashing and validation
  - Protected route access control

- ✅ **Policy Management** (7 tests)
  - Policy listing and display
  - External policy upload
  - AI-powered policy comparison API
  - Expiration warnings

- ✅ **Claims Management** (5 tests)
  - Filing claims
  - Media upload (photos/videos)
  - Geolocation handling
  - Claim listing

- ✅ **Document Management** (6 tests)
  - Document upload
  - Document download
  - Access control
  - File type validation

- ✅ **Services** (10 tests)
  - Policy change requests
  - Contact (email to service desk/agents)
  - Appointment scheduling
  - Service page navigation

- ✅ **User Information** (3 tests)
  - View user information
  - Update user information
  - Partial updates

- ✅ **Bank Management** (5 tests)
  - Connect bank accounts
  - Bank transactions
  - Account listing

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_models.py           # Database model tests
├── test_auth.py             # Authentication tests
├── test_policies.py         # Policy management tests
├── test_claims.py           # Claims management tests
├── test_documents.py        # Document management tests
├── test_services.py        # Services tests
├── test_information.py     # User information tests
└── test_bank.py            # Bank account tests
```

### Test Features

- **Isolated test database** - Each test uses a temporary SQLite database
- **Automatic cleanup** - Test data is cleaned up after each test
- **Comprehensive fixtures** - Reusable test data for all models
- **Coverage reporting** - HTML and terminal coverage reports
- **Fast execution** - Tests run in ~50-60 seconds
- **Latest run**: All 76 tests passed successfully

See `tests/README.md` for detailed testing documentation and best practices.

## Project Status

✅ **Core Features**: Fully implemented and tested  
✅ **Unit Tests**: 76 tests passing (77% code coverage) - All tests passing as of latest run  
✅ **Documentation**: Complete functional requirements  
✅ **AI Features**: Fully implemented with OpenAI integration  
  - ✅ AI Policy Comparison
  - ✅ AI Document Auto-Tagging
  - ✅ AI Claims Analysis (with Vision API)
  - ✅ AI Policy Recommendations
  - ✅ AI Appointment Suggestions
  - ✅ AI Data Validation
  - ✅ AI Chatbot (24/7 assistant)
  - ✅ AI Fraud Detection
  - ✅ Collapsible AI Features Dashboard Section
✅ **Email Integration**: Fully implemented with Flask-Mail  
✅ **Multi-Language Support**: German and English (Flask-Babel)  
✅ **Notifications System**: In-app notifications implemented  
✅ **Analytics System**: Full tracking and dashboard  
✅ **Mobile API**: REST API endpoints for mobile apps  
✅ **Bank API Structure**: Integration structure ready (requires credentials)  
📋 **Future Enhancements**: See below

## AI Features

The portal includes comprehensive AI-powered features using OpenAI's GPT-4o-mini and GPT-4o Vision models:

### Available AI Features

1. **AI Policy Comparison** - Compare external policies with SwissAxa products using GPT-4o-mini
2. **AI Document Auto-Tagging** - Automatically categorize uploaded documents
3. **AI Claims Analysis** - Analyze damage photos/videos using GPT-4o Vision API and pre-fill claim details
4. **AI Policy Recommendations** - Get personalized policy suggestions based on user profile
5. **AI Appointment Suggestions** - Optimal appointment time recommendations
6. **AI Data Validation** - Check for data inconsistencies in user information
7. **AI Chatbot** - 24/7 customer support assistant (bottom-right corner) using GPT-4o-mini
8. **AI Fraud Detection** - Transaction pattern monitoring and anomaly detection

### AI Features Dashboard

The dashboard includes a collapsible "AI-Powered Features" section:
- Hidden by default for a cleaner interface
- Click "Show Features" button to expand
- Smooth animations and user-friendly interface
- Real-time AI service status indicator

### Setup

See `AI_SETUP.md` for detailed setup instructions and API key configuration.

### Cost Considerations

OpenAI API usage is cost-effective:
- Policy comparison: ~$0.001-0.01 per comparison
- Document tagging: ~$0.0001-0.001 per document
- Claims analysis: ~$0.001-0.01 per claim
- Chatbot: ~$0.001-0.01 per message

**Note**: The application includes fallback mechanisms and works without an API key (using mock data).

## Additional Resources

- **AI Setup Guide**: See `AI_SETUP.md` for detailed AI configuration
- **Feature Implementation Guide**: See `FEATURE_IMPLEMENTATION_GUIDE.md` for advanced features setup
- **Implementation Summary**: See `IMPLEMENTATION_SUMMARY.md` for feature overview
- **Functional Requirements**: See `FUNCTIONAL_REQUIREMENTS.md` for detailed requirements

## API Endpoints

### Mobile API
- `GET /api/mobile/claims` - Get user claims
- `GET /api/mobile/claims/<id>` - Get claim details
- `GET /api/mobile/notifications` - Get notifications
- `GET /api/mobile/policies` - Get policies
- `GET /api/mobile/documents` - Get documents
- `GET /api/mobile/dashboard/stats` - Get dashboard statistics
- `POST /api/mobile/chat` - Mobile chat with AI

### Notifications API
- `GET /api/notifications` - Get user notifications
- `POST /api/notifications/<id>/read` - Mark notification as read

### Language API
- `POST /api/language/<code>` - Switch language (en/de)

### Analytics API
- `GET /admin/analytics` - Analytics dashboard

## Future Enhancements

- **Enhanced Mobile App**: Native iOS/Android applications using the mobile API
- **Real Bank API Integration**: Connect with actual bank APIs (requires credentials)
- **Push Notifications**: Browser push notifications (requires HTTPS)
- **Advanced Reporting**: Enhanced analytics and reporting features
- **Multi-tenant Support**: Support for multiple insurance companies

## Advanced Features

### ✅ Email Integration
- **Status**: Fully implemented
- **File**: `email_service.py`
- **Features**:
  - Send actual emails using Flask-Mail (not simulated)
  - Claim notification emails
  - Appointment confirmation emails
  - Contact email forwarding
  - HTML email support with attachments
- **Setup**: Configure SMTP settings via environment variables (see `FEATURE_IMPLEMENTATION_GUIDE.md`)

### ✅ Enhanced AI Features
- **Status**: Fully implemented
- **Updates**: `ai_services.py`
- **Features**:
  - **OpenAI Vision API**: Image analysis for claims using GPT-4o Vision
  - **Enhanced Document OCR**: Improved document analysis and tagging
  - **Multi-language AI Support**: AI responses in multiple languages
- **Usage**: Claims analysis now accepts image files for visual damage assessment

### ✅ Multi-Language Support
- **Status**: Fully implemented
- **File**: `i18n_support.py`
- **Features**:
  - German and English language support
  - Flask-Babel integration
  - Session-based language selection
  - Language switching API endpoint
- **API**: `POST /api/language/<code>` to switch languages

### ✅ Notifications System
- **Status**: Fully implemented
- **File**: `notifications.py`
- **Features**:
  - In-app notifications
  - Claim status notifications
  - Appointment confirmations
  - Policy update notifications
  - Notification API endpoints
- **API**: `GET /api/notifications` to retrieve notifications

### ✅ Analytics System
- **Status**: Fully implemented
- **File**: `analytics.py`
- **Features**:
  - User activity tracking
  - AI usage analytics
  - Cost tracking and estimation
  - Performance metrics
  - Advanced analytics dashboard
- **Dashboard**: Access at `/admin/analytics`

### ✅ Mobile API
- **Status**: Fully implemented
- **File**: `mobile_api.py`
- **Endpoints**:
  - `GET /api/mobile/claims` - Get user claims
  - `GET /api/mobile/claims/<id>` - Get claim details
  - `GET /api/mobile/notifications` - Get notifications
  - `GET /api/mobile/policies` - Get policies
  - `GET /api/mobile/documents` - Get documents
  - `GET /api/mobile/dashboard/stats` - Get dashboard statistics
  - `POST /api/mobile/chat` - Mobile chat with AI
- **Purpose**: REST API for mobile app development (React Native, Flutter, etc.)

### ✅ Bank API Integration Structure
- **Status**: Structure implemented (requires API credentials)
- **File**: `bank_api_integration.py`
- **Features**:
  - Support for Sparkasse, N26, Deutsche Bank
  - Transaction processing structure
  - Balance checking
  - Transaction verification
- **Note**: Requires actual bank API credentials to function

## Project Structure

```
Customer self service portal/
├── app.py                      # Main Flask application
├── ai_services.py              # AI service module (OpenAI integration)
├── email_service.py            # Email sending service
├── analytics.py                # Analytics tracking system
├── notifications.py            # Notification system
├── i18n_support.py            # Multi-language support
├── mobile_api.py              # Mobile REST API endpoints
├── bank_api_integration.py    # Bank API integration structure
├── init_sample_data.py         # Sample data initialization script
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── run_tests.py                # Test runner script
├── run_tests.ps1               # PowerShell test script
├── run_tests.bat               # Windows batch test script
├── run_server.ps1              # PowerShell server script
├── run_server.bat              # Windows batch server script
├── FUNCTIONAL_REQUIREMENTS.md  # Functional requirements document
├── AI_SETUP.md                 # AI features setup guide
├── AI_IMPLEMENTATION_SUMMARY.md # AI implementation details
├── FEATURE_IMPLEMENTATION_GUIDE.md # Advanced features guide
├── IMPLEMENTATION_SUMMARY.md   # Implementation summary
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── policies.html
│   ├── documents.html
│   ├── bank.html
│   ├── services.html
│   ├── claims.html
│   ├── policy_management.html
│   ├── contact.html
│   ├── scheduling.html
│   ├── information.html
│   └── analytics.html          # Analytics dashboard
├── static/                     # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── README.md               # Test documentation
│   ├── test_models.py
│   ├── test_auth.py
│   ├── test_policies.py
│   ├── test_claims.py
│   ├── test_documents.py
│   ├── test_services.py
│   ├── test_information.py
│   └── test_bank.py
├── uploads/                    # Uploaded files
│   ├── documents/
│   ├── policies/
│   └── claims/
├── instance/                   # Instance folder (database)
│   └── swissaxa_portal.db      # SQLite database (created on first run)
└── venv/                       # Virtual environment (not in repo)
```

## License


## Contact



