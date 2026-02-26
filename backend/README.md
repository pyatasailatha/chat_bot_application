# AI-Powered College Enquiry Chatbot

This is an intelligent chatbot system that uses OpenAI's GPT-3.5-turbo API to answer college-related queries dynamically. The system is fully trainable with custom data and can be easily extended.
# Backend

This folder contains the Flask backend for the chatbot.

## 🚀 Features

- **AI-Powered Responses**: Uses OpenAI GPT-3.5-turbo for intelligent, context-aware responses
- **Dynamic Training**: Add, update, and manage training data on the fly
- **Multiple Categories**: Organize information by category (admissions, courses, timings, hostel, placements, etc.)
- **Fallback System**: Falls back to keyword matching if API fails
- **REST API**: Clean API endpoints for easy integration
- **Admin Panel**: Simple interface to manage training data
- **College-Specific**: Built specifically for college enquiry systems

## 📋 Prerequisites

- Python 3.8+
- Node.js (for frontend, optional)
- OpenAI API Key (get from https://platform.openai.com/api-keys)

## 🔧 Installation

### 1. Clone/Setup the project

```bash
cd c:\chatbot\backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the backend directory:

```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
DEBUG=True
MONGO_URI=mongodb://localhost:27017
MONGO_DB=chatbot_db
ADMIN_USER=admin
ADMIN_PASSWORD=adminpass
```

**To get your OpenAI API Key:**
1. Go to https://platform.openai.com/account/api-keys
2. Create a new API key
3. Paste it in the `.env` file

### 5. Verify installation

```bash
python app.py
```

You should see: `Running on http://127.0.0.1:5000`

## 📚 Training Data Structure

The training data is stored in `training_data.json` with the following structure:

```json
{
  "college_info": {
    "name": "College Name",
    "location": "City, State",
    "phone": "+91-XXXXXXXXXX",
    "email": "info@college.edu"
  },
  "training_data": [
    {
      "question": "What is the fee?",
      "answer": "CSE fee is ₹90,000 per year.",
      "category": "courses"
    }
  ]
}
```

## 🛠️ Managing Training Data

### Method 1: Using Python Script

```bash
python manage_data.py
```

This script helps you add multiple training entries at once.

### Method 2: Using API Endpoints

#### Add Training Data
```bash
POST /add-training-data
Content-Type: application/json

{
  "question": "What is the admission fee?",
  "answer": "Admission fee is ₹500.",
  "category": "admissions"
}
```

#### Update College Info
```bash
POST /update-college-info
Content-Type: application/json

{
  "phone": "+91-44-XXXXX",
  "email": "info@college.edu",
  "website": "www.college.edu"
}
```

#### Get All Training Data
```bash
GET /get-training-data
```

#### Health Check
```bash
GET /health
```

### Method 3: Using Frontend Admin Panel

The frontend includes an admin panel with buttons to:
- ➕ Add Training Data
- 📊 View Training Data
- 💚 System Health

## 🎯 API Endpoints

### Chat Endpoint
```
POST /chat
Content-Type: application/json

Request:
{
  "message": "What are the lecture timings?"
}

Response:
{
  "reply": "Each lecture is 50 minutes."
}
```

### Training Data Endpoints
- `POST /add-training-data` - Add new Q&A pair
- `GET /get-training-data` - Get all training data
- `POST /update-college-info` - Update college information
- `GET /health` - Check system status

## 📖 How It Works

1. **User sends a question** via the frontend or API
2. **AI processes the question** using the training data as context
3. **OpenAI GPT-3.5** generates an intelligent response based on:
   - College information
   - Training data (Q&A pairs)
   - System prompt (role and guidelines)
4. **Response is returned** to the user

### Fallback Mechanism
If OpenAI API fails:
- System falls back to keyword matching
- Uses the legacy responses dictionary
- Ensures service doesn't completely break

## 🚀 Starting the Application

### Backend
```bash
cd backend
.\venv\Scripts\Activate
python app.py
```

### Frontend
Open `frontend/index.html` in a web browser

Or start a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
```

Then visit: `http://localhost:8000`

## 📊 Training Data Categories

Default categories include:
- **timings** - Lecture hours, exam timings, office hours
- **admissions** - Fees, eligibility, application process
- **courses** - Course details, intake, fees
- **hostel** - Room details, curfew, dining
- **placements** - Placement process, eligibility
- **infrastructure** - Labs, library, sports facilities
- **faculty** - Faculty info, mentoring
- **exams** - Hall ticket, results, revaluation

## 💡 Best Practices

1. **Keep answers concise** - AI works better with clear, short answers
2. **Use consistent formatting** - Standardize answer format across categories
3. **Include relevant details** - Add contact info when applicable
4. **Regular updates** - Update training data as policies change
5. **Test responses** - Verify AI responses make sense in context

## 🔒 Security Notes

- Keep your OpenAI API key secure (never commit `.env` file)
- Add authentication for admin endpoints before production
- Validate all inputs
- Consider rate limiting for API endpoints

## 📝 Example Training Data

Here's a well-structured example to add:

```json
[
  {
    "question": "How do I contact the admissions office?",
    "answer": "You can call us at +91 9876543210 or email admissions@college.edu. Our office is open from 9:30 AM to 4:30 PM, Monday to Friday.",
    "category": "admissions"
  },
  {
    "question": "What scholarships are available?",
    "answer": "We offer merit-based and need-based scholarships. Applications are reviewed after admission. Visit the financial aid office for details.",
    "category": "admissions"
  }
]
```

## 🐛 Troubleshooting

### OpenAI API Key Error
- Verify the API key in `.env` file
- Check if the key has sufficient credits
- Make sure the key has chat completion permissions

### CORS Errors
- Frontend should be on same origin or CORS is enabled (it is)
- Check if backend is running on port 5000

### Training Data Not Updating
- Verify the JSON syntax is valid
- Check file permissions
- Restart the backend after adding data

## 📞 Support Categories

The system is pre-configured for:
- College policies and timings
- Admission procedures and fees
- Course information and intake
- Hostel facilities and rules
- Placement statistics and process
- Infrastructure and facilities
- Faculty information
- Exam procedures

## 🎓 Future Enhancements

- Database integration (replace JSON)
- Authentication for admin panel
- Analytics and usage tracking
- Multi-language support
- Custom model training
- Sentiment analysis
- Response rating system

## 📄 License

This project is open for educational use in colleges.

## 🙋 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the training data structure
3. Verify OpenAI API setup
4. Check console logs for errors
