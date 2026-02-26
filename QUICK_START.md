# 🚀 Quick Start Guide - AI College Chatbot

## Step 1: Get OpenAI API Key (1 minute)

1. Go to https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key (it won't show again!)

## Step 2: Setup Backend (5 minutes)

```bash
# Navigate to backend
cd c:\chatbot\backend

# Activate virtual environment
.\venv\Scripts\Activate

# Install packages (if not already done)
pip install -r requirements.txt

# Create .env file with your API key
# Add this line to a new file called .env:
# OPENAI_API_KEY=sk-your_key_here
```

## Step 3: Start Backend

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

## Step 4: Open Frontend

In your browser, navigate to:
```
file:///c:/chatbot/frontend/index.html
```

Or run a server:
```bash
cd c:\chatbot\frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

## Step 5: Test the Chatbot

1. Type: "What is the CSE fee?"
2. Wait for the response from AI
3. Try more questions!

## Step 6: Add Your Training Data

### Option A: Admin Panel (Easiest)
1. Click "➕ Add Training Data" in the admin panel
2. Enter your question and answer
3. Select category
4. Done!

### Option B: Python Script
```bash
# Edit manage_data.py with your data
# Then run:
python manage_data.py
```

### Option C: API Call
```bash
# Using curl:
curl -X POST http://localhost:5000/add-training-data \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the hostel fee?",
    "answer": "Hostel fee is ₹60,000 per year.",
    "category": "hostel"
  }'
```

## Common Questions

### Q: Getting "API key not found" error?
A: Make sure you created the `.env` file with your OpenAI API key

### Q: Port 5000 already in use?
A: Change the port in app.py: `app.run(debug=True, port=5001)`

### Q: Responses are slow?
A: OpenAI API takes 1-3 seconds. This is normal on first load.

### Q: Want to see all training data?
A: Click "📊 View Training Data" → check browser console

### Q: How to update college info?
A: Click "💚 System Health" to check status, then use the API or admin panel

## File Structure

```
chatbot/
├── backend/
│   ├── app.py                 # Main Flask app (with AI integration)
│   ├── manage_data.py         # Data management script
│   ├── training_data.json     # Your college data
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Your API key (create this!)
│   ├── README.md              # Full documentation
│   └── API_DOCS.py            # API reference
│
└── frontend/
    ├── index.html             # Main page
    ├── style.css              # Styling
    └── script.js              # Frontend logic
```

## Sample Training Data to Add

Add these questions to see the AI work:

1. **Q:** "What are the lab timings?"
   **A:** "Labs are open from 9:00 AM to 5:00 PM, Monday to Saturday."
   **Category:** timings

2. **Q:** "Can I change my course?"
   **A:** "Yes, course change is possible within 1 month of admission."
   **Category:** admissions

3. **Q:** "What is the dress code?"
   **A:** "Professional attire is required on campus. No shorts or t-shirts."
   **Category:** general

4. **Q:** "When is the placement season?"
   **A:** "Placement drive starts from 6th semester onwards."
   **Category:** placements

## Customization

### Change College Name
Edit `training_data.json`:
```json
"college_info": {
  "name": "Your College Name",
  "location": "Your City"
}
```

### Add More Categories
Just create new categories in the training data! Examples:
- "sports"
- "library"
- "medical"
- "security"
- "parking"

### Customize AI Behavior
Edit the system prompt in `app.py` (around line 120):
```python
system_prompt = f"""You are a helpful college enquiry chatbot...
```

## Troubleshooting Checklist

- [ ] OpenAI API key is set in .env file
- [ ] Backend is running (`python app.py`)
- [ ] Frontend can reach backend (CORS enabled)
- [ ] Training data is in training_data.json
- [ ] JSON is valid (use JSONLint if unsure)
- [ ] Port 5000 is not blocked by firewall

## Next Steps

1. Add more training data specific to your college
2. Customize the system prompt for your needs
3. Test with real user queries
4. Deploy to production (add authentication, SSL, etc.)
5. Monitor API usage and costs

## Production Deployment

Before going live:

1. **Security:**
   - Add API key authentication
   - Implement HTTPS
   - Add rate limiting
   - Validate all inputs

2. **Performance:**
   - Add response caching
   - Use a database instead of JSON
   - Implement request queuing

3. **Monitoring:**
   - Log all interactions
   - Track API costs
   - Monitor response times
   - Set up error alerts

4. **Backup:**
   - Regular backups of training_data.json
   - Database replication
   - Disaster recovery plan

## Support

- Check README.md for detailed documentation
- Review API_DOCS.py for API reference
- Check browser console for JavaScript errors
- Check Flask console for backend errors

---

**You're all set! Start the backend and open the frontend to begin. 🎉**
