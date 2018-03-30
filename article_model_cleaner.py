import argparse, os
from functools import reduce
import importlib.util

file_util_spec = importlib.util.spec_from_file_location("file utils", os.environ['THESIS_DIR'] + "/util/file_utils.py")
file_util = importlib.util.module_from_spec(file_util_spec)
file_util_spec.loader.exec_module(file_util)

progress_indicator_spec = importlib.util.spec_from_file_location("progress indicator", os.environ['THESIS_DIR'] + "/util/progress_indicator.py")
progress_indicator = importlib.util.module_from_spec(progress_indicator_spec)
progress_indicator_spec.loader.exec_module(progress_indicator)

logger_spec = importlib.util.spec_from_file_location("logger", os.environ['THESIS_DIR'] + "/util/logger.py")
logger = importlib.util.module_from_spec(logger_spec)
logger_spec.loader.exec_module(logger)

CLEANED_MODEL_EXT = ".cleaned_model"
MODEL_EXT = ".model"

class CleanError(Exception):
    def __init__(self, message):
        super(CleanError, self).__init__(message)
        self.message = message

def create_missing_data_map():
    return {
        'content': 0,   'published_time': 0,    'url': 0,   'author': 0,
        'title': 0,     'description': 0,       'category': 0
    }

def get_output_path(output_root, article_path):
    article_name = os.path.basename(article_path)
    output_name = article_name.replace(MODEL_EXT, CLEANED_MODEL_EXT)
    return output_root + os.path.sep + output_name

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

def validate_arguments(args):
    assert(os.path.isdir(args.model_root))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-m", "--model_root", required=True, help="Directory contains model files")
    required.add_argument("-o", "--output_root", required=True, help="Directory where to saved cleaned model files")

    args = parser.parse_args()
    validate_arguments(args)

    return (args.model_root, args.output_root)

def execute(model_root, output_root):
    model_paths = list(file_util.files_ends_with(model_root, ".model"))
    progress = progress_indicator.ProgressIndicator("Model cleaner in {}".format(model_root), int(len(model_paths)))
    log = logger.Logger(output_root.rstrip(os.path.sep) + os.path.sep + "execution.log")
    log.clean()
    progress.start()
    for model_path in model_paths:
        article_model = file_util.read_json(model_path)
        try:
            cleaned_article_model = clean_article_model(article_model)
            file_util.save_json(cleaned_article_model, get_output_path(output_root, model_path))
            log.info("PROCESSED", model_path)
            progress.next()
        except CleanError as ex:
            # print(str(ex))
            log.error("FAILED", model_path  )
            progress.next()
            continue
    progress.finish()

if __name__ == '__main__':
    (model_root, output_root) = parse_arguments()
    execute(model_root, output_root)