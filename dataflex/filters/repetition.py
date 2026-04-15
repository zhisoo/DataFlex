from __future__ import annotations

from typing import Any


class RepetitionFilter:
    """
    Filter samples that contain excessive repetition of words or n-grams.

    Parameters
    ----------
    fields : list[str]
        Dataset fields to inspect.
    max_word_repetition_ratio : float
        Maximum allowed ratio of the most-frequent word to total words.
    max_ngram_repetition_ratio : float
        Maximum allowed ratio of repeated n-grams to total n-grams.
    ngram_size : int
        Size of n-grams used for repetition detection (default: 3).
    """

    def __init__(
        self,
        fields: list[str] | None = None,
        max_word_repetition_ratio: float = 0.3,
        max_ngram_repetition_ratio: float = 0.4,
        ngram_size: int = 3,
    ) -> None:
        self.fields = fields or ["instruction", "input", "output"]
        self.max_word_repetition_ratio = max_word_repetition_ratio
        self.max_ngram_repetition_ratio = max_ngram_repetition_ratio
        self.ngram_size = ngram_size

    def _word_repetition_ratio(self, text: str) -> float:
        words = text.lower().split()
        if not words:
            return 0.0
        freq: dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        return max(freq.values()) / len(words)

    def _ngram_repetition_ratio(self, text: str) -> float:
        words = text.lower().split()
        n = self.ngram_size
        if len(words) < n:
            return 0.0
        ngrams = [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]
        unique = set(ngrams)
        return 1.0 - len(unique) / len(ngrams)

    def _is_repetitive(self, text: str) -> bool:
        if self._word_repetition_ratio(text) > self.max_word_repetition_ratio:
            return True
        if self._ngram_repetition_ratio(text) > self.max_ngram_repetition_ratio:
            return True
        return False

    def filter(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = []
        for sample in dataset:
            if any(
                self._is_repetitive(str(sample.get(field, "")))
                for field in self.fields
                if sample.get(field)
            ):
                continue
            result.append(sample)
        return result

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"RepetitionFilter(fields={self.fields}, "
            f"max_word_repetition_ratio={self.max_word_repetition_ratio}, "
            f"max_ngram_repetition_ratio={self.max_ngram_repetition_ratio}, "
            f"ngram_size={self.ngram_size})"
        )
