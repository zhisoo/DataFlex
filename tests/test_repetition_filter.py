import pytest
from dataflex.filters.repetition import RepetitionFilter


class TestRepetitionFilter:
    def setup_method(self):
        self.filter = RepetitionFilter(
            fields=["instruction", "input", "output"],
            max_word_repetition_ratio=0.3,
            max_ngram_repetition_ratio=0.4,
            ngram_size=3,
        )

    def _make_sample(self, instruction="", input_="", output=""):
        return {"instruction": instruction, "input": input_, "output": output}

    def test_keeps_clean_sample(self):
        sample = self._make_sample(
            instruction="Summarize the following article.",
            output="The article discusses climate change and its effects on polar regions.",
        )
        result = self.filter.filter([sample])
        assert result == [sample]

    def test_removes_repetitive_word_in_instruction(self):
        # 'word' repeated 5 out of 9 tokens → ratio > 0.3
        sample = self._make_sample(
            instruction="word word word word word once twice three four",
        )
        result = self.filter.filter([sample])
        assert result == []

    def test_removes_repetitive_ngram_in_output(self):
        # repeated trigram pattern
        phrase = "the cat sat " * 6
        sample = self._make_sample(output=phrase.strip())
        result = self.filter.filter([sample])
        assert result == []

    def test_keeps_sample_below_thresholds(self):
        sample = self._make_sample(
            instruction="Please translate the sentence.",
            input_="Hello world how are you today.",
            output="Bonjour monde comment allez vous aujourd hui.",
        )
        result = self.filter.filter([sample])
        assert result == [sample]

    def test_empty_fields_are_skipped(self):
        sample = self._make_sample(instruction="Tell me a joke.", input_="", output="")
        result = self.filter.filter([sample])
        assert result == [sample]

    def test_empty_dataset(self):
        assert self.filter.filter([]) == []

    def test_multiple_samples_mixed(self):
        good = self._make_sample(instruction="Describe the water cycle briefly.")
        bad = self._make_sample(
            instruction="go go go go go go go go go go go go"
        )
        result = self.filter.filter([good, bad])
        assert result == [good]

    def test_custom_ngram_size(self):
        f = RepetitionFilter(ngram_size=2, max_ngram_repetition_ratio=0.3)
        repeated = "the cat " * 8
        sample = self._make_sample(output=repeated.strip())
        result = f.filter([sample])
        assert result == []

    def test_word_repetition_ratio_edge_single_word(self):
        # single word → ratio = 1.0, should be filtered
        sample = self._make_sample(instruction="hello")
        result = self.filter.filter([sample])
        assert result == []

    def test_missing_field_does_not_crash(self):
        sample = {"instruction": "What is AI?"}
        result = self.filter.filter([sample])
        assert result == [sample]
