import argparse, os, importlib.util

spec = importlib.util.spec_from_file_location("util", os.environ['THESIS_DIR'] + "/util/file_utils.py")
file_util = importlib.util.module_from_spec(spec)
spec.loader.exec_module(file_util)

MODEL_EXTENSION = ".cleaned_model"

def create_missing_data_map():
    return {    
        'content': 0,   'published_time': 0,    'url': 0,   'author': 0,
        'title': 0,     'description': 0,       'category': 0
    }

def validate_arguments(args):
    assert(os.path.isdir(args.model_root))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-m", "--model_root", required=True, help="Directory contains model files")

    args = parser.parse_args()
    validate_arguments(args)
    
    return args.model_root

def execute(model_root):
    model_files = list(file_util.files_ends_with(model_root, MODEL_EXTENSION))
    missing_data_map = create_missing_data_map()
    for model_path in model_files:
        article_model = file_util.read_json(model_path)
        for (key, value) in missing_data_map.items():
            if not article_model[key]:
                missing_data_map[key] += 1

    percentage_map = {}
    for (key, value) in missing_data_map.items():
        percentage_map[key] = int((value / (len(model_files) + 1 )) * 100)
    print("# of files: " + str(len(model_files)))
    print(percentage_map)

if __name__ == '__main__':
    model_root = parse_arguments()
    execute(model_root)