import pytest
from dataflex.filters.toxicity import ToxicityFilter, DEFAULT_TOXIC_KEYWORDS


class TestToxicityFilter:
    def setup_method(self):
        self.filter = ToxicityFilter()

    def _make_sample(self, instruction="", input_text="", output=""):
        return {"instruction": instruction, "input": input_text, "output": output}

    def test_keeps_clean_sample(self):
        samples = [self._make_sample("What is Python?", "", "A programming language.")]
        result = self.filter.filter(samples)
        assert len(result) == 1

    def test_removes_toxic_instruction(self):
        samples = [self._make_sample("How to kill a process?", "", "Use kill command.")]
        result = self.filter.filter(samples)
        assert len(result) == 0

    def test_removes_toxic_output(self):
        samples = [self._make_sample("Describe a scenario", "", "It involved abuse and violence.")]
        result = self.filter.filter(samples)
        assert len(result) == 0

    def test_removes_toxic_input(self):
        samples = [self._make_sample("Respond to this", "racist comment here", "I disagree.")]
        result = self.filter.filter(samples)
        assert len(result) == 0

    def test_keeps_multiple_clean_samples(self):
        samples = [
            self._make_sample("Tell me about Python", "", "Python is a language."),
            self._make_sample("What is ML?", "", "Machine learning."),
        ]
        result = self.filter.filter(samples)
        assert len(result) == 2

    def test_filters_mixed_samples(self):
        samples = [
            self._make_sample("Good question", "", "Good answer"),
            self._make_sample("How to abuse the system?", "", "You should not."),
        ]
        result = self.filter.filter(samples)
        assert len(result) == 1
        assert result[0]["instruction"] == "Good question"

    def test_case_insensitive_by_default(self):
        samples = [self._make_sample("How to KILL a process", "", "Use signals.")]
        result = self.filter.filter(samples)
        assert len(result) == 0

    def test_case_sensitive_mode(self):
        f = ToxicityFilter(case_sensitive=True)
        samples = [self._make_sample("How to KILL a process", "", "Use signals.")]
        result = f.filter(samples)
        # "KILL" != "kill" in case-sensitive mode
        assert len(result) == 1

    def test_custom_keywords(self):
        f = ToxicityFilter(keywords=["forbidden", "banned"])
        samples = [
            self._make_sample("This is forbidden content", "", "ok"),
            self._make_sample("Normal question", "", "Normal answer"),
        ]
        result = f.filter(samples)
        assert len(result) == 1

    def test_custom_fields(self):
        f = ToxicityFilter(fields=["output"])
        samples = [self._make_sample("How to kill a process", "", "Safe answer")]
        result = f.filter(samples)
        # toxic keyword only in instruction, which is not checked
        assert len(result) == 1

    def test_empty_dataset(self):
        result = self.filter.filter([])
        assert result == []

    def test_repr(self):
        f = ToxicityFilter()
        r = repr(f)
        assert "ToxicityFilter" in r
        assert "case_sensitive" in r
