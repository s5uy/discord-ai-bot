import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.config.settings import normalize_openai_base_url
from src.utils.text import chunk_discord


class TestOpenAiUrl(unittest.TestCase):
    def test_normalize_adds_v1_for_bare_host(self) -> None:
        self.assertEqual(
            normalize_openai_base_url("https://api.example.com"),
            "https://api.example.com/v1",
        )

    def test_normalize_preserves_existing_v1(self) -> None:
        self.assertEqual(
            normalize_openai_base_url("https://api.example.com/v1"),
            "https://api.example.com/v1",
        )


class TestChunk(unittest.TestCase):
    def test_chunk_splits_long_text(self) -> None:
        s = "a" * 5000
        parts = chunk_discord(s, 2000)
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 2000)


if __name__ == "__main__":
    unittest.main()
