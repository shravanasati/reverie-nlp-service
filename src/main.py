from fastapi import FastAPI
from pydantic import BaseModel

from src.services.emotions import (
    EmotionClassifier,
    EmotionAnalysisResult,
)
from src.services.sentiments import (
    SentimentClassifier,
    SentimentAnalysisResult,
)
from src.services.keywords import KeywordExtractor

app = FastAPI()

# Instantiate NLP services
emotion_classifier = EmotionClassifier()
sentiment_classifier = SentimentClassifier()
keyword_extractor = KeywordExtractor()


# Pydantic models for request and response
class TextIn(BaseModel):
    text: str


class AnalysisOut(BaseModel):
    emotions: list[EmotionAnalysisResult]
    sentiment: list[SentimentAnalysisResult]
    keywords: list[str]


@app.post("/analyze", response_model=AnalysisOut)
async def analyze_text(request: TextIn):
    text_to_analyze = request.text

    emotions = emotion_classifier.classify(text_to_analyze)
    sentiments = sentiment_classifier.classify(text_to_analyze)
    keywords = keyword_extractor.extract(text_to_analyze)

    return AnalysisOut(emotions=emotions, sentiment=sentiments, keywords=keywords)


@app.get("/")
def root():
    return {"message": "Service healthy and running successfully 🚀"}
