from os import makedirs, path

def init_instances(app):
    try:
        makedirs(path.join(app.instance_path, "poster_cache"))
    except OSError:
        pass
