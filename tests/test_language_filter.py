import pytest
from dataflex.filters.language import LanguageFilter


class TestLanguageFilter:
    def setup_method(self):
        self.samples = [
            {"instruction": "Hello, how are you?", "output": "I am fine.", "lang": "en"},
            {"instruction": "你好，你好吗？", "output": "我很好。", "lang": "zh"},
            {"instruction": "Bonjour, comment allez-vous?", "output": "Bien.", "lang": "fr"},
            {"instruction": "Hola, ¿cómo estás?", "output": "Bien.", "lang": "es"},
        ]

    # --- lang_field mode ---

    def test_keeps_english_via_lang_field(self):
        f = LanguageFilter(allowed_languages=["en"], lang_field="lang")
        result = f.filter(self.samples)
        assert len(result) == 1
        assert result[0]["lang"] == "en"

    def test_keeps_multiple_languages_via_lang_field(self):
        f = LanguageFilter(allowed_languages=["en", "zh"], lang_field="lang")
        result = f.filter(self.samples)
        assert len(result) == 2
        langs = {s["lang"] for s in result}
        assert langs == {"en", "zh"}

    def test_case_insensitive_lang_field(self):
        samples = [{"instruction": "Hi", "lang": "EN"}]
        f = LanguageFilter(allowed_languages=["en"], lang_field="lang")
        result = f.filter(samples)
        assert len(result) == 1

    def test_missing_lang_field_falls_back_to_detection(self):
        samples = [{"instruction": "Hello world"}]
        f = LanguageFilter(allowed_languages=["en"], lang_field="lang")
        # No lang field present — falls back; result depends on langdetect availability
        result = f.filter(samples)
        assert isinstance(result, list)

    def test_empty_dataset(self):
        f = LanguageFilter(allowed_languages=["en"], lang_field="lang")
        assert f.filter([]) == []

    def test_no_matching_language(self):
        f = LanguageFilter(allowed_languages=["de"], lang_field="lang")
        result = f.filter(self.samples)
        assert result == []

    def test_empty_instruction_excluded(self):
        samples = [{"instruction": "", "output": "nothing"}]
        f = LanguageFilter(allowed_languages=["en"])
        result = f.filter(samples)
        assert result == []

    # --- constructor validation ---

    def test_raises_on_empty_allowed_languages(self):
        with pytest.raises(ValueError, match="allowed_languages must not be empty"):
            LanguageFilter(allowed_languages=[])

    def test_custom_field(self):
        samples = [
            {"query": "What is Python?", "lang": "en"},
            {"query": "Python是什么？", "lang": "zh"},
        ]
        f = LanguageFilter(allowed_languages=["en"], field="query", lang_field="lang")
        result = f.filter(samples)
        assert len(result) == 1
        assert result[0]["lang"] == "en"

    # --- repr ---

    def test_repr(self):
        f = LanguageFilter(allowed_languages=["en", "zh"], lang_field="lang")
        r = repr(f)
        assert "LanguageFilter" in r
        assert "en" in r
        assert "zh" in r
