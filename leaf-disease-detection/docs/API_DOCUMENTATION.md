# API Documentation

Complete documentation for the Leaf Disease Detection API.

## Base URL

```
http://localhost:8000  # Development
https://api.yourdomain.com  # Production
```

## Authentication

Currently, the API does not require authentication. For production deployments, consider implementing:
- API Keys
- OAuth 2.0
- JWT tokens

---

## Endpoints

### 1. Root Endpoint

Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Leaf Disease Detection API",
  "version": "1.0.0",
  "description": "AI-powered plant disease detection system",
  "endpoints": {
    "/": "API information",
    "/health": "Health check endpoint",
    "/analyze": "Analyze leaf image for diseases (POST)",
    "/docs": "Interactive API documentation",
    "/redoc": "Alternative API documentation"
  },
  "supported_formats": [".jpg", ".jpeg", ".png", ".webp"],
  "max_file_size_mb": 10.0
}
```

---

### 2. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running successfully",
  "version": "1.0.0",
  "timestamp": "2025-10-15T10:30:00"
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is down

---

### 3. Analyze Leaf Image

Analyze an uploaded leaf image for diseases.

**Endpoint:** `POST /analyze`

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Image file (JPEG, PNG, WEBP) |

**Request Example (cURL):**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/leaf.jpg"
```

**Request Example (Python):**
```python
import requests

url = "http://localhost:8000/analyze"
files = {"file": open("leaf.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()
print(result)
```

**Request Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/analyze', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Success Response (200 OK):**
```json
{
  "disease_name": "Tomato Early Blight",
  "confidence": "High",
  "description": "Early blight is a common fungal disease affecting tomato plants, caused by Alternaria solani. The condition shows characteristic dark concentric ring patterns on leaves, typically starting from the lower leaves and progressing upward.",
  "symptoms": [
    "Dark brown spots with concentric rings (target-like pattern) on older leaves",
    "Yellowing of leaves around the lesions",
    "Premature leaf drop starting from bottom of plant",
    "Stem lesions may appear as dark, sunken areas",
    "Fruit may show dark leathery spots near the stem end"
  ],
  "treatment": [
    "Remove and destroy all infected leaves and plant debris immediately",
    "Apply copper-based fungicide or chlorothalonil according to label instructions",
    "Use organic options like neem oil or Bacillus subtilis for mild infections",
    "Improve air circulation by proper spacing and pruning",
    "Apply mulch to prevent soil splash onto lower leaves"
  ],
  "prevention": [
    "Practice crop rotation, avoid planting tomatoes in same location for 3-4 years",
    "Space plants adequately (24-36 inches) for air circulation",
    "Water at the base of plants early in the day; avoid overhead watering",
    "Apply preventive fungicide sprays in humid conditions",
    "Use disease-resistant varieties when available; remove plant debris at season end"
  ],
  "severity": "Moderate",
  "timestamp": "2025-10-15T10:30:00.123456",
  "model_used": "llama-3.2-90b-vision-preview"
}
```

**Error Responses:**

**400 Bad Request** - Invalid file type or size
```json
{
  "detail": "File must be an image. Allowed types: image/jpeg, image/png, image/webp"
}
```

**413 Payload Too Large** - File size exceeds limit
```json
{
  "detail": "File size exceeds maximum allowed size of 10.0MB"
}
```

**500 Internal Server Error** - Processing error
```json
{
  "detail": "Error analyzing image: <error message>",
  "timestamp": "2025-10-15T10:30:00",
  "path": "/analyze"
}
```

---

## Response Schema

### AnalysisResponse

| Field | Type | Description |
|-------|------|-------------|
| disease_name | string | Name of detected disease or "Healthy Leaf" |
| confidence | string | Detection confidence: High, Medium, or Low |
| description | string | Detailed description of the condition |
| symptoms | array[string] | List of visible symptoms |
| treatment | array[string] | Recommended treatment steps |
| prevention | array[string] | Prevention measures |
| severity | string | Severity level: Healthy, Mild, Moderate, or Severe |
| timestamp | string (ISO 8601) | Analysis timestamp |
| model_used | string | AI model used for analysis |

### HealthStatus

| Field | Type | Description |
|-------|------|-------------|
| status | string | Health status: "healthy" or "unhealthy" |
| message | string | Status message |
| version | string | API version |
| timestamp | string (ISO 8601) | Check timestamp |

---

## File Requirements

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)

### File Size
- Maximum: 10 MB
- Recommended: 1-5 MB for faster processing

### Image Quality Guidelines
- Minimum resolution: 500x500 pixels
- Recommended: 1000x1000 pixels or higher
- Clear focus on the leaf
- Good lighting (natural daylight preferred)
- Minimal background clutter
- Single leaf preferred

---

## Rate Limiting

**Current Status:** No rate limiting implemented

**Recommended for Production:**
- 100 requests per hour per IP
- 1000 requests per day per API key
- Burst limit: 10 requests per minute

**Response Headers (when implemented):**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634567890
```

---

## Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "detail": "Error message describing what went wrong",
  "timestamp": "2025-10-15T10:30:00",
  "path": "/analyze"
}
```

### Common Error Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Invalid file type, corrupt file |
| 413 | Payload Too Large | File exceeds 10MB limit |
| 415 | Unsupported Media Type | Wrong content type |
| 422 | Unprocessable Entity | Invalid request structure |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | API processing error |
| 503 | Service Unavailable | API is down or overloaded |

---

## Code Examples

### Python (requests)

```python
import requests
from pathlib import Path

def analyze_leaf(image_path: str):
    """Analyze a leaf image for diseases"""
    url = "http://localhost:8000/analyze"
    
    with open(image_path, "rb") as f:
        files = {"file": (Path(image_path).name, f, "image/jpeg")}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.json()['detail']}")

# Usage
result = analyze_leaf("path/to/leaf.jpg")
print(f"Disease: {result['disease_name']}")
print(f"Severity: {result['severity']}")
print(f"Confidence: {result['confidence']}")
```

### Python (httpx - async)

```python
import httpx
import asyncio

async def analyze_leaf_async(image_path: str):
    """Async version of leaf analysis"""
    url = "http://localhost:8000/analyze"
    
    async with httpx.AsyncClient() as client:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = await client.post(url, files=files)
        
        return response.json()

# Usage
result = asyncio.run(analyze_leaf_async("leaf.jpg"))
```

### JavaScript (Fetch API)

```javascript
async function analyzeLeaf(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Usage with file input
document.getElementById('fileInput').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  if (file) {
    const result = await analyzeLeaf(file);
    console.log('Disease:', result.disease_name);
    console.log('Severity:', result.severity);
  }
});
```

### JavaScript (Axios)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function analyzeLeaf(imagePath) {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(imagePath));
  
  try {
    const response = await axios.post(
      'http://localhost:8000/analyze',
      formData,
      {
        headers: formData.getHeaders()
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}

// Usage
analyzeLeaf('path/to/leaf.jpg')
  .then(result => {
    console.log('Disease:', result.disease_name);
    console.log('Treatments:', result.treatment);
  });
```

### cURL

```bash
# Basic analysis
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@leaf.jpg"

# Save response to file
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@leaf.jpg" \
  -o result.json

# With timeout
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@leaf.jpg" \
  --max-time 30

# Check health
curl http://localhost:8000/health
```

---

## Interactive Documentation

The API provides interactive documentation using Swagger UI and ReDoc:

### Swagger UI
```
http://localhost:8000/docs
```
- Interactive API testing
- Try out endpoints directly
- View request/response schemas

### ReDoc
```
http://localhost:8000/redoc
```
- Clean, organized documentation
- Easy navigation
- Downloadable OpenAPI spec

---

## Best Practices

### 1. Image Optimization

```python
from PIL import Image

def optimize_image(image_path, max_size=(1024, 1024)):
    """Optimize image before uploading"""
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save to buffer
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)
    
    return buffer
```

### 2. Error Handling

```python
def safe_analyze(image_path):
    """Analyze with proper error handling"""
    try:
        response = requests.post(
            "http://localhost:8000/analyze",
            files={"file": open(image_path, "rb")},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}")
        print(f"Details: {e.response.json()}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None
```

### 3. Batch Processing

```python
import concurrent.futures
from pathlib import Path

def batch_analyze(image_folder, max_workers=3):
    """Analyze multiple images concurrently"""
    image_files = list(Path(image_folder).glob("*.jpg"))
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(analyze_leaf, str(img)): img 
            for img in image_files
        }
        
        for future in concurrent.futures.as_completed(futures):
            img = futures[future]
            try:
                result = future.result()
                results.append({
                    "image": img.name,
                    "result": result
                })
            except Exception as e:
                print(f"Error processing {img.name}: {e}")
    
    return results

# Usage
results = batch_analyze("test_images/", max_workers=3)
```

### 4. Response Validation

```python
from pydantic import BaseModel, ValidationError

class AnalysisResult(BaseModel):
    disease_name: str
    confidence: str
    severity: str
    symptoms: list[str]
    treatment: list[str]
    prevention: list[str]

def validate_response(response_data):
    """Validate API response"""
    try:
        result = AnalysisResult(**response_data)
        return result
    except ValidationError as e:
        print(f"Invalid response: {e}")
        return None
```

---

## Monitoring & Logging

### Health Check Script

```python
import requests
import time
from datetime import datetime

def monitor_api(interval=60):
    """Monitor API health"""
    url = "http://localhost:8000/health"
    
    while True:
        try:
            response = requests.get(url, timeout=5)
            status = "✅ UP" if response.status_code == 200 else "❌ DOWN"
            print(f"[{datetime.now()}] API Status: {status}")
        except Exception as e:
            print(f"[{datetime.now()}] API Status: ❌ DOWN - {e}")
        
        time.sleep(interval)

# Run monitor
monitor_api(interval=300)  # Check every 5 minutes
```

### Request Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def analyze_with_logging(image_path):
    """Analyze with request logging"""
    logging.info(f"Starting analysis for {image_path}")
    
    try:
        start_time = time.time()
        result = analyze_leaf(image_path)
        duration = time.time() - start_time
        
        logging.info(f"Analysis completed in {duration:.2f}s")
        logging.info(f"Detected: {result['disease_name']} ({result['confidence']})")
        
        return result
    
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise
```

---

## Troubleshooting

### Common Issues

**1. Connection Refused**
```
Solution: Ensure the API is running on the correct port
Check: curl http://localhost:8000/health
```

**2. Timeout Errors**
```
Solution: Increase timeout value or optimize image size
Example: requests.post(url, files=files, timeout=60)
```

**3. Invalid File Type**
```
Solution: Convert image to supported format (JPEG, PNG)
Check: file.content_type before upload
```

**4. Large Response Times**
```
Solution: 
- Compress images before upload
- Use smaller image dimensions
- Check API server resources
```

---

## Changelog

### Version 1.0.0 (2025-10-15)
- Initial release
- Basic disease detection endpoint
- Support for JPEG, PNG, WEBP formats
- Health check endpoint
- Comprehensive error handling

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: [Your Repo URL]
- Email: support@yourdomain.com
- Documentation: https://docs.yourdomain.com

---

## Legal

### Terms of Use
- API provided "as-is" without warranties
- Not a substitute for professional agricultural advice
- Usage subject to fair use policies

### Data Privacy
- Images are not stored on the server
- Analysis results are not logged permanently
- No personal data is collected

---

**Last Updated:** October 15, 2025
