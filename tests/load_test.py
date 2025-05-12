import asyncio
from pathlib import Path
import httpx

TEST_JOURNALS_FILE = Path(__file__).parent / "test_journals.txt"


def load_journal_entries(file_path: Path) -> list[str]:
    """Loads journal entries from a text file."""
    if not file_path.exists():
        return []
    content = file_path.read_text(encoding="utf-8")
    # Split by double newlines and filter out any empty strings
    entries = [entry.strip() for entry in content.split("\n\n") if entry.strip()]
    return entries


async def perform_load_test():
    entries = load_journal_entries(TEST_JOURNALS_FILE)
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=6)) as client:
        for ent in entries:
            resp = await client.post(
                "http://localhost:5000/analyze",
                json={"text": ent},
                headers={"Authorization": "Bearer hellodarknesmyoldfriend"},
            )
            print(resp.json())


if __name__ == "__main__":
    asyncio.run(perform_load_test())
