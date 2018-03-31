import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import unittest

from article_model_cleaner import date_from_url

class TestArticleModelCleaner(unittest.TestCase):
    def test_date_from_url(self):
        test_map = {
            ('http://index.hu/belfold/2016/08/25/vaszily_mtva_lehallgatas_nyomozas/', 'index'): '2016-08-25T08:00:00+00:00',
            ('http://www.origo.hu/itthon/20170718-ovni-kell-a-gyermekeket-a-kanikulaban.html', 'origo'): '2017-07-18T08:00:00+00:00',
            ('http://www.origo.hu/gazdasag/20131115-tobb-toltennyel-megy-brusszel-ellen-orban.html', 'origo'): '2013-11-15T08:00:00+00:00',
            ('', 'origo'): ''
        }

        for (url, portal), expected in test_map.items():
            self.assertEqual(date_from_url(url, portal), expected)
