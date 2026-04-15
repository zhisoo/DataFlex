import pytest
from dataflex.filters.stopwords import StopwordsFilter, DEFAULT_STOPWORDS


class TestStopwordsFilter:
    def setup_method(self):
        self.f = StopwordsFilter(min_ratio=0.3)

    def _make_sample(self, instruction="", input_text="", output=""):
        return {"instruction": instruction, "input": input_text, "output": output}

    # --- construction ---

    def test_invalid_ratio_raises(self):
        with pytest.raises(ValueError):
            StopwordsFilter(min_ratio=1.5)

    def test_invalid_negative_ratio_raises(self):
        with pytest.raises(ValueError):
            StopwordsFilter(min_ratio=-0.1)

    # --- keeps valid samples ---

    def test_keeps_meaningful_sample(self):
        sample = self._make_sample(
            instruction="Explain photosynthesis process plants",
            output="Photosynthesis converts sunlight carbon dioxide water glucose oxygen.",
        )
        result = self.f.filter([sample])
        assert result == [sample]

    def test_keeps_sample_with_empty_fields(self):
        sample = self._make_sample(instruction="Describe neural networks architecture")
        result = self.f.filter([sample])
        assert len(result) == 1

    # --- removes low-content samples ---

    def test_removes_stopword_heavy_instruction(self):
        # Almost entirely stopwords
        sample = self._make_sample(
            instruction="the a and or but in on at to for of with by",
            output="This is a valid output with meaningful content here.",
        )
        result = self.f.filter([sample])
        assert result == []

    def test_removes_stopword_heavy_output(self):
        sample = self._make_sample(
            instruction="Explain quantum computing benefits",
            output="the and or but in on at to for of with by from is it",
        )
        result = self.f.filter([sample])
        assert result == []

    # --- custom stopwords ---

    def test_custom_stopwords(self):
        custom = {"foo", "bar", "baz"}
        f = StopwordsFilter(min_ratio=0.5, stopwords=custom)
        # All tokens are custom stopwords → ratio = 0
        sample = self._make_sample(instruction="foo bar baz")
        assert f.filter([sample]) == []

    def test_custom_stopwords_case_insensitive(self):
        custom = {"Foo", "BAR"}
        f = StopwordsFilter(min_ratio=0.5, stopwords=custom)
        sample = self._make_sample(instruction="foo bar")
        assert f.filter([sample]) == []

    # --- custom fields ---

    def test_custom_fields_only_checks_specified(self):
        f = StopwordsFilter(min_ratio=0.3, fields=["output"])
        # instruction is stopword-heavy but not checked
        sample = self._make_sample(
            instruction="the a and or but in",
            output="Neural networks learn complex representations.",
        )
        assert f.filter([sample]) == [sample]

    # --- empty input ---

    def test_empty_list_returns_empty(self):
        assert self.f.filter([]) == []

    # --- multiple samples ---

    def test_filters_mixed_samples(self):
        good = self._make_sample(
            instruction="Describe machine learning algorithms",
            output="Machine learning algorithms optimise predictive models.",
        )
        bad = self._make_sample(
            instruction="the and or but in on",
            output="the and or but in on",
        )
        result = self.f.filter([good, bad])
        assert result == [good]
