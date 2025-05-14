from keybert import KeyBERT


class KeywordExtractor:
    def __init__(self) -> None:
        self.kw_model = KeyBERT()

    def extract(self, text: str):
        keywords_with_scores = self.kw_model.extract_keywords(
            text, keyphrase_ngram_range=(1, 2), top_n=10
        )
        return [keyword for keyword, score in keywords_with_scores]


if __name__ == "__main__":
    ke = KeywordExtractor()
    text_to_analyze = (
        "Natural Language Processing (NLP) is a subfield of artificial intelligence "
        "concerned with the interaction between computers and humans in natural language. "
        "Keyphrase extraction is an important task in NLP."
    )
    print(ke.extract(text_to_analyze))

    text_to_analyze_2 = (
        "Transformers have revolutionized the field of machine learning, "
        "especially in natural language processing tasks such as translation and summarization."
    )
    print(ke.extract(text_to_analyze_2))
