from missing_data_counter import execute

portals = ['index', 'origo', 'nnn', 'nynyny', 'ps']
model_root = "/Users/tbalogh/dev/sandboxes/thesis/articles/cleaned_model"
for portal in portals:
    print(portal)
    execute(model_root + "/" + portal)