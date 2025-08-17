# Deployment Guide

This guide covers various deployment options for the PDF Knowledge Graph Generator application.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Docker (for containerized deployment)
- Access to a cloud platform (for cloud deployment)

## 🏠 Local Development

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/smritirangarajan/pdf-knowledge-graph.git
cd pdf-knowledge-graph

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 2. Run Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### 1. Build and Run with Docker Compose

```bash
# Build and start the application
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 2. Manual Docker Build

```bash
# Build the image
docker build -t pdf-knowledge-graph .

# Run the container
docker run -p 8501:8501 pdf-knowledge-graph
```

### 3. Docker Compose with Custom Configuration

Create a `docker-compose.override.yml` file for custom settings:

```yaml
version: '3.8'
services:
  pdf-knowledge-graph:
    environment:
      - STREAMLIT_SERVER_PORT=8502
      - LOG_LEVEL=DEBUG
    volumes:
      - ./custom_config:/app/config
      - ./data:/app/data
```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the path to `app.py`
   - Click "Deploy"

3. **Configuration**
   - Set environment variables in the Streamlit Cloud dashboard
   - Configure secrets if needed
   - Set resource limits

### Heroku

1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Open App**
   ```bash
   heroku open
   ```

### Google Cloud Run

1. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   ```

2. **Build and Deploy**
   ```bash
   # Build the container
   gcloud builds submit --tag gcr.io/PROJECT_ID/pdf-knowledge-graph
   
   # Deploy to Cloud Run
   gcloud run deploy pdf-knowledge-graph \
     --image gcr.io/PROJECT_ID/pdf-knowledge-graph \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### AWS ECS

1. **Create ECS Cluster**
   ```bash
   aws ecs create-cluster --cluster-name pdf-knowledge-graph
   ```

2. **Create Task Definition**
   ```json
   {
     "family": "pdf-knowledge-graph",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "pdf-knowledge-graph",
         "image": "your-ecr-repo/pdf-knowledge-graph:latest",
         "portMappings": [
           {
             "containerPort": 8501,
             "protocol": "tcp"
           }
         ]
       }
     ]
   }
   ```

3. **Deploy Service**
   ```bash
   aws ecs create-service \
     --cluster pdf-knowledge-graph \
     --service-name pdf-knowledge-graph-service \
     --task-definition pdf-knowledge-graph:1 \
     --desired-count 1
   ```

## Environment Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Application Configuration
LOG_LEVEL=INFO
DEBUG=false
MAX_UPLOAD_SIZE=200

# Security
ENABLE_AUTHENTICATION=false
RATE_LIMIT=100
SESSION_TIMEOUT=3600
```

### Configuration Files

The application uses configuration files in the `config/` directory:

- `config/settings.py` - Main configuration
- `.streamlit/config.toml` - Streamlit-specific settings

## Monitoring and Logging

### Health Checks

The application includes health check endpoints:

- **Health Check**: `/_stcore/health`
- **Metrics**: Available through Streamlit's built-in monitoring

### Logging

Configure logging in `config/settings.py`:

```python
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/app.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}
```

### Performance Monitoring

- Use Streamlit's built-in performance monitoring
- Monitor memory usage and response times
- Set up alerts for high resource usage

## 🔒 Security Considerations

### Production Security

1. **HTTPS**: Always use HTTPS in production
2. **Authentication**: Consider implementing user authentication
3. **Rate Limiting**: Enable rate limiting to prevent abuse
4. **Input Validation**: Validate all user inputs
5. **File Upload Security**: Limit file types and sizes

### Security Headers

Add security headers in your reverse proxy or load balancer:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

## Scaling

### Horizontal Scaling

1. **Load Balancer**: Use a load balancer to distribute traffic
2. **Multiple Instances**: Run multiple instances of the application
3. **Session Management**: Use external session storage (Redis)

### Vertical Scaling

1. **Resource Limits**: Adjust CPU and memory limits
2. **Caching**: Implement Redis caching for better performance
3. **CDN**: Use CDN for static assets

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8501
   lsof -i :8501
   
   # Kill the process
   kill -9 PID
   ```

2. **Memory Issues**
   - Increase container memory limits
   - Optimize PDF processing
   - Implement streaming for large files

3. **Dependencies Issues**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   
   # Clear pip cache
   pip cache purge
   ```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
streamlit run app.py
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [spaCy Documentation](https://spacy.io/usage)

## 🤝 Support

For deployment issues:

1. Check the [GitHub Issues](https://github.com/smritirangarajan/pdf-knowledge-graph/issues)
2. Review the logs for error messages
3. Verify environment configuration
4. Test locally before deploying

---

**Happy Deploying!**
