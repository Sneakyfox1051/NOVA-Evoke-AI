# NOVA Assistant - Streamlit Cloud Deployment

A simple and clean AI assistant interface built with Streamlit and OpenAI.

## Features

- 🤖 Clean ChatGPT-like interface
- 🎯 Uses your specific OpenAI Assistant (asst_XTd5ExJ9KUTLyrFkzkzPZa2f)
- 📱 Responsive design
- 🔄 JSON response formatting
- 💬 Real-time chat

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
# Create .env file with your API key
python setup_api_key.py

# Or set environment variable directly
# Windows PowerShell:
$env:OPENAI_API_KEY="your_api_key_here"

# Windows CMD:
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac:
export OPENAI_API_KEY="your_api_key_here"
```

3. Run locally:
```bash
python run_streamlit.py
# or
streamlit run streamlit_app.py
```

## Streamlit Cloud Deployment

This app is configured for easy deployment on Streamlit Cloud.

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_ASSISTANT_ID`: Your assistant ID (asst_XTd5ExJ9KUTLyrFkzkzPZa2f)

### Deployment Steps
1. Push this code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. The app will automatically deploy!

## Configuration

The app uses your specific NOVA assistant with ID `asst_XTd5ExJ9KUTLyrFkzkzPZa2f` and is configured to use GPT-4o-mini by default.