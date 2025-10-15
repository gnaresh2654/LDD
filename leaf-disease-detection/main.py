from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import base64
import os
from groq import Groq
import uvicorn
from datetime import datetime

app = FastAPI(title="Leaf Disease Detection API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=GROQ_API_KEY)

class AnalysisResponse(BaseModel):
    disease_name: str
    confidence: str
    description: str
    symptoms: list[str]
    treatment: list[str]
    prevention: list[str]
    severity: str
    timestamp: str

class HealthStatus(BaseModel):
    status: str
    message: str

@app.get("/")
async def root():
    return {
        "message": "Leaf Disease Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/analyze": "Analyze leaf image for diseases"
        }
    }

@app.get("/health", response_model=HealthStatus)
async def health_check():
    return HealthStatus(
        status="healthy",
        message="API is running successfully"
    )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_leaf(file: UploadFile = File(...)):
    """
    Analyze uploaded leaf image for diseases using Groq Vision API
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Read and encode image
        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare prompt for Groq Vision API
        prompt = """You are an expert plant pathologist. Analyze this leaf image and provide a detailed diagnosis.

Please provide your analysis in the following structured format:

DISEASE NAME: [Name of the disease or "Healthy" if no disease detected]
CONFIDENCE: [High/Medium/Low]
DESCRIPTION: [Brief description of the condition]
SYMPTOMS: [List 3-5 visible symptoms, separated by semicolons]
TREATMENT: [List 3-5 treatment recommendations, separated by semicolons]
PREVENTION: [List 3-5 prevention measures, separated by semicolons]
SEVERITY: [Mild/Moderate/Severe/Healthy]

Be specific and practical in your recommendations."""

        # Call Groq Vision API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-90b-vision-preview",
            temperature=0.3,
            max_tokens=1024,
        )
        
        # Parse response
        response_text = chat_completion.choices[0].message.content
        
        # Extract structured information
        analysis = parse_analysis_response(response_text)
        analysis["timestamp"] = datetime.now().isoformat()
        
        return AnalysisResponse(**analysis)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )

def parse_analysis_response(response_text: str) -> dict:
    """Parse the structured response from Groq API"""
    
    lines = response_text.strip().split('\n')
    analysis = {
        "disease_name": "Unknown",
        "confidence": "Medium",
        "description": "",
        "symptoms": [],
        "treatment": [],
        "prevention": [],
        "severity": "Unknown"
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("DISEASE NAME:"):
            analysis["disease_name"] = line.replace("DISEASE NAME:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            analysis["confidence"] = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("DESCRIPTION:"):
            analysis["description"] = line.replace("DESCRIPTION:", "").strip()
        elif line.startswith("SYMPTOMS:"):
            symptoms_text = line.replace("SYMPTOMS:", "").strip()
            analysis["symptoms"] = [s.strip() for s in symptoms_text.split(';') if s.strip()]
        elif line.startswith("TREATMENT:"):
            treatment_text = line.replace("TREATMENT:", "").strip()
            analysis["treatment"] = [t.strip() for t in treatment_text.split(';') if t.strip()]
        elif line.startswith("PREVENTION:"):
            prevention_text = line.replace("PREVENTION:", "").strip()
            analysis["prevention"] = [p.strip() for p in prevention_text.split(';') if p.strip()]
        elif line.startswith("SEVERITY:"):
            analysis["severity"] = line.replace("SEVERITY:", "").strip()
    
    # Fallback parsing if structured format is not followed
    if not analysis["description"] and len(lines) > 0:
        analysis["description"] = response_text[:200] + "..."
    
    if not analysis["symptoms"]:
        analysis["symptoms"] = ["Analysis completed - check description for details"]
    
    if not analysis["treatment"]:
        analysis["treatment"] = ["Consult with agricultural expert for specific treatment"]
    
    if not analysis["prevention"]:
        analysis["prevention"] = ["Maintain proper plant hygiene and monitoring"]
    
    return analysis

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
