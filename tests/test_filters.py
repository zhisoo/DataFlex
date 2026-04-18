"""Tests for dataflex.filters quality and deduplication filters."""
import pytest

from dataflex.filters.quality import QualityFilter
from dataflex.filters.dedup import DeduplicationFilter


SAMPLE_DATASET = [
    {"instruction": "Translate the following sentence.", "input": "Hello world", "output": "Hola mundo"},
    {"instruction": "hi", "input": "", "output": "ok"},  # too short
    {"instruction": "Summarize this article in detail.", "input": "", "output": "This is a summary."},
    {"instruction": "Translate the following sentence.", "input": "Hello world", "output": "Bonjour monde"},  # duplicate instruction+input
    {"instruction": "", "input": "", "output": ""},  # empty
    {"instruction": "What is the capital of France?", "input": "", "output": "Paris"},
]


class TestQualityFilter:
    def setup_method(self):
        # Using min_output_len=4 to allow short but valid outputs like "Paris"
        self.qf = QualityFilter(min_instruction_len=10, min_output_len=4)

    def test_filters_short_instruction(self):
        result = self.qf.filter(SAMPLE_DATASET)
        instructions = [s["instruction"] for s in result]
        assert "hi" not in instructions

    def test_filters_empty_sample(self):
        result = self.qf.filter(SAMPLE_DATASET)
        for s in result:
            assert len(s["instruction"].strip()) >= 10

    def test_keeps_valid_samples(self):
        result = self.qf.filter(SAMPLE_DATASET)
        assert any(s["instruction"] == "Summarize this article in detail." for s in result)

    def test_keeps_short_but_valid_output(self):
        # "Paris" has 5 chars, should pass with min_output_len=4
        result = self.qf.filter(SAMPLE_DATASET)
        assert any(s["output"] == "Paris" for s in result)

    def test_max_length_filter(self):
        qf = QualityFilter(max_instruction_len=20)
        long_sample = [{"instruction": "A" * 21, "input": "", "output": "short answer"}]
        assert qf.filter(long_sample) == []

    def test_non_string_fields_filtered(self):
        bad = [{"instruction": 123, "input": "", "output": "answer"}]
        assert self.qf.filter(bad) == []

    def test_filters_whitespace_only_instruction(self):
        # NOTE: whitespace-only instructions should be treated as empty and filtered out
        whitespace_sample = [{"instruction": "   ", "input": "", "output": "some output here"}]
        assert self.qf.filter(whitespace_sample) == []


class TestDeduplicationFilter:
    def setup_method(self):
        self.df = DeduplicationFilter()

    def test_removes_duplicates(self):
        result = self.df.filter(SAMPLE_DATASET)
        keys = [(s["instruction"], s.get("input", "")) for s in result]
        assert len(keys) == len(set(keys))

    def test_keeps_first_occurrence(self):
        result = self.df.filter(SAMPLE_DATASET)
        dup_matches = [
            s for s in result
            if s["instruction"] == "Translate the following sentence."
        ]
        assert len(dup_matches) == 1
        assert dup_matches[0]["output"] == "Hola mundo"

    def test_case_insensitive_dedup(self):
        dataset = [
            {"instruction": "Hello World", "input": "", "output": "a"},
            {"instruction": "hello world", "input": "", "output": "b"},
        ]
        result = self.df