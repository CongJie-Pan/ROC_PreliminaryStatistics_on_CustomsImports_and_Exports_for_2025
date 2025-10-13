"""
Cache Management Utilities

This module provides utilities for managing Streamlit's data cache,
including cache statistics, manual refresh, and cache monitoring.
"""

import streamlit as st
from typing import Dict, Any, Optional
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages caching operations for the Streamlit dashboard.

    This class provides utilities for monitoring and controlling the
    data cache system.
    """

    def __init__(self):
        """Initialize the cache manager."""
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize session state variables for cache tracking."""
        if 'cache_last_cleared' not in st.session_state:
            st.session_state.cache_last_cleared = None

        if 'cache_hit_count' not in st.session_state:
            st.session_state.cache_hit_count = 0

        if 'cache_miss_count' not in st.session_state:
            st.session_state.cache_miss_count = 0

    def clear_all_caches(self):
        """
        Clear all Streamlit caches.

        This will force reload of all data on next access.
        """
        st.cache_data.clear()
        st.session_state.cache_last_cleared = datetime.now()
        logger.info("All caches cleared")

    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get current cache status and statistics.

        Returns:
            Dictionary containing cache status information
        """
        last_cleared = st.session_state.get('cache_last_cleared')

        if last_cleared:
            time_since_clear = datetime.now() - last_cleared
            minutes_since_clear = int(time_since_clear.total_seconds() / 60)
        else:
            minutes_since_clear = None

        return {
            "cache_enabled": True,
            "last_cleared": last_cleared,
            "minutes_since_clear": minutes_since_clear,
            "cache_hit_count": st.session_state.cache_hit_count,
            "cache_miss_count": st.session_state.cache_miss_count
        }

    def display_cache_info(self):
        """
        Display cache information in the Streamlit UI.

        This is useful for debugging and monitoring cache performance.
        """
        status = self.get_cache_status()

        with st.expander("🔧 Cache Information", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Cache Status", "Enabled" if status["cache_enabled"] else "Disabled")

                if status["last_cleared"]:
                    st.metric("Last Cleared", f"{status['minutes_since_clear']} min ago")
                else:
                    st.metric("Last Cleared", "Never")

            with col2:
                st.metric("Cache Hits", status["cache_hit_count"])
                st.metric("Cache Misses", status["cache_miss_count"])

            if st.button("🔄 Clear Cache"):
                self.clear_all_caches()
                st.success("✅ Cache cleared successfully!")
                st.rerun()

    def record_cache_hit(self):
        """Record a cache hit event."""
        st.session_state.cache_hit_count += 1

    def record_cache_miss(self):
        """Record a cache miss event."""
        st.session_state.cache_miss_count += 1


def get_cache_key(table_name: str, **kwargs) -> str:
    """
    Generate a cache key for a specific data request.

    Args:
        table_name: Name of the table
        **kwargs: Additional parameters that affect the cache

    Returns:
        String cache key

    Examples:
        >>> key = get_cache_key('table08', columns=['year_month'])
        >>> print(key)
    """
    parts = [table_name]

    for key, value in sorted(kwargs.items()):
        if value is not None:
            parts.append(f"{key}={value}")

    return "_".join(parts)


def estimate_cache_size() -> str:
    """
    Estimate the size of cached data in memory.

    Returns:
        String representation of estimated cache size

    Note:
        This is an approximation and may not reflect actual memory usage.
    """
    try:
        import sys

        # Get all cached data (this is an approximation)
        cache_size_bytes = sys.getsizeof(st.session_state)

        # Convert to appropriate unit
        if cache_size_bytes < 1024:
            return f"{cache_size_bytes} B"
        elif cache_size_bytes < 1024**2:
            return f"{cache_size_bytes / 1024:.2f} KB"
        elif cache_size_bytes < 1024**3:
            return f"{cache_size_bytes / (1024**2):.2f} MB"
        else:
            return f"{cache_size_bytes / (1024**3):.2f} GB"

    except Exception as e:
        logger.error(f"Error estimating cache size: {e}")
        return "Unknown"


def should_refresh_cache(last_update: Optional[datetime], ttl_seconds: int = 3600) -> bool:
    """
    Determine if cache should be refreshed based on TTL.

    Args:
        last_update: Timestamp of last cache update
        ttl_seconds: Time-to-live in seconds (default: 1 hour)

    Returns:
        True if cache should be refreshed, False otherwise

    Examples:
        >>> from datetime import datetime, timedelta
        >>> last_update = datetime.now() - timedelta(hours=2)
        >>> should_refresh_cache(last_update, ttl_seconds=3600)
        True
    """
    if last_update is None:
        return True

    age = datetime.now() - last_update
    return age.total_seconds() > ttl_seconds


# Global cache manager instance
cache_manager = CacheManager()
