from typing import Any

from dataflex.filters.quality import QualityFilter
from dataflex.filters.dedup import DeduplicationFilter
from dataflex.filters.length import LengthFilter


class FilterPipeline:
    """
    A composable pipeline that applies multiple filters sequentially
    to a dataset.
    """

    DEFAULT_FILTERS = [QualityFilter, DeduplicationFilter, LengthFilter]

    def __init__(self, filters: list | None = None):
        """
        Args:
            filters: List of instantiated filter objects. If None, uses
                     the default filter stack with default parameters.
        """
        if filters is None:
            self.filters = [cls() for cls in self.DEFAULT_FILTERS]
        else:
            self.filters = filters

    def run(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Apply all filters in order and return the cleaned dataset.

        Args:
            dataset: Raw list of sample dicts.

        Returns:
            Filtered dataset.
        """
        current = dataset
        for f in self.filters:
            before = len(current)
            current = f.filter(current)
            after = len(current)
            print(f"[{f.__class__.__name__}] {before} -> {after} samples")
        return current

    def add_filter(self, f: Any) -> "FilterPipeline":
        """Append a filter to the pipeline and return self for chaining."""
        self.filters.append(f)
        return self

    def __repr__(self) -> str:
        names = ", ".join(f.__class__.__name__ for f in self.filters)
        return f"FilterPipeline([{names}])"
