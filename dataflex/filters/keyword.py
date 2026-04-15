from typing import List, Optional, Set


class KeywordFilter:
    """
    Filter that removes samples containing specified keywords or phrases.

    Checks instruction, input, and output fields for forbidden keywords.
    """

    def __init__(
        self,
        keywords: List[str],
        fields: Optional[List[str]] = None,
        case_sensitive: bool = False,
    ):
        """
        Args:
            keywords: List of keywords/phrases to filter out.
            fields: List of sample fields to check. Defaults to
                    ['instruction', 'input', 'output'].
            case_sensitive: Whether matching should be case-sensitive.
        """
        if not keywords:
            raise ValueError("keywords list must not be empty")

        self.case_sensitive = case_sensitive
        self.fields = fields or ["instruction", "input", "output"]

        if case_sensitive:
            self._keywords: Set[str] = set(keywords)
        else:
            self._keywords = set(kw.lower() for kw in keywords)

    def _contains_keyword(self, text: str) -> bool:
        """Return True if text contains any of the forbidden keywords."""
        if not text:
            return False
        haystack = text if self.case_sensitive else text.lower()
        return any(kw in haystack for kw in self._keywords)

    def filter(self, dataset: List[dict]) -> List[dict]:
        """
        Remove samples that contain any forbidden keyword in the checked fields.

        Args:
            dataset: List of sample dicts.

        Returns:
            Filtered list with matching samples removed.
        """
        result = []
        for sample in dataset:
            flagged = False
            for field in self.fields:
                value = sample.get(field, "")
                if isinstance(value, str) and self._contains_keyword(value):
                    flagged = True
                    break
            if not flagged:
                result.append(sample)
        return result

    def __repr__(self) -> str:
        return (
            f"KeywordFilter(keywords={sorted(self._keywords)!r}, "
            f"fields={self.fields!r}, "
            f"case_sensitive={self.case_sensitive})"
        )
