import argparse, os, json
from functools import reduce
import importlib.util

import file_utils

class CleanError(Exception):
    def __init__(self, message):
        super(CleanError, self).__init__(message)
        self.message = message

def create_missing_data_map():
    return {
        'content': 0,   'published_time': 0,    'url': 0,   'author': 0,
        'title': 0,     'description': 0,       'category': 0
    }


def date_from_url(url, portal):
    if portal == 'index' and url:       
        (years, months, days) = url.split('/')[-5:-2]       #http://index.hu/belfold/2016/08/25/vaszily_mtva_lehallgatas_nyomozas/
        return "{}-{}-{}T08:00:00+00:00".format(years, months, days)
    elif portal == 'origo' and url:                 
        yyyymmdd = url.split('/')[-1][0:8]      #http://www.origo.hu/itthon/20170718-ovni-kell-a-gyermekeket-a-kanikulaban.html
        return "{}-{}-{}T08:00:00+00:00".format(yyyymmdd[0:4], yyyymmdd[4:6], yyyymmdd[6:8])
    else:
        return ""

def clean_article_model(article_model):
    if not article_model['content']:
        article_model['content'] = article_model['description']
    if not article_model['published_time']:
        article_model['published_time'] = date_from_url(article_model['url'], article_model['portal'])
    if not article_model['author']:
        article_model['author'] = article_model['portal']

    if not article_model['content']:
        raise CleanError("both content and description was empty")
    if not article_model['published_time']:
        raise CleanError("published time was empty and can not be extracted from other sources")

    return article_model


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-a", "--article_content", required=True, help="The content of article")

    args = parser.parse_args()

    return args.article_content


def process(article_model_str):
    try:
        model = json.loads(article_model_str)
        cleaned_model = clean_article_model(model)
        print(json.dumps(cleaned_model, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
    except IOError as ex:
        pass

if __name__ == '__main__':
    article_model_str = parse_arguments()
    process(article_model_str)
