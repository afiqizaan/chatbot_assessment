# 🚀 Render Deployment Guide

## Quick Deploy to Render.com

### Step 1: Connect to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your `chatbot_assessment` repository

### Step 2: Configure Settings
- **Name**: `zus-coffee-chatbot` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Plan**: `Free`

### Step 3: Environment Variables
Add this environment variable:
- **Key**: `GEMINI_API_KEY`
- **Value**: Your Google Gemini API key

### Step 4: Deploy
Click "Create Web Service" and wait for deployment (2-5 minutes).

## 🌐 Public URL
Once deployed, you'll get a URL like:
`https://your-app-name.onrender.com`

**This URL is public and shareable!** Anyone can test your chatbot.

## 🔧 Alternative: Blueprint Deployment
If you prefer automatic configuration:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Render will use the `render.yaml` file automatically

## 📱 Testing Your Deployed Chatbot
Visit your URL and try:
- "Hello, how are you?"
- "What is 15 plus 27?"
- "Show me coffee cups"
- "Outlets in KL"

## 🆘 Troubleshooting
- **Build fails**: Check that all dependencies are in `requirements.txt`
- **API key error**: Ensure `GEMINI_API_KEY` is set in environment variables
- **Port issues**: The app automatically uses Render's PORT environment variable

## 📊 Monitoring
- Check deployment logs in Render dashboard
- Monitor health at `/health` endpoint
- View API docs at `/docs` endpoint 