#!/usr/bin/env python3
"""
Unit tests for utils.py.

Covers:
- access_nested_map (normal cases + KeyError cases)
- get_json (mocked requests.get)
- memoize decorator (mocking the underlying method)
"""
from typing import Any, Dict, Tuple
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map behaviour."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any],
                               path: Tuple[str, ...], expected: Any) -> None:
        """access_nested_map should return the value for the given path."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any],
                                         path: Tuple[str, ...]) -> None:
        """access_nested_map should raise KeyError for missing keys."""
        with self.assertRaises(KeyError) as ctx:
            utils.access_nested_map(nested_map, path)
        # ensure exception message contains the missing key (last item in path)
        self.assertIn(path[-1], str(ctx.exception))


class TestGetJson(unittest.TestCase):
    """Test utils.get_json using mocked requests.get."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any]) -> None:
        """get_json should return the json payload from requests.get."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        with patch('utils.requests.get', return_value=mock_resp) as mock_get:
            result = utils.get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self) -> None:
        """memoize should cache the result and call the underlying method once."""
        class TestClass:
            def a_method(self) -> int:
                """Return a value."""
                return 42

            @utils.memoize
            def a_property(self) -> int:
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mocked:
            first = obj.a_property
            second = obj.a_property
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mocked.assert_called_once()
