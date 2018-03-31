import sys, os, codecs, json, re, argparse, hashlib
from os.path import isfile, join
from lxml import html
from functools import reduce

import file_utils 
import executor_logger as logger
import progress_indicator

SHA1 = hashlib.sha1()
LOG_PATH = None
MODEL_EXTENSION = ".model"


class DateParseError(Exception):
    def __init__(self, message):
        super(DateParseError, self).__init__(message)
        self.message = message


class OrigoDateParseError(DateParseError):
    pass


class ArticleParseError(Exception):
    pass


def evaluate_xpath(article_html, xpath_expr, separator, transformator):
    return concat(transformator(not_nones(article_html.xpath(xpath_expr))), separator)


def not_nones(values):
    return [v for v in values if type(v) is not None]


def concat(parts, separator):
    return reduce(lambda x, y: x + y.strip() + separator, parts, "").rstrip(separator)


def no_transformation(xpath_result):
    return xpath_result


def unique(xpath_result):
    if isinstance(xpath_result, list):
        return set(xpath_result)
    return xpath_result


def from_origo_date_format(xpath_result):
    # YYYY-MM-DDTHH:MM   ->    YYYY-MM-DDTHH:MM:SS+HH:MM
    if len(xpath_result) is 1:
        return xpath_result[0] + ":00+00:00"
    return ""

def double_digit(might_double_digit_str):
    if len(might_double_digit_str) is 1:
        return '0' + might_double_digit_str
    return might_double_digit_str


def month_as_number(month_as_str):
    month_map = {
        'január': '01', 'február': '02', 'március': '03', 'április': '04', 'május': '05', 'június': '06',
        'július': '07', 'augusztus': '08', 'szeptember': '09', 'október': '10', 'november': '11', 'december': '12'
    }
    if month_as_str not in month_map.keys():
        raise DateParseError("month as str failed " + month_as_str)
    return month_map[month_as_str]


nynyny_date_regex = re.compile("([\d]{4})\.\s+([\w]+)\s+([\d][\d]?)\.\s+([\d]{2}):([\d]{2})$")


def from_nynyny_date_format(xpath_result):
    # YYYY. month DD. HH:MM   ->    YYYY-MM-DDTHH:MM:SS+HH:MM
    if len(xpath_result) == 1:
        matches = nynyny_date_regex.match(xpath_result[0])
        if not matches:
            raise DateParseError("no nynyny date format found in: " + str(xpath_result))
        months = month_as_number(matches.group(2))
        days = double_digit(matches.group(3))
        return "{}-{}-{}T{}:{}:00+00:00".format(matches.group(1), months, days, matches.group(4), matches.group(5))
    else:
        raise DateParseError("xpath result contains more than one date: " + xpath_result)


xpath_map_factory = {}


def index_xpath_map():
    data_xpath_map = dict()
    data_xpath_map['content'] = (
    '//div[@class="cikk-torzs"]/p/text() | //div[@class="cikk-torzs"]/h3//text() | //div[@class="cikk-torzs"]/blockquote//text() | //div[@class="cikk-torzs"]/ul//text()',
    " ", no_transformation)
    data_xpath_map['published_time'] = (
    '/html/head/meta[@property="article:published_time"]/@content', "", no_transformation)
    data_xpath_map['url'] = ('/html/head/meta[@property="og:url"]/@content', "", no_transformation)

    data_xpath_map['author'] = ('/html/head/meta[@name="author"]/@content', "", no_transformation)
    data_xpath_map['title'] = ('/html/head/meta[@property="og:title"]/@content', "", no_transformation)
    data_xpath_map['description'] = ('/html/head/meta[@property="og:description"]/@content', "", no_transformation)
    data_xpath_map['category'] = ('/html/head/meta[@name="news_keywords"]/@content', "", no_transformation)
    data_xpath_map['tags'] = ('/html/head/meta[@name="keywords"]/@content', ";", no_transformation)
    return data_xpath_map


xpath_map_factory['index'] = index_xpath_map


def nnn_xpath_map():
    data_xpath_map = dict()
    data_xpath_map['content'] = ('//main[@id="content-main"]/article/p/text()', " ", no_transformation)
    data_xpath_map['published_time'] = (
    '/html/head/meta[@property="article:published_time"]/@content', "", no_transformation)
    data_xpath_map['url'] = ('/html/head/meta[@property="og:url"]/@content', "", no_transformation)

    data_xpath_map['author'] = ('/html/head/meta[@name="author"]/@content', "", no_transformation)
    data_xpath_map['title'] = ('/html/head/meta[@name="title"]/@content', "", no_transformation)
    data_xpath_map['description'] = ('/html/head/meta[@name="description"]/@content', "", no_transformation)
    data_xpath_map['category'] = ('/html/head/meta[@name="category"]/@value', "", no_transformation)
    data_xpath_map['tags'] = ('/html/head/meta[@property="article:tag"]/@content', ";", no_transformation)
    return data_xpath_map


xpath_map_factory['nnn'] = nnn_xpath_map


def nynyny_xpath_map():
    data_xpath_map = dict()
    data_xpath_map['content'] = ('//*[@id="cikkholder"]/div[@class="maincontent8"]//p/text()', " ", no_transformation)
    data_xpath_map['published_time'] = ('//*[@id="cikkholder"]/p[1]/text()', "", from_nynyny_date_format)
    data_xpath_map['url'] = ('/html/head/meta[@property="og:url"]/@content', "", no_transformation)

    data_xpath_map['author'] = ('//*[@id="cikkholder"]/div[2]/div[2]/div/p/a/text()', "", no_transformation)
    data_xpath_map['title'] = ('/html/head/meta[@property="og:title"]/@content', "", no_transformation)
    data_xpath_map['description'] = ('/html/head/meta[@property="og:description"]/@content', "", no_transformation)
    data_xpath_map['category'] = ('//*[@id="cikkholder"]/div[1]/a/text()', "", no_transformation)
    data_xpath_map['tags'] = ('//*[@id="cikkholder"]/div/div/a/text()', ";", no_transformation)
    return data_xpath_map


xpath_map_factory['nynyny'] = nynyny_xpath_map


def origo_xpath_map():
    data_xpath_map = dict()
    data_xpath_map['content'] = (
    '//div[@id="article-text"]/p/text() | //div[@id="article-text"]/h2/text() | //div[@id="article-lead"]/p/text()',
    " ", no_transformation)
    data_xpath_map['published_time'] = ('//span[@id="article-date"]/@datetime', "", from_origo_date_format)
    data_xpath_map['url'] = ('/html/head/meta[@property="og:url"]/@content', "", no_transformation)

    data_xpath_map['author'] = ('//span[@class="article-author"]/text()', "", no_transformation)
    data_xpath_map['title'] = ('/html/head/meta[@name="title"]/@content', "", no_transformation)
    data_xpath_map['description'] = ('/html/head/meta[@name="description"]/@content', "", no_transformation)
    data_xpath_map['category'] = ('//*[@id="breadcrumb"]/a/text()', "", no_transformation)
    return data_xpath_map


xpath_map_factory['origo'] = origo_xpath_map


def ps_xpath_map():
    data_xpath_map = dict()
    data_xpath_map['content'] = ('//div[@class="theiaPostSlider_slides"]//text()', " ", no_transformation)
    data_xpath_map['published_time'] = (
    '/html/head/meta[@property="article:published_time"]/@content', "", no_transformation)
    data_xpath_map['url'] = ('/html/head/meta[@property="og:url"]/@content', "", no_transformation)

    data_xpath_map['author'] = ('//span[@class="vcard author"]/span/a/text()', ";", unique)
    data_xpath_map['title'] = ('/html/head/title/text()', "", no_transformation)
    data_xpath_map['description'] = ('/html/head/meta[@property="og:description"]/@content', "", no_transformation)
    data_xpath_map['category'] = ('/html/head/meta[@property="article:section"]/@content', "", no_transformation)
    # data_xpath_map['post_tags'] = ('//*[@id="left-content"]/div/span/a/text()', ";", no_transformation)
    data_xpath_map['tags'] = ('/html/head/meta[@property="article:tag"]/@content', ";", no_transformation)
    return data_xpath_map


xpath_map_factory['ps'] = ps_xpath_map

ACCEPTED_PORTALS = ['index', 'origo', 'nnn', 'nynyny', 'ps']


def validate_arguments(args):
    if not args.portal in ACCEPTED_PORTALS:
        raise ValueError("portal must be one of the following: " + str(ACCEPTED_PORTALS))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-p", "--portal", required=True,
                          help="One of the following portals: index|origo|nnn|nynyny|ps")
    required.add_argument("-t", "--html_text", required=True, help="Html page as text. Html content of an article of the given portal.")

    args = parser.parse_args()
    validate_arguments(args)

    return args.html_text, args.portal


def generate_id(article):
    SHA1.update(article['url'].encode('utf-8'))
    return SHA1.hexdigest()


def create_article_model(portal, article_html, xpath_map):
    article = dict()
    article['portal'] = portal
    for key, (xpath_expr, separator, transformator) in xpath_map.items():
        article[key] = evaluate_xpath(article_html, xpath_expr, separator, transformator)
    article['id'] = generate_id(article)
    return article


def get_output_path(output_root, file_name):
    if not file_name:
        raise ValueError('file_name should be not empty: ' + file_name)
    output_name = file_name + MODEL_EXTENSION
    return output_root + os.path.sep + output_name


def validate_config(config):
    assert (config['portal'] in ACCEPTED_PORTALS)


def process(text, config):
    if type(config) is str:
        config = json.loads(config)
    validate_config(config)
    article_html = html.fromstring(text)
    portal = config['portal']
    article_model = create_article_model(portal, article_html, xpath_map_factory[portal]())
    return json.dumps(article_model, ensure_ascii=False, sort_keys=True, indent=4)

if __name__ == '__main__':
    text, portal = parse_arguments()
    config = dict()
    config['portal'] = portal
    print(process(text, config))
