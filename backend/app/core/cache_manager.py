from __future__ import annotations
import hashlib
import json
from datetime import datetime, timedelta
from typing import Any
from pydantic import BaseModel

class CacheEntry(BaseModel):
    key: str
    value: dict[str, Any] | None
    content_hash: str | None
    etag: str | None
    last_modified: str | None
    cached_at: datetime
    ttl_seconds: int
    is_negative: bool

class CacheManager:
    """In-memory cache with TTL, negative caching, and content hashing."""
    
    def __init__(self, default_ttl: int = 3600):
        self._cache: dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
    
    def make_key(self, source_id: str, org_number: str, **params: Any) -> str:
        """Generate a deterministic cache key."""
        sorted_params = sorted(params.items())
        param_str = "&".join(f"{k}={v}" for k, v in sorted_params)
        return f"{source_id}:{org_number}:{param_str}"
    
    def get(self, key: str) -> CacheEntry | None:
        """Get a cached entry if not expired."""
        if key not in self._cache:
            return None
            
        entry = self._cache[key]
        expiry_time = entry.cached_at + timedelta(seconds=entry.ttl_seconds)
        
        if datetime.now() > expiry_time:
            del self._cache[key]
            return None
            
        return entry
    
    def put(self, key: str, value: dict[str, Any] | None, etag: str | None = None, 
            last_modified: str | None = None, ttl: int | None = None,
            is_negative: bool = False) -> None:
        """Store a cache entry."""
        ttl_seconds = ttl if ttl is not None else self._default_ttl
        content_hash = self.compute_hash(value) if value else None
        
        entry = CacheEntry(
            key=key,
            value=value,
            content_hash=content_hash,
            etag=etag,
            last_modified=last_modified,
            cached_at=datetime.now(),
            ttl_seconds=ttl_seconds,
            is_negative=is_negative
        )
        self._cache[key] = entry
    
    def has_content_changed(self, key: str, new_content: dict[str, Any]) -> bool:
        """Check if content has changed using SHA-256 hash comparison."""
        entry = self.get(key)
        if not entry:
            return True
            
        new_hash = self.compute_hash(new_content)
        return entry.content_hash != new_hash
    
    @staticmethod
    def compute_hash(content: dict[str, Any]) -> str:
        """Compute SHA-256 hash of content."""
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode('utf-8')).hexdigest()
    
    def get_etag(self, key: str) -> str | None:
        """Get stored ETag for conditional requests."""
        entry = self.get(key)
        return entry.etag if entry else None
    
    def get_last_modified(self, key: str) -> str | None:
        """Get stored Last-Modified for conditional requests."""
        entry = self.get(key)
        return entry.last_modified if entry else None
    
    def invalidate(self, key: str) -> None:
        """Remove a cache entry."""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
    
    def stats(self) -> dict[str, Any]:
        """Return cache statistics."""
        now = datetime.now()
        active = 0
        expired = 0
        negative = 0
        
        for entry in self._cache.values():
            if now > entry.cached_at + timedelta(seconds=entry.ttl_seconds):
                expired += 1
            else:
                active += 1
                if entry.is_negative:
                    negative += 1
                    
        return {
            "total": len(self._cache),
            "active": active,
            "expired": expired,
            "negative": negative
        }
