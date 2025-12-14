# Render Deployment Guide

## Quick Deploy to Render

### 1. Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `lGikundiro/Guided-Revision-Conversational-Model`

### 2. Configure Service Settings

**Basic Settings:**
- **Name**: `audio-classification-api`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```
  uvicorn src.prediction:app --host 0.0.0.0 --port $PORT
  ```

**Environment Variables:**
- `PYTHON_VERSION`: `3.10.0`
- `MODEL_PATH`: `models/us8k_cnn.h5`
- `CLASSES_PATH`: `models/classes.joblib`

### 3. Deploy

Click **"Create Web Service"** and wait for deployment (3-5 minutes).

### 4. Test Your API

Once deployed, your API will be at: `https://audio-classification-api.onrender.com`

**Test endpoints:**
```bash
# Health check
curl https://audio-classification-api.onrender.com/health

# API info
curl https://audio-classification-api.onrender.com/
```

## Common Issues & Fixes

### Issue: "Not Found" Error
**Solution**: The root endpoint `/` is now added. Redeploy if you see this error.

### Issue: Model files too large for GitHub
**Solution**: We're using a demo model (~500KB). For production, use Git LFS or external storage.

### Issue: Build fails
**Check**: 
- requirements.txt is in root directory
- All dependencies are correctly listed
- Python version is 3.10+

### Issue: Timeout on startup
**Solution**: Render free tier can be slow. Wait 2-3 minutes for first request.

## For Streamlit UI

Deploy separately as a second service:

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
streamlit run src/ui.py --server.port $PORT --server.address 0.0.0.0
```

## URLs After Deployment

- **API**: `https://audio-classification-api.onrender.com`
- **UI**: `https://audio-classification-ui.onrender.com` (if deployed separately)
- **API Docs**: `https://audio-classification-api.onrender.com/docs` (FastAPI auto-generated)
