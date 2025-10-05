import unittest
from unittest.mock import patch
import logging
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logging_utils import LoggingUtils


class TestLoggingUtils(unittest.TestCase):

    def setUp(self):
        logging.getLogger().handlers.clear()
        logging.getLogger().setLevel(logging.WARNING)

    def tearDown(self):
        logging.getLogger().handlers.clear()
        logging.getLogger().setLevel(logging.WARNING)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_default_level(self, mock_basic_config):
        LoggingUtils.setup_logging()

        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args

        self.assertEqual(call_args[1]['level'], logging.INFO)
        self.assertEqual(call_args[1]['format'], '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.assertEqual(len(call_args[1]['handlers']), 2)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_debug_level(self, mock_basic_config):
        LoggingUtils.setup_logging('DEBUG')

        call_args = mock_basic_config.call_args
        self.assertEqual(call_args[1]['level'], logging.DEBUG)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_warning_level(self, mock_basic_config):
        LoggingUtils.setup_logging('WARNING')

        call_args = mock_basic_config.call_args
        self.assertEqual(call_args[1]['level'], logging.WARNING)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_error_level(self, mock_basic_config):
        LoggingUtils.setup_logging('ERROR')

        call_args = mock_basic_config.call_args
        self.assertEqual(call_args[1]['level'], logging.ERROR)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_critical_level(self, mock_basic_config):
        LoggingUtils.setup_logging('CRITICAL')

        call_args = mock_basic_config.call_args
        self.assertEqual(call_args[1]['level'], logging.CRITICAL)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_lowercase_level(self, mock_basic_config):
        LoggingUtils.setup_logging('info')

        call_args = mock_basic_config.call_args
        self.assertEqual(call_args[1]['level'], logging.INFO)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_mixed_case_level(self, mock_basic_config):
        LoggingUtils.setup_logging('DeBuG')

        call_args = mock_basic_config.call_args
        self.assertEqual(call_args[1]['level'], logging.DEBUG)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_handlers_configuration(self, mock_basic_config):
        LoggingUtils.setup_logging()

        call_args = mock_basic_config.call_args
        handlers = call_args[1]['handlers']

        self.assertEqual(len(handlers), 2)

        handler_types = [type(handler).__name__ for handler in handlers]
        self.assertIn('StreamHandler', handler_types)
        self.assertIn('FileHandler', handler_types)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_file_handler_filename(self, mock_basic_config):
        LoggingUtils.setup_logging()

        call_args = mock_basic_config.call_args
        handlers = call_args[1]['handlers']

        file_handler = None
        for handler in handlers:
            if isinstance(handler, logging.FileHandler):
                file_handler = handler
                break

        self.assertIsNotNone(file_handler)
        self.assertEqual(file_handler.baseFilename, os.path.abspath('app.log'))

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_format_string(self, mock_basic_config):
        LoggingUtils.setup_logging()

        call_args = mock_basic_config.call_args
        expected_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.assertEqual(call_args[1]['format'], expected_format)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_invalid_level_raises_attribute_error(self, mock_basic_config):
        with self.assertRaises(AttributeError):
            LoggingUtils.setup_logging('INVALID_LEVEL')

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_empty_string_level_raises_attribute_error(self, mock_basic_config):
        with self.assertRaises(AttributeError):
            LoggingUtils.setup_logging('')

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_none_level_raises_attribute_error(self, mock_basic_config):
        with self.assertRaises(AttributeError):
            LoggingUtils.setup_logging(None)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_is_static_method(self, mock_basic_config):
        LoggingUtils.setup_logging()
        mock_basic_config.assert_called_once()

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_multiple_calls(self, mock_basic_config):
        LoggingUtils.setup_logging('INFO')
        LoggingUtils.setup_logging('DEBUG')
        LoggingUtils.setup_logging('ERROR')

        self.assertEqual(mock_basic_config.call_count, 3)

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_with_spaces_in_level(self, mock_basic_config):
        with self.assertRaises(AttributeError):
            LoggingUtils.setup_logging('  INFO  ')

    @patch('utils.logging_utils.logging.basicConfig')
    def test_setup_logging_numeric_string_level_raises_attribute_error(self, mock_basic_config):
        with self.assertRaises(AttributeError):
            LoggingUtils.setup_logging('10')

    def test_setup_logging_actual_functionality(self):
        LoggingUtils.setup_logging('DEBUG')

        root_logger = logging.getLogger()

        self.assertEqual(root_logger.level, logging.DEBUG)

        self.assertGreater(len(root_logger.handlers), 0)

    def test_setup_logging_creates_log_file(self):
        LoggingUtils.setup_logging()

        logger = logging.getLogger('test')
        logger.info('Test message')

        self.assertTrue(os.path.exists('app.log'))


if __name__ == '__main__':
    unittest.main()
