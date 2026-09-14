from __future__ import annotations
import pytest
import asyncio
from app.core.cache_manager import CacheManager

@pytest.mark.asyncio
async def test_cache_put_get(mock_cache_manager):
    await mock_cache_manager.put("key1", "value1")
    assert await mock_cache_manager.get("key1") == "value1"

@pytest.mark.asyncio
async def test_cache_ttl(mock_cache_manager):
    await mock_cache_manager.put("key2", "value2", ttl=0.01)
    await asyncio.sleep(0.02)
    assert await mock_cache_manager.get("key2") is None

@pytest.mark.asyncio
async def test_negative_caching(mock_cache_manager):
    await mock_cache_manager.put_negative("key3")
    assert await mock_cache_manager.is_negative("key3") is True

@pytest.mark.asyncio
async def test_content_hash(mock_cache_manager):
    hash1 = mock_cache_manager.hash_content("data")
    hash2 = mock_cache_manager.hash_content("data")
    assert hash1 == hash2

@pytest.mark.asyncio
async def test_etag_storage(mock_cache_manager):
    await mock_cache_manager.store_etag("url1", "etag1")
    assert await mock_cache_manager.get_etag("url1") == "etag1"

@pytest.mark.asyncio
async def test_cache_invalidation(mock_cache_manager):
    await mock_cache_manager.put("key4", "value4")
    await mock_cache_manager.invalidate("key4")
    assert await mock_cache_manager.get("key4") is None

@pytest.mark.asyncio
async def test_cache_stats(mock_cache_manager):
    await mock_cache_manager.put("k", "v")
    await mock_cache_manager.get("k")
    stats = mock_cache_manager.get_stats()
    assert stats["hits"] >= 0
