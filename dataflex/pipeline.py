from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Filter(Protocol):
    """Structural protocol that every filter must satisfy."""

    def filter(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ...


class FilterPipeline:
    """
    Sequentially apply a list of filters to a dataset.

    Parameters
    ----------
    filters : list[Filter]
        Ordered list of filter objects to apply.
    verbose : bool
        If True, print the number of samples after each filter step.
    """

    def __init__(self, filters: list[Any] | None = None, verbose: bool = False) -> None:
        self.filters: list[Any] = filters or []
        self.verbose = verbose

    def add_filter(self, f: Any) -> "FilterPipeline":
        """Append a filter and return self for method chaining."""
        self.filters.append(f)
        return self

    def run(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Run all filters in order and return the filtered dataset."""
        data = list(dataset)
        if self.verbose:
            print(f"[Pipeline] Start: {len(data)} samples")
        for f in self.filters:
            before = len(data)
            data = f.filter(data)
            if self.verbose:
                removed = before - len(data)
                print(
                    f"[Pipeline] {f.__class__.__name__}: "
                    f"{len(data)} remaining ({removed} removed)"
                )
        return data

    def __repr__(self) -> str:  # pragma: no cover
        names = ", ".join(f.__class__.__name__ for f in self.filters)
        return f"FilterPipeline(filters=[{names}], verbose={self.verbose})"
