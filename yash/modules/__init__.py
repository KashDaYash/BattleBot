# Sample content for __init__.py
import os
import glob
from os.path import dirname, isfile, join

def __list_all_modules():
    modules_dir = dirname(__file__)
    all_modules = []

    mod_paths = glob.glob(join(modules_dir, "*.py"))

    modules = [
        (f.replace(modules_dir, "yash.modules").replace(os.sep, "."))[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    all_modules.extend(modules)

    return sorted(all_modules)

ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ["ALL_MODULES"]