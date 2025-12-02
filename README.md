# Cyber Data Summarization Agent

An AI-powered full-stack application that analyzes and summarizes Cybersecurity host data, providing actionable security insights for SOC analysts, security engineers, and IT administrators.

## 🎯 Project Overview

This application leverages Large Language Models (LLMs) to automatically analyze cybersecurity host data, identifying vulnerabilities, malware, and security risks. It provides three levels of analysis (Brief, Detailed, Technical) tailored to different audiences.

### Key Features

- 🤖 **AI-Powered Analysis**: Uses Groq's Llama 3.3 70B model for intelligent summarization
- 🔍 **Vulnerability Detection**: Automatically identifies CVEs with CVSS scores
- 🚨 **Malware Detection**: Detects C2 servers and threat actor associations
- 📊 **Statistical Insights**: Generates key metrics and risk assessments
- 📁 **Flexible Input**: Supports both sample data and JSON file uploads
- 🎨 **Clean UI**: Intuitive interface built with vanilla JavaScript
- ⚡ **Fast Processing**: Typically completes analysis in 10-15 seconds

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Flask 3.0.0 (Python web framework)
- Groq API (Llama 3.3 70B model)
- Pandas (Data processing and statistics)
- Python-dotenv (Environment management)

**Frontend:**
- Vanilla JavaScript (No frameworks)
- HTML5/CSS3
- Marked.js (Markdown rendering)
- Font Awesome (Icons)

### Project Structure

```
censys-summarization-agent/
├── backend/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py          # AI/LLM integration
│   │   └── data_processor.py      # Data cleaning and statistics
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py             # Utility functions
│   ├── data/
│   │   └── sample_hosts.json      # Sample Censys data
│   ├── app.py                     # Main Flask application
│   ├── config.py                  # Configuration management
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment variables (not in repo)
├── frontend/
│   ├── css/
│   │   └── style.css              # Application styles
│   ├── js/
│   │   ├── main.js                # Main application logic
│   │   ├── api.js                 # API client
│   │   └── utils.js               # UI utilities
│   └── index.html                 # Main HTML page
├── README.md                      # This file
├── FUTURE_ENHANCEMENTS.md         # Planned improvements
└── .gitignore                     # Git ignore file
```

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Groq API key (free tier available)

## 🚀 Installation

### Step 1: Get a Groq API Key

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

### Step 2: Set Up the Project

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Create .env file
touch .env  # On macOS/Linux
# OR
type nul > .env  # On Windows
```

Add the following content to `.env`:

```properties
# Groq API Configuration
GROQ_API_KEY=your-groq-api-key-here
AI_PROVIDER=groq

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Logging
LOG_LEVEL=INFO
```

**Important:** Replace `your-groq-api-key-here` with your actual Groq API key.

## ▶️ Running the Application

### Start the Backend Server

```bash
# Make sure you're in the backend directory with venv activated
cd backend
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

The application interface will load automatically.

## 🧪 Testing Instructions

### Manual Testing

#### Test 1: Load Sample Data

1. Click the **"Load Sample Data"** button
2. Verify that the Data Preview section appears
3. Check that 3 hosts are displayed with:
   - IP addresses
   - Locations (US, China)
   - Vulnerability counts
   - Risk badges (HIGH, CRITICAL)
   - Malware alert for Cobalt Strike

**Expected Result:** Preview shows 3 hosts with security indicators

#### Test 2: Generate Summary (Detailed)

1. After loading sample data, ensure "Detailed" is selected in the dropdown
2. Click **"Generate Summary"**
3. Wait 10-15 seconds for AI analysis
4. Verify the results section contains:
   - Comprehensive summary with sections
   - 5 key insights as bullet points
   - Risk assessment paragraph
   - Statistics cards showing:
     - Total hosts (3)
     - Total vulnerabilities
     - Critical vulnerability hosts
     - Malware detected hosts
     - Geographic distribution
     - Risk levels

**Expected Result:** Complete security analysis identifying CVE-2023-38408, CVE-2024-6387, Cobalt Strike malware, and threat actors (FIN7, APT41)

#### Test 3: Different Summary Types

1. Load sample data
2. Select **"Brief"** from dropdown
3. Generate summary - should be 3-4 paragraphs, executive-level
4. Reload sample data
5. Select **"Technical"** from dropdown
6. Generate summary - should be very detailed with commands and procedures

**Expected Result:** Each summary type produces different length and detail level

#### Test 4: File Upload

1. Click **"Upload JSON File"**
2. Select the `backend/data/sample_hosts.json` file (or provided `hosts_dataset.json`)
3. Verify data preview appears with correct host count
4. Generate summary

**Expected Result:** File uploads successfully and analysis completes

### API Testing (Optional)

Test the backend API directly using curl or Postman:

```bash
# Health check
curl http://localhost:5000/api/health

# Get sample data
curl http://localhost:5000/api/sample-data

# Test summarization
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d @backend/data/sample_hosts.json
```

### Expected Output Example

For the provided dataset, the application should identify:

**Vulnerabilities:**
- CVE-2023-38408 (Critical, CVSS 9.8) - all hosts
- CVE-2024-6387 (High, CVSS 8.1) - 2 hosts
- CVE-2018-15473 (Medium, CVSS 5.3) - 1 host

**Malware:**
- Cobalt Strike C2 server on 1.92.135.168
- Associated threat actors: FIN7, APT41, Cobalt Group

**Risk Levels:**
- 1 Critical risk host
- 2 High risk hosts

## 🤖 AI Techniques Used

This project demonstrates several advanced AI/ML techniques:

### 1. Prompt Engineering

**Structured Prompts:**
- Multi-section prompts with clear objectives and output requirements
- Explicit formatting instructions to ensure consistent responses
- Domain-specific vocabulary (CVE IDs, CVSS scores, threat actors)

**Role-Based Context:**
- System messages define the AI as a "cybersecurity analyst"
- Sets expectations for technical accuracy and security focus

**Conditional Prompting:**
- Different prompts for Brief/Detailed/Technical summaries
- Adjusts depth and audience based on user selection

**Example Prompt Structure:**
```
You are a cybersecurity analyst...
Analyze this host data: [JSON]
Provide analysis including:
1. Overview
2. Vulnerabilities (CVEs with CVSS)
3. Malware detection
...
Be specific about CVE IDs and threat actors.
```

### 2. Multi-Stage Analysis Pipeline

The application uses a three-stage approach:

1. **Primary Analysis** (Main Summary)
   - Comprehensive security assessment
   - Temperature: 0.3 for factual consistency
   - Max tokens: 500-2000 based on summary type

2. **Insight Extraction** (Key Findings)
   - Focused prompt for critical insights
   - Temperature: 0.2 for precision
   - Max tokens: 300

3. **Risk Assessment** (Security Evaluation)
   - Risk-focused analysis
   - Temperature: 0.2 for reliable assessment
   - Max tokens: 200

**Why Multi-Stage?**
- Prevents overwhelming single prompts
- Allows fine-tuned control per output type
- Reduces hallucination through focused queries
- Improves response quality and consistency

### 3. Temperature Control

Different temperatures for different tasks:
- **0.3** for main summary: Balance between creativity and factuality
- **0.2** for insights/risk: Prioritize consistency and accuracy
- Lower temperatures reduce randomness in security-critical analysis

### 4. Token Management

Strategic token limits prevent verbose responses:
- Brief: 500 tokens (concise)
- Detailed: 1500 tokens (balanced)
- Technical: 2000 tokens (comprehensive)

### 5. Model Selection: Groq Llama 3.3 70B

**Why Groq?**
- **Speed**: 100+ tokens/second vs OpenAI's ~30 tokens/second
- **Cost**: Free tier with generous limits (no credit card required)
- **Quality**: 70B parameter model with strong reasoning
- **Reliability**: Consistent performance for structured tasks

**Why Llama 3.3 70B specifically?**
- Excellent instruction following
- Strong performance on technical/domain-specific content
- Good at structured output (sections, bullet points)
- Balances capability with inference speed

### 6. Data Preprocessing

Before AI analysis:
- Clean and normalize JSON structure
- Extract nested fields (services, vulnerabilities, malware)
- Calculate statistics (vulnerability counts, risk levels)
- Handle both wrapped and unwrapped JSON formats

**Benefits:**
- Reduces noise in AI prompts
- Provides pre-calculated stats for verification
- Handles edge cases in data structure

### 7. Context Optimization

- JSON data passed directly to preserve structure
- Selective field extraction (only relevant security data)
- Balanced context size (not too large, not too small)

### 8. Error Handling & Fallbacks

- Graceful degradation if AI fails
- Timeout handling (180 seconds)
- Structured try-catch blocks
- User-friendly error messages

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Your Groq API key | None | Yes |
| `AI_PROVIDER` | AI provider name | `groq` | No |
| `FLASK_ENV` | Flask environment | `development` | No |
| `FLASK_DEBUG` | Enable debug mode | `True` | No |
| `PORT` | Server port | `5000` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Changing AI Models

To use a different Groq model, edit `backend/services/ai_service.py`:

```python
self.model = "llama-3.3-70b-versatile"  # Current
# Or try:
# self.model = "mixtral-8x7b-32768"
# self.model = "gemma2-9b-it"
```

## 🧩 Assumptions

1. **Data Format**: Input data follows Censys host data schema with fields like `ip`, `services`, `vulnerabilities`, `threat_intelligence`

2. **API Availability**: Requires active internet connection for Groq API calls

3. **Rate Limits**: Free tier Groq account is sufficient for demonstration purposes (30 requests/minute)

4. **Data Size**: Optimized for datasets of 1-100 hosts. Larger datasets may require pagination or chunking

5. **Browser Compatibility**: Requires modern browser with ES6+ JavaScript support

6. **Security**: Application runs locally. In production, would require authentication, HTTPS, and input sanitization

7. **JSON Format**: Accepts both:
   - Wrapped format: `{"metadata": {...}, "hosts": [...]}`
   - Direct array: `[{host1}, {host2}, ...]`

## 🐛 Troubleshooting

### "Unable to connect to backend API"
- Ensure Flask server is running (`python app.py`)
- Check that port 5000 is not in use by another application
- Verify firewall isn't blocking localhost connections

### "Failed to generate summary: 401 Unauthorized"
- Check that `GROQ_API_KEY` in `.env` is correct
- Verify API key is active at https://console.groq.com
- Ensure no extra spaces in the `.env` file

### "Analysis taking too long"
- Groq's free tier occasionally has high demand
- Try again in a few minutes
- Check internet connection stability

### "Invalid JSON format"
- Ensure uploaded file is valid JSON
- Check file uses UTF-8 encoding
- Verify structure matches Censys format

### File upload not working
- Check file size (should be under 10MB)
- Ensure file extension is `.json`
- Try the "Load Sample Data" button first to verify system works

### Markdown not rendering (showing ** and ` marks)
- Clear browser cache
- Verify `marked.js` CDN is accessible
- Check browser console for JavaScript errors

## 📊 Performance

Typical performance metrics on standard hardware:

- **Load Sample Data**: < 1 second
- **File Upload**: 1-2 seconds
- **AI Analysis (Brief)**: 8-12 seconds
- **AI Analysis (Detailed)**: 10-15 seconds
- **AI Analysis (Technical)**: 15-20 seconds
- **Memory Usage**: ~100MB (backend)

## 🔒 Security Considerations

**Current Implementation:**
- Runs locally on localhost
- No user authentication
- API key stored in environment variable

**Production Recommendations:**
- Add user authentication (JWT, OAuth)
- Implement rate limiting per user
- Use HTTPS/TLS for all connections
- Sanitize all user inputs
- Store API keys in secure vault (e.g., AWS Secrets Manager)
- Add CORS restrictions
- Implement audit logging
- Add input size limits

## 📝 License

MIT License - feel free to use this project for learning and development.

## 👤 Author

Abdur Razzaq
- **Date**: January 2025

## 🙏 Acknowledgments

- Groq for providing fast, free LLM inference
- OpenSSH, Nginx, and other open-source projects whose vulnerabilities appear in the dataset

## 📞 Support

For questions or issues with this project, please refer to:
- Project documentation in this README
- Inline code comments
- FUTURE_ENHANCEMENTS.md for planned improvements

