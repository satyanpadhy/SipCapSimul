# 🚀 Quick Deploy Guide - 5 Minutes to Live App

## Step 1: Push to GitHub
```bash
# If you haven't already, create a GitHub repository
git init
git add .
git commit -m "Initial commit: SIP PCAP Comparison Tool"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - **Repository**: `YOUR_USERNAME/YOUR_REPO_NAME`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Click "Deploy!"

## Step 3: Share Your App
- Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`
- Share this URL with your team
- Perfect for SIP analysis and troubleshooting

## Alternative: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Connect GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects and deploys!

## Alternative: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Set build command: `pip install -r requirements_streamlit.txt`
6. Set start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
7. Deploy!

---
**Time to deploy: ~5 minutes**
**Cost: FREE**
**Result: Live, shareable SIP PCAP comparison tool** 