# Deployment Guide - Render

Your Multiplication Table app is ready to deploy on Render (a free cloud hosting platform).

## Steps to Deploy:

### 1. Initialize Git Repository (if not already done)
```powershell
git init
git add .
git commit -m "Initial commit"
```

### 2. Push to GitHub
- Create a GitHub account (if you don't have one)
- Create a new repository named `multiplication-table-app`
- Push your local code to GitHub:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/multiplication-table-app.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Render
- Go to https://render.com
- Sign up with your GitHub account
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Fill in the deployment details:
  - **Name**: `multiplication-table-app` (or any name you prefer)
  - **Environment**: `Python 3`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn app:app`
  - **Instance Type**: `Free` (for students)
- Click "Create Web Service"
- Wait 2-3 minutes for deployment to complete

### 4. Access Your App
Once deployed, Render will provide a public URL (e.g., `https://multiplication-table-app-xxxxx.onrender.com`)
Share this link with students so they can access the app from anywhere!

## Alternative Deployment Options:

### PythonAnywhere (Easiest for beginners)
- Go to https://www.pythonanywhere.com
- Sign up (free account available)
- Upload your files
- Configure web app settings
- Your app will be live at `yourusername.pythonanywhere.com`

### Heroku (Requires credit card)
- Go to https://www.heroku.com
- Sign up and follow their deployment guide
- Use the Procfile we created

## Notes:
- The app will be publicly accessible 24/7
- Students can access it from any device (phone, tablet, computer)
- No installation required - just open the link!
