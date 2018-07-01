import argparse, os, json
import file_utils.file_utils as file_utils


def validate_arguments(args):
    for model_file in args.model_files:
        assert(os.path.isfile(model_file))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-m", "--model_files", required=True, help="List of article model files", nargs='+')

    args = parser.parse_args()
    validate_arguments(args)

    return args.model_files


def execute(model_files):
    missing_data_map = {
        'content': 0,   'published_time': 0,    'url': 0,   'author': 0,
        'title': 0,     'description': 0,       'category': 0
    }

    for model_path in model_files:
        article_model = file_utils.read_json(model_path)
        for (key, value) in missing_data_map.items():
            if not article_model[key]:
                missing_data_map[key] += 1

    percentage_map = {}
    for (key, value) in missing_data_map.items():
        percentage_map[key] = int((value / (len(model_files) + 1)) * 100)
    print("# of files: " + str(len(model_files)))
    print(percentage_map)


if __name__ == '__main__':
    model_files = parse_arguments()
    execute(model_files)

