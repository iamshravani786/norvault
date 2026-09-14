from __future__ import annotations

from .base import AuthorityLevel, SourceAdapter, AdapterResult, ExtractedFact
from .registry import get_adapter, get_all_adapters, seed_default_sources
from .brreg_enheter import BrregEnheterAdapter
from .brreg_roller import BrregRollerAdapter
from .brreg_regnskap import BrregRegnskapAdapter
from .brreg_underenheter import BrregUnderenheterAdapter
from .website import WebsiteAdapter

__all__ = [
    "AuthorityLevel",
    "SourceAdapter",
    "AdapterResult",
    "ExtractedFact",
    "get_adapter",
    "get_all_adapters",
    "seed_default_sources",
    "BrregEnheterAdapter",
    "BrregRollerAdapter",
    "BrregRegnskapAdapter",
    "BrregUnderenheterAdapter",
    "WebsiteAdapter",
]
