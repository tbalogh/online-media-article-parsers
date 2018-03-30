from article_model_cleaner import execute
from multiprocessing import Pool

portals = ['index', 'origo', 'nnn', 'nynyny', 'ps']
# input_root = "/Users/tbalogh/dev/sandboxes/thesis/articles/model/"
input_root = "/Users/tbalogh/dev/sandboxes/thesis_articles"
# output_root = "/Users/tbalogh/dev/sandboxes/thesis/articles/cleaned_model/"
output_root = "/Users/tbalogh/dev/sandboxes/thesis_articles"
list_of_params = []
for portal in portals:
    input_root_for_portal =  input_root + '/' + portal + '/model'
    output_root_for_portal = output_root + '/' + portal + '/cleaned_model'
    list_of_params.append((input_root_for_portal, output_root_for_portal))

pool = Pool()
pool.starmap(execute, list_of_params)