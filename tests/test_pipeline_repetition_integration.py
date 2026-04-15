"""Integration test: FilterPipeline with RepetitionFilter (and others)."""
import pytest
from dataflex.pipeline import FilterPipeline
from dataflex.filters.repetition import RepetitionFilter
from dataflex.filters.quality import QualityFilter
from dataflex.filters.length import LengthFilter


class TestPipelineRepetitionIntegration:
    def setup_method(self):
        self.pipeline = FilterPipeline(
            filters=[
                QualityFilter(),
                LengthFilter(min_instruction_length=5),
                RepetitionFilter(
                    max_word_repetition_ratio=0.3,
                    max_ngram_repetition_ratio=0.4,
                ),
            ]
        )

    def _make_sample(self, instruction, output="This is a valid output sentence."):
        return {"instruction": instruction, "input": "", "output": output}

    def test_clean_sample_passes_pipeline(self):
        sample = self._make_sample(
            "Explain the concept of machine learning in simple terms."
        )
        result = self.pipeline.run([sample])
        assert result == [sample]

    def test_repetitive_sample_removed_by_pipeline(self):
        bad = self._make_sample("do do do do do do do do do do do")
        good = self._make_sample("What is the capital of France?")
        result = self.pipeline.run([bad, good])
        assert bad not in result
        assert good in result

    def test_empty_pipeline_input(self):
        assert self.pipeline.run([]) == []

    def test_add_filter_chaining(self):
        pipeline = FilterPipeline()
        pipeline.add_filter(RepetitionFilter()).add_filter(QualityFilter())
        assert len(pipeline.filters) == 2

    def test_verbose_pipeline_does_not_raise(self, capsys):
        verbose_pipeline = FilterPipeline(
            filters=[RepetitionFilter()], verbose=True
        )
        sample = self._make_sample("Describe the solar system.")
        verbose_pipeline.run([sample])
        captured = capsys.readouterr()
        assert "Pipeline" in captured.out
