from fastapi.testclient import TestClient
from src.main import app, API_KEY
from pathlib import Path
import pytest

# Define the path to the test journals file
TEST_JOURNALS_FILE = Path(__file__).parent / "test_journals.txt"


def load_journal_entries(file_path: Path) -> list[str]:
    """Loads journal entries from a text file."""
    if not file_path.exists():
        return []
    content = file_path.read_text(encoding="utf-8")
    # Split by double newlines and filter out any empty strings
    entries = [entry.strip() for entry in content.split("\n\n") if entry.strip()]
    return entries


def get_test_cases():
    journal_entries = load_journal_entries(TEST_JOURNALS_FILE)
    assert journal_entries, f"No journal entries found in {TEST_JOURNALS_FILE}"
    return journal_entries


@pytest.mark.parametrize("journal_entry", get_test_cases())
def test_analysis(journal_entry, capsys):
    with TestClient(app) as client:
        resp = client.post(
            "/analyze",
            json={"text": journal_entry},
            headers={"Authorization": f"Bearer {API_KEY}"},
        )

        assert resp.status_code == 200
        result = resp.json()

        # Print the input and result for visibility in pytest output
        with capsys.disabled():
            print(f"\nInput: {journal_entry[:70]}...")
            print(f"Analysis result: {result}")

        # Validate emotions field
        assert "emotions" in result, "Response missing emotions field"
        assert isinstance(result["emotions"], list), "Emotions should be a list"
        assert len(result["emotions"]) >= 1, "Should have at least one emotion"
        for emotion in result["emotions"]:
            assert "label" in emotion, "Emotion missing label"
            assert "score" in emotion, "Emotion missing score"
            assert isinstance(emotion["label"], str), "Emotion label should be string"
            assert isinstance(emotion["score"], float), "Emotion score should be float"
            assert 0 <= emotion["score"] <= 1, "Emotion score should be between 0 and 1"

        # Validate sentiment field
        assert "sentiment" in result, "Response missing sentiment field"
        assert isinstance(result["sentiment"], dict), "Sentiment should be a dictionary"
        assert "label" in result["sentiment"], "Sentiment missing label"
        assert "score" in result["sentiment"], "Sentiment missing score"
        assert isinstance(
            result["sentiment"]["label"], str
        ), "Sentiment label should be string"
        assert isinstance(
            result["sentiment"]["score"], float
        ), "Sentiment score should be float"
        assert (
            0 <= result["sentiment"]["score"] <= 1
        ), "Sentiment score should be between 0 and 1"

        # Validate keywords field
        assert "keywords" in result, "Response missing keywords field"
        assert isinstance(result["keywords"], list), "Keywords should be a list"
        for keyword in result["keywords"]:
            assert isinstance(keyword, str), "Keywords should be strings"
