from transformers import pipeline
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmotionAnalysisResult:
    label: str
    score: float


# todo fix index error when exceeding model's token limit
# chunk the given text as per tokens
# aggregate each of them

class EmotionClassifier:
    def __init__(self) -> None:
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=3,
            truncation=True,
        )

    def classify(self, text: str) -> list[EmotionAnalysisResult]:
        output = self.classifier(text)[0]  # type: ignore
        return [EmotionAnalysisResult(**i) for i in output]  # type: ignore


if __name__ == "__main__":
    ec = EmotionClassifier()
    print(ec.classify("dont angry me"))
