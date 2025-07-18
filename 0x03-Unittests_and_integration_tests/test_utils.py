#!/usr/bin/env python3
"""Test utils.access_nested_map function."""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Dict, Tuple, Any


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected: Any,
    ) -> None:
        """Test access_nested_map with valid inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

@parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected_exception: Exception,
    ) -> None:
        """Test access_nested_map raises exceptions."""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)

#!/usr/bin/env python3
"""Test utils.get_json function."""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import get_json
from typing import Dict


class TestGetJson(unittest.TestCase):
    """Test class for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            mock_get: Mock,
    ) -> None:
        """Test get_json returns expected result."""
        mock_get.return_value = Mock(json=lambda: test_payload)
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)

#!/usr/bin/env python3
"""Test utils.memoize decorator."""
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self) -> None:
        """Test memoize decorator caches properly."""
        class TestClass:
            """Test class with memoized property."""

            def a_method(self) -> int:
                """Return 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized property."""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test = TestClass()
            self.assertEqual(test.a_property, 42)
            self.assertEqual(test.a_property, 42)
            mock_method.assert_called_once()
