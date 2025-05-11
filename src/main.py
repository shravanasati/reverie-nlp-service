from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from src.services.emotions import (
    EmotionClassifier,
    EmotionAnalysisResult,
)
from src.services.sentiments import (
    SentimentClassifier,
    SentimentAnalysisResult,
)
from src.services.keywords import KeywordExtractor

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY environment variable not set.")

security = HTTPBearer()


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


emotion_classifier = EmotionClassifier()
sentiment_classifier = SentimentClassifier()
keyword_extractor = KeywordExtractor()


class TextIn(BaseModel):
    text: str


class AnalysisOut(BaseModel):
    emotions: list[EmotionAnalysisResult]
    sentiment: SentimentAnalysisResult
    keywords: list[str]


@app.post(
    "/analyze", response_model=AnalysisOut, dependencies=[Depends(verify_api_key)]
)
async def analyze_text(request: TextIn):
    text_to_analyze = request.text

    emotions = emotion_classifier.classify(text_to_analyze)
    sentiments = sentiment_classifier.classify(text_to_analyze)
    keywords = keyword_extractor.extract(text_to_analyze)

    return AnalysisOut(emotions=emotions, sentiment=sentiments, keywords=keywords)


@app.get("/")
def root():
    return {"message": "Service healthy and running successfully 🚀"}
