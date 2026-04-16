import pytest
from dataflex.filters.length import LengthFilter


SAMPLE_VALID = {
    "instruction": "Explain the theory of relativity in simple terms.",
    "input": "",
    "output": "The theory of relativity, developed by Einstein, describes how space and time are linked.",
}


class TestLengthFilter:
    def setup_method(self):
        self.filter = LengthFilter()

    def test_keeps_valid_sample(self):
        result = self.filter.filter([SAMPLE_VALID])
        assert len(result) == 1

    def test_removes_short_instruction(self):
        sample = {**SAMPLE_VALID, "instruction": "Hi"}
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_removes_long_instruction(self):
        sample = {**SAMPLE_VALID, "instruction": "x" * 600}
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_removes_empty_output(self):
        sample = {**SAMPLE_VALID, "output": ""}
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_removes_long_output(self):
        sample = {**SAMPLE_VALID, "output": "word " * 500}
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_removes_long_input(self):
        sample = {**SAMPLE_VALID, "input": "a" * 1025}
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_allows_empty_input(self):
        sample = {**SAMPLE_VALID, "input": ""}
        result = self.filter.filter([sample])
        assert len(result) == 1

    def test_custom_thresholds(self):
        f = LengthFilter(min_instruction_len=5, max_instruction_len=20)
        sample = {**SAMPLE_VALID, "instruction": "Short one."}
        result = f.filter([sample])
        assert len(result) == 1

    def test_empty_dataset(self):
        result = self.filter.filter([])
        assert result == []

    def test_mixed_dataset(self):
        short_instr = {**SAMPLE_VALID, "instruction": "Hi"}
        dataset = [SAMPLE_VALID, short_instr, SAMPLE_VALID]
        result = self.filter.filter(dataset)
        assert len(result) == 2

    def test_repr(self):
        r = repr(self.filter)
        assert "LengthFilter" in r
        assert "min_instruction_len" in r

    # Personal note: added this test to verify that an output consisting only
    # of whitespace is treated as effectively empty and filtered out.
    def test_removes_whitespace_only_output(self):
        sample = {**SAMPLE_VALID, "output": "   "}
        result = self.filter.filter([sample])
        assert len(result) == 0

    # Personal note: tab-only and newline-only outputs should also be filtered.
    # Found this edge case while testing with some scraped data.
    def test_removes_tab_only_output(self):
        sample = {**SAMPLE_VALID, "output": "\t\t\t"}
        result = self.filter.filter([sample])
        assert len(result) == 0

    def test_removes_newline_only_output(self):
        sample = {**SAMPLE_VALID, "output": "\n\n"}
        result = self.filter.filter([sample])
        assert len(result) == 0
