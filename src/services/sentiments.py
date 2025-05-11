from transformers import pipeline
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SentimentAnalysisResult:
    label: str
    score: float


class SentimentClassifier:
    def __init__(self) -> None:
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )

    def classify(self, text: str) -> SentimentAnalysisResult:
        output = self.classifier(text)  # type: ignore
        return [SentimentAnalysisResult(**i) for i in output][0]  # type: ignore


if __name__ == "__main__":
    sc = SentimentClassifier()
    print(sc.classify("I am very happy with this product!"))
    print(sc.classify("This is not good at all."))
