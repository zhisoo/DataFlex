from dataflex.filters.quality import QualityFilter
from dataflex.filters.dedup import DeduplicationFilter
from dataflex.filters.length import LengthFilter
from dataflex.filters.language import LanguageFilter
from dataflex.filters.toxicity import ToxicityFilter
from dataflex.filters.keyword import KeywordFilter
from dataflex.filters.punctuation import PunctuationFilter
from dataflex.filters.repetition import RepetitionFilter
from dataflex.filters.stopwords import StopwordsFilter

# Filters I commonly use: QualityFilter, DeduplicationFilter, LengthFilter
# TODO: look into adding a custom domain-specific filter later

__all__ = [
    "QualityFilter",
    "DeduplicationFilter",
    "LengthFilter",
    "LanguageFilter",
    "ToxicityFilter",
    "KeywordFilter",
    "PunctuationFilter",
    "RepetitionFilter",
    "StopwordsFilter",
]
