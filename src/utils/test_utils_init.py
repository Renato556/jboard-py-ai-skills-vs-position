import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import LoggingUtils, ValidationUtils
from src import utils


class TestUtilsInit(unittest.TestCase):

    def test_logging_utils_import(self):
        self.assertTrue(hasattr(utils, 'LoggingUtils'))
        self.assertEqual(utils.LoggingUtils, LoggingUtils)

    def test_validation_utils_import(self):
        self.assertTrue(hasattr(utils, 'ValidationUtils'))
        self.assertEqual(utils.ValidationUtils, ValidationUtils)

    def test_direct_import_logging_utils(self):
        from src.utils import LoggingUtils as LU
        self.assertIsNotNone(LU)
        self.assertTrue(hasattr(LU, 'setup_logging'))

    def test_direct_import_validation_utils(self):
        from src.utils import ValidationUtils as VU
        self.assertIsNotNone(VU)
        self.assertTrue(hasattr(VU, 'validate_url'))
        self.assertTrue(hasattr(VU, 'sanitize_input'))

    def test_utils_module_functionality(self):
        self.assertTrue(callable(utils.LoggingUtils.setup_logging))

        result = utils.ValidationUtils.validate_url("https://example.com")
        self.assertTrue(result)

        data = {"test": "  value  "}
        sanitized = utils.ValidationUtils.sanitize_input(data)
        self.assertEqual(sanitized, {"test": "value"})


if __name__ == '__main__':
    unittest.main()
