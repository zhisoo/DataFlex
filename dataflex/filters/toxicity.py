from typing import List, Optional


DEFAULT_TOXIC_KEYWORDS: List[str] = [
    "hate", "kill", "murder", "abuse", "violence",
    "racist", "sexist", "offensive", "slur", "harassment"
]


class ToxicityFilter:
    """
    Filters out samples containing toxic or harmful content
    based on a configurable keyword list.
    """

    def __init__(
        self,
        fields: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        case_sensitive: bool = False,
    ):
        self.fields = fields or ["instruction", "input", "output"]
        self.keywords = keywords if keywords is not None else DEFAULT_TOXIC_KEYWORDS
        self.case_sensitive = case_sensitive

        if not self.case_sensitive:
            self._keywords_normalized = [kw.lower() for kw in self.keywords]
        else:
            self._keywords_normalized = list(self.keywords)

    def _contains_toxic(self, text: str) -> bool:
        if not text:
            return False
        compare = text if self.case_sensitive else text.lower()
        return any(kw in compare for kw in self._keywords_normalized)

    def filter(self, dataset: List[dict]) -> List[dict]:
        """
        Returns samples that do not contain toxic keywords in any checked field.
        """
        result = []
        for sample in dataset:
            toxic = False
            for field in self.fields:
                value = sample.get(field, "")
                if isinstance(value, str) and self._contains_toxic(value):
                    toxic = True
                    break
            if not toxic:
                result.append(sample)
        return result

    def __repr__(self) -> str:
        return (
            f"ToxicityFilter(fields={self.fields}, "
            f"keywords_count={len(self.keywords)}, "
            f"case_sensitive={self.case_sensitive})"
        )
