"""
Testing filters and parsers functionality
"""

# python imports
import unittest

# project imports
from core import filters, parsers


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.category = 'Blog'

    def test_urlify_category(self):
        urlified = filters.urlify_category(self.category)
        self.assertEqual(urlified, 'Blog1.html')

    def test_parse_markdown(self):
        parsed = filters.parse_markdown('**Boo!**')
        self.assertIn('<p><strong>Boo!</strong></p>', parsed)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = parsers.Parse('content')

    def test_parse_files(self):
        files = self.parser.parse_files()
        self.assertEqual(len(files), 6)

    def test_wrong_directory(self):
        parser = parsers.Parse('some dir')
        parser.parse_files()
        self.assertRaises(FileNotFoundError)


if __name__ == '__main__':
    unittest.main()
