import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import ValidationUtils


class TestValidationUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_validate_url_valid_http_url(self):
        url = "http://example.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_valid_https_url(self):
        url = "https://example.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_with_path(self):
        url = "https://example.com/path/to/resource"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_with_query_params(self):
        url = "https://example.com/path?param1=value1&param2=value2"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_with_fragment(self):
        url = "https://example.com/path#section"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_with_port(self):
        url = "https://example.com:8080/path"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_with_subdomain(self):
        url = "https://api.example.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_localhost(self):
        url = "http://localhost:3000"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_ip_address(self):
        url = "http://192.168.1.1:8080"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_ftp_scheme(self):
        url = "ftp://ftp.example.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_custom_scheme(self):
        url = "custom://example.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_no_scheme(self):
        url = "example.com"
        result = ValidationUtils.validate_url(url)
        self.assertFalse(result)

    def test_validate_url_no_netloc(self):
        url = "http://"
        result = ValidationUtils.validate_url(url)
        self.assertFalse(result)

    def test_validate_url_empty_string(self):
        url = ""
        result = ValidationUtils.validate_url(url)
        self.assertFalse(result)

    def test_validate_url_only_scheme(self):
        url = "http:"
        result = ValidationUtils.validate_url(url)
        self.assertFalse(result)

    def test_validate_url_malformed_url(self):
        url = "ht tp://example.com"
        result = ValidationUtils.validate_url(url)
        self.assertFalse(result)

    def test_validate_url_invalid_characters(self):
        url = "https://exam ple.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    def test_validate_url_unicode_domain(self):
        url = "https://тест.com"
        result = ValidationUtils.validate_url(url)
        self.assertTrue(result)

    @patch('src.utils.validation_utils.urlparse')
    def test_validate_url_urlparse_exception(self, mock_urlparse):
        mock_urlparse.side_effect = Exception("Parse error")

        url = "https://example.com"
        result = ValidationUtils.validate_url(url)
        self.assertFalse(result)

    def test_validate_url_none_input(self):
        result = ValidationUtils.validate_url(None)
        self.assertFalse(result)

    def test_validate_url_is_static_method(self):
        result = ValidationUtils.validate_url("https://example.com")
        self.assertTrue(result)

    def test_sanitize_input_simple_dict(self):
        data = {"name": "  John  ", "age": "  25  "}
        result = ValidationUtils.sanitize_input(data)
        expected = {"name": "John", "age": "25"}
        self.assertEqual(result, expected)

    def test_sanitize_input_nested_dict(self):
        data = {
            "user": {
                "name": "  Alice  ",
                "email": "  alice@example.com  "
            },
            "role": "  admin  "
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "user": {
                "name": "Alice",
                "email": "alice@example.com"
            },
            "role": "admin"
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_list_in_dict(self):
        data = {
            "skills": ["  Python  ", "  Flask  ", "  API  "],
            "name": "  Developer  "
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "skills": ["  Python  ", "  Flask  ", "  API  "],
            "name": "Developer"
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_simple_list(self):
        data = ["  item1  ", "  item2  ", "  item3  "]
        result = ValidationUtils.sanitize_input(data)
        expected = ["  item1  ", "  item2  ", "  item3  "]
        self.assertEqual(result, expected)

    def test_sanitize_input_nested_list(self):
        data = [["  item1  ", "  item2  "], ["  item3  ", "  item4  "]]
        result = ValidationUtils.sanitize_input(data)
        expected = [["  item1  ", "  item2  "], ["  item3  ", "  item4  "]]
        self.assertEqual(result, expected)

    def test_sanitize_input_complex_nested_structure(self):
        data = {
            "users": [
                {
                    "info": {
                        "name": "  Admin  ",
                        "roles": ["  admin  ", "  user  "]
                    },
                    "active": "  true  "
                }
            ],
            "settings": {
                "theme": "  dark  ",
                "options": ["  option1  ", "  option2  "]
            }
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "users": [
                {
                    "info": {
                        "name": "Admin",
                        "roles": ["  admin  ", "  user  "]
                    },
                    "active": "true"
                }
            ],
            "settings": {
                "theme": "dark",
                "options": ["  option1  ", "  option2  "]
            }
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_non_string_values(self):
        data = {
            "number": 123,
            "boolean": True,
            "none_value": None,
            "float_value": 45.67
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "number": "123",
            "boolean": "True",
            "none_value": "None",
            "float_value": "45.67"
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_empty_dict(self):
        data = {}
        result = ValidationUtils.sanitize_input(data)
        self.assertEqual(result, {})

    def test_sanitize_input_empty_list(self):
        data = []
        result = ValidationUtils.sanitize_input(data)
        self.assertEqual(result, [])

    def test_sanitize_input_string_with_newlines_and_tabs(self):
        data = {"text": "  \nHello\tWorld\r\n  "}
        result = ValidationUtils.sanitize_input(data)
        expected = {"text": "Hello\tWorld"}
        self.assertEqual(result, expected)

    def test_sanitize_input_special_characters(self):
        data = {
            "password": "  P@ssw0rd!  ",
            "email": "  user@domain.com  ",
            "symbols": "  #$%&*()  "
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "password": "P@ssw0rd!",
            "email": "user@domain.com",
            "symbols": "#$%&*()"
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_unicode_strings(self):
        data = {
            "name": "  José da Silva  ",
            "city": "  São Paulo  ",
            "emoji": "  😀🎉  "
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "name": "José da Silva",
            "city": "São Paulo",
            "emoji": "😀🎉"
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_primitive_value_not_dict_or_list(self):
        result = ValidationUtils.sanitize_input("  test  ")
        self.assertEqual(result, "  test  ")

        result = ValidationUtils.sanitize_input(123)
        self.assertEqual(result, 123)

        result = ValidationUtils.sanitize_input(True)
        self.assertEqual(result, True)

        result = ValidationUtils.sanitize_input(None)
        self.assertEqual(result, None)

    def test_sanitize_input_mixed_types_in_list(self):
        data = [
            "  string  ",
            123,
            {"key": "  value  "},
            ["  nested  "],
            None,
            True
        ]
        result = ValidationUtils.sanitize_input(data)
        expected = [
            "  string  ",
            123,
            {"key": "value"},
            ["  nested  "],
            None,
            True
        ]
        self.assertEqual(result, expected)

    def test_sanitize_input_deep_nesting(self):
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "value": "  deep_value  ",
                            "list": ["  item1  ", "  item2  "]
                        }
                    }
                }
            }
        }
        result = ValidationUtils.sanitize_input(data)
        expected = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "value": "deep_value",
                            "list": ["  item1  ", "  item2  "]
                        }
                    }
                }
            }
        }
        self.assertEqual(result, expected)

    def test_sanitize_input_is_static_method(self):
        data = {"test": "  value  "}
        result = ValidationUtils.sanitize_input(data)
        expected = {"test": "value"}
        self.assertEqual(result, expected)

    def test_sanitize_input_list_with_dicts(self):
        data = [
            {"name": "  John  ", "age": "  25  "},
            {"name": "  Jane  ", "age": "  30  "}
        ]
        result = ValidationUtils.sanitize_input(data)
        expected = [
            {"name": "John", "age": "25"},
            {"name": "Jane", "age": "30"}
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
