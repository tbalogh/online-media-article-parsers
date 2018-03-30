from article_parser import execute
from multiprocessing import Pool

def parellel_execute(portal, input_root, output_root):
    execute(portal, input_root, output_root)

# input_root = "/Users/tbalogh/dev/sandboxes/thesis/articles/html/"
input_root = "/Users/tbalogh/dev/sandboxes/thesis_articles"
# output_root = "/Users/tbalogh/dev/sandboxes/thesis/articles/model/"
output_root = "/Users/tbalogh/dev/sandboxes/thesis_articles"



portals = ['index', 'origo', 'nnn', 'nynyny', 'ps']
list_of_params = []
for portal in portals:
    input_root_for_portal =  input_root + '/' + portal + '/html'
    output_root_for_portal = output_root + '/' + portal + '/model'
    list_of_params.append((portal, input_root_for_portal, output_root_for_portal))


pool = Pool()
pool.starmap(parellel_execute, list_of_params)