import unittest
from article_parser import from_nynyny_date_format, from_origo_date_format, validate_config


class TestArticleParser(unittest.TestCase):

    def test_from_nynynyn_date_format(self):
        test_map = {
            "1999. január 12. 13:23": "1999-01-12T13:23:00+00:00",
            "2012. március 1. 09:12": "2012-03-01T09:12:00+00:00"
        }
        for date, expected in test_map.items():
            self.assertEqual(from_nynyny_date_format([date]), expected)

    def test_valid_configs(self):
        valid_configs = [
            {'portal': 'index'}, {'portal': 'origo'}, {'portal': 'nnn'}, {'portal': 'nynyny'}, {'portal': 'ps'}
        ]
        for config in valid_configs:
            validate_config(config)
