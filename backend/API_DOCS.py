"""
API Documentation for College Enquiry Chatbot

Base URL: http://localhost:5000
"""

# CHAT ENDPOINT
# =============================================================================
"""
POST /chat

Description: Send a message and get a response from the AI chatbot

Request:
  Headers:
    Content-Type: application/json
  
  Body:
    {
      "message": "What is the duration of each lecture?"
    }

Response (200 OK):
  {
    "reply": "Each lecture is 50 minutes."
  }

Example cURL:
  curl -X POST http://localhost:5000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is the fee for CSE?"}'

Example Python:
  import requests
  
  url = "http://localhost:5000/chat"
  data = {"message": "What is the fee for CSE?"}
  response = requests.post(url, json=data)
  print(response.json())
"""

# ADD TRAINING DATA ENDPOINT
# =============================================================================
"""
POST /add-training-data

Description: Add a new question-answer pair to the training data

Request:
  Headers:
    Content-Type: application/json
  
  Body:
    {
      "question": "What is the application fee?",
      "answer": "Application fee is ₹500.",
      "category": "admissions"
    }

Response (200 OK):
  {
    "success": true,
    "message": "Training data added successfully"
  }

Error Response (400 Bad Request):
  {
    "error": "Question and answer are required"
  }

Categories:
  - admissions
  - courses
  - timings
  - hostel
  - placements
  - infrastructure
  - faculty
  - exams
  - general

Example Python:
  import requests
  
  url = "http://localhost:5000/add-training-data"
  data = {
    "question": "What is the hostel fee?",
    "answer": "Hostel fee is ₹60,000 per year.",
    "category": "hostel"
  }
  response = requests.post(url, json=data)
  print(response.json())
"""

# GET TRAINING DATA ENDPOINT
# =============================================================================
"""
GET /get-training-data

Description: Retrieve all training data

Response (200 OK):
  {
    "college_info": {
      "name": "Your College Name",
      "location": "Chennai, Tamil Nadu, India"
    },
    "training_data": [
      {
        "question": "What is the fee?",
        "answer": "CSE fee is ₹90,000 per year.",
        "category": "courses"
      },
      ...
    ]
  }

Example Python:
  import requests
  
  response = requests.get("http://localhost:5000/get-training-data")
  data = response.json()
  print(f"Total entries: {len(data['training_data'])}")
  for entry in data['training_data']:
    print(f"Q: {entry['question']}")
    print(f"A: {entry['answer']}\n")
"""

# UPDATE COLLEGE INFO ENDPOINT
# =============================================================================
"""
POST /update-college-info

Description: Update college information

Request:
  Headers:
    Content-Type: application/json
  
  Body:
    {
      "phone": "+91-44-XXXXX",
      "email": "info@college.edu",
      "website": "www.college.edu",
      "location": "Chennai, Tamil Nadu"
    }

Response (200 OK):
  {
    "success": true,
    "message": "College info updated successfully"
  }

Note: You can update any fields. They will be merged with existing info.

Example Python:
  import requests
  
  url = "http://localhost:5000/update-college-info"
  data = {
    "phone": "+91-44-28425555",
    "email": "admissions@college.edu"
  }
  response = requests.post(url, json=data)
  print(response.json())
"""

# HEALTH CHECK ENDPOINT
# =============================================================================
"""
GET /health

Description: Check system health status

Response (200 OK):
  {
    "status": "healthy",
    "openai": "connected",
    "training_data_count": 42
  }

Possible OpenAI statuses:
  - "connected" - API key configured
  - "not configured" - No API key set

Example Python:
  import requests
  
  response = requests.get("http://localhost:5000/health")
  health = response.json()
  print(f"Status: {health['status']}")
  print(f"OpenAI: {health['openai']}")
  print(f"Entries: {health['training_data_count']}")
"""

# ERROR CODES
# =============================================================================
"""
200 OK
  Request successful

400 Bad Request
  - Missing required fields
  - Invalid JSON format
  - Invalid data types

500 Internal Server Error
  - Database/file I/O errors
  - OpenAI API errors
  - Unexpected server errors

502 Bad Gateway
  - Server not responding
  - Connection issues

503 Service Unavailable
  - Server is down
  - Maintenance
"""

# RATE LIMITING
# =============================================================================
"""
Current: No rate limiting implemented

Recommended for production:
  - Limit to 100 requests/minute per IP
  - Implement user authentication
  - Add API key validation
  - Log all requests for analytics
"""

# BEST PRACTICES
# =============================================================================
"""
1. Error Handling
   Always check response status code before processing

2. Timeouts
   Set appropriate timeouts for API calls
   
3. Retry Logic
   Implement exponential backoff for failed requests
   
4. Validation
   Validate all input data before sending

5. Security
   - Don't expose API keys in client-side code
   - Use HTTPS in production
   - Implement proper authentication

6. Performance
   - Batch similar requests when possible
   - Use caching for frequently asked questions
   - Implement request queuing for high traffic
"""

# JAVASCRIPT EXAMPLES
# =============================================================================
"""
// Send chat message
async function sendChat(message) {
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  const data = await response.json();
  return data.reply;
}

// Add training data
async function addData(question, answer, category) {
  const response = await fetch('http://localhost:5000/add-training-data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, answer, category })
  });
  return await response.json();
}

// Get all data
async function getAllData() {
  const response = await fetch('http://localhost:5000/get-training-data');
  return await response.json();
}

// Check health
async function checkHealth() {
  const response = await fetch('http://localhost:5000/health');
  return await response.json();
}
"""

# CURL EXAMPLES
# =============================================================================
"""
# Send chat message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the fee?"}'

# Add training data
curl -X POST http://localhost:5000/add-training-data \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I apply?", "answer": "Apply online at portal.college.edu", "category": "admissions"}'

# Get training data
curl -X GET http://localhost:5000/get-training-data

# Update college info
curl -X POST http://localhost:5000/update-college-info \
  -H "Content-Type: application/json" \
  -d '{"phone": "+91-44-28425555"}'

# Health check
curl -X GET http://localhost:5000/health
"""
