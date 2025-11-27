# Deployment Guide - Render Cloud Platform

This guide walks through deploying the UrbanSound8K ML application to Render.

## Prerequisites

1. GitHub account with your code pushed
2. Render account (free tier available): https://render.com
3. Trained model files (`models/us8k_cnn.h5`, `models/classes.joblib`)

## Deployment Steps

### Option 1: Manual Deployment (Recommended for first time)

#### Step 1: Deploy FastAPI Service

1. **Log in to Render Dashboard**: https://dashboard.render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select branch: `main`

3. **Configure Service**:
   - **Name**: `urbansound-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.prediction:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   Add these in the "Environment" section:
   ```
   MODEL_PATH=/opt/render/project/src/models/us8k_cnn.h5
   CLASSES_PATH=/opt/render/project/src/models/classes.joblib
   PYTHON_VERSION=3.10.0
   ```

5. **Instance Type**: Free (or paid for better performance)

6. **Click "Create Web Service"**
   - Wait for deployment (5-10 minutes)
   - Note your service URL: `https://urbansound-api.onrender.com`

7. **Test API**:
   ```powershell
   curl https://urbansound-api.onrender.com/health
   ```

#### Step 2: Deploy Streamlit UI Service

1. **Create Another Web Service**:
   - Click "New +" → "Web Service"
   - Same repository
   - Select branch: `main`

2. **Configure Service**:
   - **Name**: `urbansound-ui`
   - **Region**: Same as API
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/ui.py --server.port $PORT --server.address 0.0.0.0`

3. **Environment Variables**:
   ```
   api_url=https://urbansound-api.onrender.com
   PYTHON_VERSION=3.10.0
   ```
   (Replace with your actual API URL from Step 1.6)

4. **Click "Create Web Service"**
   - Wait for deployment
   - Note your UI URL: `https://urbansound-ui.onrender.com`

5. **Access Application**:
   - Open: `https://urbansound-ui.onrender.com`
   - Upload audio files and test predictions

### Option 2: Infrastructure as Code (render.yaml)

1. **Update render.yaml** with your API URL in the UI service

2. **In Render Dashboard**:
   - Go to "Blueprints"
   - Click "New Blueprint Instance"
   - Connect repository
   - Select `render.yaml`
   - Click "Apply"

3. Render will automatically create both services

## Post-Deployment

### Verify Deployment

1. **API Health Check**:
   ```powershell
   curl https://your-api-url.onrender.com/health
   ```

2. **UI Access**:
   - Open browser: `https://your-ui-url.onrender.com`
   - Test single prediction
   - Verify retrain button

### Monitoring

**Render Dashboard provides**:
- Real-time logs (Logs tab)
- Metrics: CPU, Memory, Request count
- Deployment history
- Auto-scaling options (paid plans)

**Check Logs**:
1. Go to service in dashboard
2. Click "Logs" tab
3. View real-time application logs

### Update Model

**To deploy a new model version**:

1. Train new model locally:
   ```powershell
   python src/model.py --data data/processed --model_output models/us8k_cnn_v2.h5 --train
   ```

2. Commit and push:
   ```powershell
   git add models/
   git commit -m "Update model to v2"
   git push origin main
   ```

3. Render auto-deploys on push (if enabled)
   - Or manually trigger: Dashboard → Service → "Manual Deploy"

### Scaling

**Free Tier Limitations**:
- Service spins down after 15 min inactivity
- First request after sleep: ~30sec cold start
- 750 hours/month

**Upgrade for**:
- Always-on instances
- Auto-scaling
- Custom domains
- Better performance

## Load Testing Deployed Service

1. **Update Locust target**:
   ```powershell
   locust -f loadtest/locustfile.py --host=https://your-api-url.onrender.com
   ```

2. **Access Locust UI**: http://localhost:8089

3. **Configure Test**:
   - Users: 50 (start small on free tier)
   - Spawn rate: 5/sec
   - Run and observe

4. **Record Results**:
   - Take screenshots of Locust charts
   - Note response times, failure rates
   - Update README with results

## Troubleshooting

### Issue: Build Fails

**Check**:
- `requirements.txt` has all dependencies
- Python version compatibility
- Build logs in Render dashboard

**Fix**:
```powershell
# Test locally first
pip install -r requirements.txt
python src/prediction.py
```

### Issue: Model Not Loading

**Check**:
- Model files exist in repo (`models/us8k_cnn.h5`)
- Environment variables set correctly
- File paths in code match Render's `/opt/render/project/src/...`

**Fix**:
- Ensure model files committed to Git
- Or use persistent disks (paid feature)

### Issue: Cold Starts

**Problem**: Free tier spins down after 15 min

**Solutions**:
- Upgrade to paid plan
- Use external uptime monitor (ping every 14 min)
- Accept cold starts for demo purposes

### Issue: API URL Not Working in UI

**Fix**:
1. Get correct API URL from Render dashboard
2. Update UI service environment variable: `api_url`
3. Redeploy UI service

## Cost Optimization

**Free Tier Usage**:
- Both services: Free (with limitations)
- Storage: 512MB included
- Bandwidth: 100GB/month

**Paid Upgrade ($7-25/month)**:
- Always-on instances
- Faster builds
- More resources

## Security Best Practices

1. **Environment Variables**: Never commit secrets to Git
2. **HTTPS**: Render provides automatic SSL
3. **Authentication**: Add if deploying publicly (not included in base project)
4. **Rate Limiting**: Consider adding for production

## Next Steps

- [ ] Deploy both services
- [ ] Test predictions with sample audio
- [ ] Run load tests and record results
- [ ] Update README with live URLs
- [ ] Create demo video showing deployment
- [ ] (Optional) Add custom domain

## Resources

- Render Docs: https://render.com/docs
- Render Python Guide: https://render.com/docs/deploy-fastapi
- Support: support@render.com
