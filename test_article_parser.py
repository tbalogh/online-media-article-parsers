import unittest
from article_parser import is_portal_accepted, get_output_path, from_nynyny_date_format, from_origo_date_format, validate_config


class TestArticleParser(unittest.TestCase):

    def test_accepted_portals(self):
        test_map = {
            'index': True, 'origo': True, 'nnn': True, 'nynyny': True, 'ps': True,
            'hvg': False, '': False
        }

        for portal, expected in test_map.items():
            self.assertEquals(is_portal_accepted(portal), expected)

    def test_get_output_path(self):
        test_map = { 
            ('/output_root',  "id1" ) : '/output_root/id1.model',
        }
        for (output_root, original_path), expected in test_map.items():
            assert(get_output_path(output_root, original_path) == expected)

        try:
            get_output_path('/output_root', '')
            self.assertTrue(False,  msg="get_output_path should throw ValueError without file name")
        except ValueError:
            pass

    def test_from_nynynyn_date_format(self):
        #YYYY. month DD. HH:MM
        test_map = {
            "1999. január 12. 13:23": "1999-01-12T13:23:00+00:00",
            "2012. március 1. 09:12": "2012-03-01T09:12:00+00:00"
        }
        for date, expected in test_map.items():
            self.assertEquals(from_nynyny_date_format([date]), expected)

    def test_valid_configs(self):
        valid_configs = [
            {portal: 'index'}, {portal: 'origo'}, {portal: 'nnn'}, {portal: 'nynyny'}, {portal: 'ps'}
        ]
        for config in valid_configs:
            validate_config(config)

    # TODO remove unused test
    # def test_from_origo_date_format(self):
    #     #YYYY. month DD. HH:MM
    #     test_map = {
    #         "\r\n\t\t\tvar strModDate = '2011. 08. 02., 18:08';\r\n\t\t\tif (strModDate.substr(16,1) == ':') strModDate = strModDate.substr(0,15) + '0' + strModDate.substr(15,strModDate.length);\r\n\t\t\tvar strNowDate = '2017. 09. 11., 01:03';\r\n\t\t   ": "2011-08-02T18:08:00+00:00",
    #         "strModDate = '2012. 03. 01. 09:12'": "2012-03-01T09:12:00+00:00"
    #     }
    #     for date, expected in test_map.items():
    #         assert(from_origo_date_format([date]) == expected)