from __future__ import annotations

from typing import List, Optional, Set

DEFAULT_STOPWORDS: Set[str] = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "it", "this", "that",
    "was", "are", "be", "has", "had", "have", "will", "would", "could",
    "should", "may", "might", "do", "does", "did", "not", "no", "so",
    # extra common fillers I kept seeing slip through in my datasets
    "just", "very", "also", "then", "than", "when", "where", "which",
    # added: these kept showing up as noise in my instruction-tuning data
    "please", "sure", "okay", "yes", "yeah", "like", "well",
}


class StopwordsFilter:
    """Filter samples where meaningful word ratio is too low.

    Computes the ratio of non-stopword tokens to total tokens across
    specified fields.  Samples whose ratio falls below *min_ratio* are
    removed, indicating the text is mostly filler words.
    """

    def __init__(
        self,
        min_ratio: float = 0.3,
        fields: Optional[List[str]] = None,
        stopwords: Optional[Set[str]] = None,
    ) -> None:
        if not 0.0 <= min_ratio <= 1.0:
            raise ValueError("min_ratio must be between 0.0 and 1.0")
        self.min_ratio = min_ratio
        self.fields = fields or ["instruction", "input", "output"]
        self.stopwords: Set[str] = (
            {w.lower() for w in stopwords} if stopwords is not None else DEFAULT_STOPWORDS
        )

    def _meaningful_ratio(self, text: str) -> float:
        """Return the fraction of tokens that are not stopwords."""
        tokens = text.lower().split()
        if not tokens:
            return 1.0  # empty text is not penalised here
        meaningful = sum(1 for t in tokens if t.strip(".,!?;:") not in self.stopwords)
        return meaningful / len(tokens)

    def _check_field(self, sample: dict, field: str) -> bool:
        """Return True if the field passes the stopwords ratio check."""
        text = sample.get(field, "")
        if not isinstance(text, str) or not text.strip():
            return True  # skip missing / empty fields
        return self._meaningful_ratio(text) >= self.min_ratio

    def filter(self, samples: List[dict]) -> List[dict]:
        """Return samples that pass the meaningful-word ratio threshold."""
        return [
            s for s in samples
            if all(self._check_field(s, f) for f in self.fields)
        ]

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"StopwordsFilter(min_ratio={self.min_ratio}, "
            f"fields={self.fields})"
        )
