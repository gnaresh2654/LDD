# Deployment Guide

Complete guide for deploying the Leaf Disease Detection System to production.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Checklist](#production-checklist)

---

## 🏠 Local Development

### Prerequisites
- Python 3.11+
- Groq API Key
- Git

### Setup Steps

```bash
# Clone repository
git clone <your-repo-url>
cd leaf-disease-detection

# Run setup script
chmod +x setup.sh
./setup.sh

# Or on Windows
setup.bat

# Edit .env file
nano .env  # Add your GROQ_API_KEY

# Start backend
./start_backend.sh  # or start_backend.bat on Windows

# Start frontend (new terminal)
./start_frontend.sh  # or start_frontend.bat on Windows
```

---

## 🐳 Docker Deployment

### Single Container

```bash
# Build backend
docker build --target backend -t leaf-detection-api .

# Run backend
docker run -d \
  --name leaf-api \
  -p 8000:8000 \
  -e GROQ_API_KEY=your_key_here \
  leaf-detection-api

# Build frontend
docker build --target frontend -t leaf-detection-frontend .

# Run frontend
docker run -d \
  --name leaf-frontend \
  -p 8501:8501 \
  -e API_BASE_URL=http://localhost:8000 \
  leaf-detection-frontend
```

### Docker Compose (Recommended)

```bash
# Create .env file with GROQ_API_KEY
echo "GROQ_API_KEY=your_key_here" > .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## ☁️ Cloud Deployment

### Option 1: Heroku

#### Backend Deployment

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create leaf-detection-api

# Set environment variables
heroku config:set GROQ_API_KEY=your_key_here

# Create Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Deploy
git push heroku main

# Open app
heroku open
```

#### Frontend Deployment

```bash
# Create frontend app
heroku create leaf-detection-frontend

# Set backend URL
heroku config:set API_BASE_URL=https://leaf-detection-api.herokuapp.com

# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
git push heroku main
```

### Option 2: AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx -y

# 4. Clone repository
git clone <your-repo-url>
cd leaf-disease-detection

# 5. Setup application
./setup.sh

# 6. Configure systemd service for backend
sudo nano /etc/systemd/system/leaf-api.service
```

**Backend Service File:**
```ini
[Unit]
Description=Leaf Disease Detection API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/leaf-disease-detection
Environment="PATH=/home/ubuntu/leaf-disease-detection/venv/bin"
Environment="GROQ_API_KEY=your_key_here"
ExecStart=/home/ubuntu/leaf-disease-detection/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable leaf-api
sudo systemctl start leaf-api
sudo systemctl status leaf-api

# Configure frontend service
sudo nano /etc/systemd/system/leaf-frontend.service
```

**Frontend Service File:**
```ini
[Unit]
Description=Leaf Disease Detection Frontend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/leaf-disease-detection
Environment="PATH=/home/ubuntu/leaf-disease-detection/venv/bin"
ExecStart=/home/ubuntu/leaf-disease-detection/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start frontend
sudo systemctl enable leaf-frontend
sudo systemctl start leaf-frontend

# Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/leaf-detection
```

**Nginx Configuration:**
```nginx
# Backend
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Frontend
server {
    listen 80;
    server_name app.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/leaf-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.yourdomain.com -d app.yourdomain.com
```

### Option 3: Streamlit Cloud (Frontend Only)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Add secrets in dashboard:
   ```toml
   API_BASE_URL = "https://your-backend-url.com"
   ```
7. Click "Deploy"

### Option 4: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set GROQ_API_KEY=your_key_here

# Deploy
railway up
```

### Option 5: Google Cloud Run

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Build and push backend
gcloud builds submit --tag gcr.io/PROJECT_ID/leaf-api

# Deploy backend
gcloud run deploy leaf-api \
  --image gcr.io/PROJECT_ID/leaf-api \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key_here \
  --allow-unauthenticated

# Build and push frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/leaf-frontend

# Deploy frontend
gcloud run deploy leaf-frontend \
  --image gcr.io/PROJECT_ID/leaf-frontend \
  --platform managed \
  --region us-central1 \
  --set-env-vars API_BASE_URL=https://leaf-api-xxx.run.app \
  --allow-unauthenticated
```

---

## ✅ Production Checklist

### Security

- [ ] API key stored in environment variables (not in code)
- [ ] HTTPS/SSL enabled
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation in place
- [ ] File upload size limits enforced
- [ ] Error messages don't expose sensitive info

### Performance

- [ ] Image compression before upload
- [ ] Caching strategy implemented
- [ ] CDN for static assets (if applicable)
- [ ] Database connection pooling (if using DB)
- [ ] Async operations where possible

### Monitoring

- [ ] Logging configured
- [ ] Error tracking (Sentry, etc.)
- [ ] Uptime monitoring
- [ ] Performance monitoring
- [ ] API usage tracking

### Backup & Recovery

- [ ] Database backups (if applicable)
- [ ] Configuration backups
- [ ] Disaster recovery plan
- [ ] Version control for all code

### Documentation

- [ ] API documentation accessible
- [ ] User guide available
- [ ] Deployment procedures documented
- [ ] Troubleshooting guide prepared

### Testing

- [ ] Unit tests written
- [ ] Integration tests passed
- [ ] Load testing performed
- [ ] Security scanning completed

---

## 🔧 Environment Variables for Production

### Backend
```bash
GROQ_API_KEY=your_production_key
HOST=0.0.0.0
PORT=8000
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
MAX_FILE_SIZE=10485760  # 10MB
```

### Frontend
```bash
API_BASE_URL=https://api.yourdomain.com
```

---

## 📊 Monitoring Setup

### Basic Health Check Script

```bash
#!/bin/bash
# health_check.sh

API_URL="https://api.yourdomain.com/health"

response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)

if [ $response -eq 200 ]; then
    echo "✅ API is healthy"
    exit 0
else
    echo "❌ API is down (HTTP $response)"
    # Send alert (email, Slack, etc.)
    exit 1
fi
```

Add to crontab:
```bash
*/5 * * * * /path/to/health_check.sh
```

---

## 🚨 Troubleshooting Production Issues

### Backend Not Starting
```bash
# Check logs
journalctl -u leaf-api -n 50

# Check if port is in use
sudo lsof -i :8000

# Verify environment variables
sudo systemctl show leaf-api | grep Environment
```

### Frontend Connection Issues
```bash
# Test backend connectivity
curl https://api.yourdomain.com/health

# Check frontend logs
journalctl -u leaf-frontend -n 50

# Verify secrets
cat .streamlit/secrets.toml
```

### High Memory Usage
```bash
# Monitor resources
htop

# Restart services
sudo systemctl restart leaf-api
sudo systemctl restart leaf-frontend
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Deploy multiple backend instances behind load balancer
- Use managed services (AWS ECS, Google Cloud Run)
- Implement request queuing

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize image processing
- Use faster storage (SSD)

### Database (If Added)
- Use connection pooling
- Implement caching layer (Redis)
- Regular optimization

---

## 💰 Cost Optimization

1. **Groq API**: Monitor usage, implement caching
2. **Hosting**: Use spot instances, serverless options
3. **Storage**: Compress images, clean up old data
4. **Bandwidth**: Use CDN, enable compression

---

**Need Help?** Check our [README.md](README.md) or create an issue on GitHub.
