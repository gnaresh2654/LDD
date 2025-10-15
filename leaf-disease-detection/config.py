"""
Configuration settings for Leaf Disease Detection System
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_TITLE: str = "Leaf Disease Detection API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered plant disease detection system"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Groq API Configuration
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.2-90b-vision-preview"
    GROQ_TEMPERATURE: float = 0.3
    GROQ_MAX_TOKENS: int = 1024
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp"]
    ALLOWED_MIME_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # Analysis Configuration
    CONFIDENCE_LEVELS: List[str] = ["High", "Medium", "Low"]
    SEVERITY_LEVELS: List[str] = ["Healthy", "Mild", "Moderate", "Severe"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Validation
if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY must be set in environment variables or .env file")

# Analysis prompt template
ANALYSIS_PROMPT = """You are an expert plant pathologist with years of experience in diagnosing plant diseases. Analyze this leaf image carefully and provide a detailed, accurate diagnosis.

Please provide your analysis in the following structured format:

DISEASE NAME: [Specific name of the disease, or "Healthy Leaf" if no disease is detected]
CONFIDENCE: [High/Medium/Low based on image quality and visible symptoms]
DESCRIPTION: [2-3 sentences describing the condition, what you observe, and why you reached this conclusion]
SYMPTOMS: [List 3-5 specific visible symptoms, separated by semicolons. Be precise and descriptive]
TREATMENT: [List 3-5 practical, actionable treatment steps, separated by semicolons. Include both organic and chemical options where applicable]
PREVENTION: [List 3-5 prevention measures to avoid future infections, separated by semicolons. Include cultural practices and monitoring recommendations]
SEVERITY: [Healthy/Mild/Moderate/Severe based on the extent of infection and potential impact]

Important guidelines:
- Be specific about the plant species if identifiable
- Mention the specific pathogen (fungus, bacteria, virus, pest) if known
- Consider environmental factors that may contribute to the condition
- Provide practical recommendations suitable for both home gardeners and commercial growers
- If the image quality is poor or disease is unclear, indicate this in your confidence level and description
"""
