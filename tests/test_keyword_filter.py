import pytest
from dataflex.filters.keyword import KeywordFilter


class TestKeywordFilter:
    def setup_method(self):
        self.clean_sample = {
            "instruction": "Translate the following sentence.",
            "input": "Hello world",
            "output": "Bonjour le monde",
        }

    def _make_sample(self, instruction="", input_text="", output=""):
        return {"instruction": instruction, "input": input_text, "output": output}

    def test_keeps_clean_sample(self):
        f = KeywordFilter(keywords=["spam", "violence"])
        result = f.filter([self.clean_sample])
        assert result == [self.clean_sample]

    def test_removes_sample_with_keyword_in_instruction(self):
        f = KeywordFilter(keywords=["spam"])
        sample = self._make_sample(instruction="This is spam content.")
        result = f.filter([sample])
        assert result == []

    def test_removes_sample_with_keyword_in_output(self):
        f = KeywordFilter(keywords=["violence"])
        sample = self._make_sample(output="This promotes violence.")
        result = f.filter([sample])
        assert result == []

    def test_removes_sample_with_keyword_in_input(self):
        f = KeywordFilter(keywords=["hate"])
        sample = self._make_sample(input_text="I hate everything.")
        result = f.filter([sample])
        assert result == []

    def test_case_insensitive_by_default(self):
        f = KeywordFilter(keywords=["spam"])
        sample = self._make_sample(instruction="This is SPAM content.")
        result = f.filter([sample])
        assert result == []

    def test_case_sensitive_no_match(self):
        f = KeywordFilter(keywords=["spam"], case_sensitive=True)
        sample = self._make_sample(instruction="This is SPAM content.")
        result = f.filter([sample])
        assert result == [sample]

    def test_case_sensitive_match(self):
        f = KeywordFilter(keywords=["SPAM"], case_sensitive=True)
        sample = self._make_sample(instruction="This is SPAM content.")
        result = f.filter([sample])
        assert result == []

    def test_custom_fields_only_checks_specified(self):
        f = KeywordFilter(keywords=["spam"], fields=["instruction"])
        sample = self._make_sample(instruction="clean", output="This is spam.")
        result = f.filter([sample])
        assert result == [sample]

    def test_empty_dataset_returns_empty(self):
        f = KeywordFilter(keywords=["spam"])
        assert f.filter([]) == []

    def test_multiple_keywords_any_triggers_removal(self):
        f = KeywordFilter(keywords=["spam", "hate", "violence"])
        sample = self._make_sample(instruction="This promotes hate speech.")
        result = f.filter([sample])
        assert result == []

    def test_empty_keywords_raises(self):
        with pytest.raises(ValueError):
            KeywordFilter(keywords=[])

    def test_repr(self):
        f = KeywordFilter(keywords=["spam"], fields=["instruction"], case_sensitive=False)
        r = repr(f)
        assert "KeywordFilter" in r
        assert "spam" in r
