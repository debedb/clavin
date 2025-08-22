#!/usr/bin/env python3
"""Test script for multiple collection support."""

from main import CollectionSpec
import sys


def test_collection_spec_parsing():
    """Test parsing of collection specifications."""
    
    # Test single collection without root
    parser = CollectionSpec()
    parser.add("abc123")
    retval = parser.get_collections()
    assert retval == [("abc123", None)]
    print("✓ Single collection without root")
    
    # Test single collection with root
    parser = CollectionSpec()
    parser.add("abc123:/api/v1")
    retval = parser.get_collections()
    assert retval == [("abc123", "/api/v1")]
    print("✓ Single collection with root")
    
    # Test multiple collections
    parser = CollectionSpec()
    parser.add("abc123")
    parser.add("def456:/api/v2")
    parser.add("ghi789:/api/v3")
    retval = parser.get_collections()
    assert retval == [
        ("abc123", None),
        ("def456", "/api/v2"),
        ("ghi789", "/api/v3")
    ]
    print("✓ Multiple collections with mixed roots")
    
    # Test invalid root (doesn't start with /)
    parser = CollectionSpec()
    try:
        parser.add("abc123:api/v1")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Root path must start with '/'" in str(e)
    print("✓ Invalid root path rejected")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_collection_spec_parsing()