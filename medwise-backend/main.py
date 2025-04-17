from fastapi import FastAPI, UploadFile, File, Form, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from pydantic import BaseModel, Field
import secrets
import os
from typing import Annotated, Optional
from fastapi import Body

# Import your existing components
from chat import chat_with_bot
from xray_model import predict_xray
from multimodal import predict_multimodal
from anonymizer import anonymize_text
from dotenv import load_dotenv
load_dotenv()
# Initialize FastAPI app
app = FastAPI()

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Basic authentication setup
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv("API_USERNAME", ""))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("API_PASSWORD", ""))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Pydantic models for request validation
class SymptomRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=1000)

class AnonymizeRequest(BaseModel):
    text: str

# Routes
@app.get("/")
async def home():
    return {"message": "Welcome to Medwise AI API"}

@app.post("/chat")
@limiter.limit("5/minute")
async def chat(
    request: Request, 
    symptom: SymptomRequest,
    username: str = Depends(get_current_username)
):
    return {
        "response": chat_with_bot(symptom.text),
        "user": username
    }

@app.post("/predict-xray")
async def xray(
    username: str = Depends(get_current_username),
    file: UploadFile = File(...)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        prediction = await predict_xray(contents)
        return {
            "prediction": prediction,
            "user": username
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-multimodal")
async def multimodal(
    username: str = Depends(get_current_username),
    symptom_text: str = Form(...),
    file: UploadFile = File(...)
):
    result = await predict_multimodal(symptom_text, file)
    return {
        **result,
        "user": username
    }

@app.post("/anonymize")
async def anonymize(
    request: AnonymizeRequest,
    username: str = Depends(get_current_username)
):
    return {
        "anonymized": anonymize_text(request.text),
        "user": username
    }