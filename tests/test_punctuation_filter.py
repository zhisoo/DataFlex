import pytest
from dataflex.filters.punctuation import PunctuationFilter


class TestPunctuationFilter:
    def setup_method(self):
        self.filter = PunctuationFilter(min_ratio=0.0, max_ratio=0.3)

    def _make_sample(self, instruction="", input="", output=""):
        return {"instruction": instruction, "input": input, "output": output}

    def test_keeps_clean_sample(self):
        sample = self._make_sample(
            instruction="Tell me about the weather",
            output="The weather today is sunny and warm.",
        )
        result = self.filter.filter([sample])
        assert len(result) == 1

    def test_removes_high_punctuation_instruction(self):
        # "!!!???..." — very high punctuation ratio
        sample = self._make_sample(
            instruction="!!!???...!!!",
            output="Some normal output here.",
        )
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_removes_high_punctuation_output(self):
        sample = self._make_sample(
            instruction="Normal instruction",
            output="!!!@@@###$$$%%%^^^&&&",
        )
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_keeps_empty_field(self):
        sample = self._make_sample(
            instruction="What is the capital of France?",
            input="",
            output="Paris.",
        )
        result = self.filter.filter([sample])
        assert len(result) == 1

    def test_keeps_multiple_valid_samples(self):
        samples = [
            self._make_sample(instruction="Hello world", output="Hi there."),
            self._make_sample(instruction="Explain Python", output="Python is a language."),
        ]
        result = self.filter.filter(samples)
        assert len(result) == 2

    def test_mixed_samples(self):
        samples = [
            self._make_sample(instruction="Normal text here", output="Normal output."),
            self._make_sample(instruction="!!!???!!!", output="Normal output."),
        ]
        result = self.filter.filter(samples)
        assert len(result) == 1
        assert result[0]["instruction"] == "Normal text here"

    def test_custom_fields(self):
        f = PunctuationFilter(max_ratio=0.3, fields=["instruction"])
        sample = self._make_sample(
            instruction="Normal instruction",
            output="!!!???!!!",  # high punctuation but not checked
        )
        result = f.filter([sample])
        assert len(result) == 1

    def test_invalid_min_ratio_raises(self):
        with pytest.raises(ValueError):
            PunctuationFilter(min_ratio=-0.1)

    def test_invalid_max_ratio_raises(self):
        with pytest.raises(ValueError):
            PunctuationFilter(max_ratio=1.5)

    def test_min_greater_than_max_raises(self):
        with pytest.raises(ValueError):
            PunctuationFilter(min_ratio=0.5, max_ratio=0.2)

    def test_repr(self):
        f = PunctuationFilter(min_ratio=0.0, max_ratio=0.25)
        r = repr(f)
        assert "PunctuationFilter" in r
        assert "0.25" in r
