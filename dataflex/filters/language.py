from typing import List, Optional


class LanguageFilter:
    """
    Filter samples based on detected or declared language.

    Keeps only samples whose language matches one of the allowed languages.
    Language detection is done via a simple heuristic using the `langdetect`
    library if available, or by checking a declared 'lang' field in the sample.
    """

    def __init__(
        self,
        allowed_languages: List[str],
        field: str = "instruction",
        lang_field: Optional[str] = None,
        min_confidence: float = 0.6,
    ):
        """
        Args:
            allowed_languages: List of BCP-47 language codes to keep (e.g. ['en', 'zh']).
            field: The text field to use for language detection.
            lang_field: If set, read language from this field instead of detecting it.
            min_confidence: Minimum confidence threshold for langdetect (0.0 - 1.0).
                Lowered default to 0.6 since short samples often score below 0.7
                even when correctly detected.
        """
        if not allowed_languages:
            raise ValueError("allowed_languages must not be empty")
        self.allowed_languages = [lang.lower().strip() for lang in allowed_languages]
        self.field = field
        self.lang_field = lang_field
        self.min_confidence = min_confidence
        self._langdetect_available = self._check_langdetect()

    @staticmethod
    def _check_langdetect() -> bool:
        try:
            import langdetect  # noqa: F401
            return True
        except ImportError:
            return False

    def _detect_language(self, text: str) -> Optional[str]:
        if not self._langdetect_available:
            return None
        try:
            from langdetect import detect_langs
            results = detect_langs(text)
            if results and results[0].prob >= self.min_confidence:
                return results[0].lang.lower()
        except Exception:
            pass
        return None

    def _is_allowed(self, sample: dict) -> bool:
        if self.lang_field and self.lang_field in sample:
            lang = str(sample[self.lang_field]).lower().strip()
            return lang in self.allowed_languages

        text = sample.get(self.field, "")
        if not text:
            return False

        detected = self._detect_language(text)
        if detected is None:
            # Cannot determine language; keep sample to avoid data loss
            return True
        return detected in self.allowed_languages

    def filter(self, dataset: List[dict]) -> List[dict]:
        """Return only samples whose language is in allowed_languages."""
        return [sample for sample in dataset if self._is_allowed(sample)]

    def __repr__(self) -> str:
        return (
            f"LanguageFilter(allowed_languages={self.allowed_languages}, "
            f"field='{self.field}', lang_field={self.lang_field!r})"
        )
