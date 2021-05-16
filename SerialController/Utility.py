import importlib
import inspect
import os
from glob import glob
from os.path import join, relpath
from logging import getLogger, DEBUG, NullHandler

logger = getLogger(__name__)
logger.addHandler(NullHandler())
logger.setLevel(DEBUG)
logger.propagate = True


def ospath(path):
    return path.replace('/', os.sep)


# Show all file names under the directory
def browseFileNames(path='.', ext='', recursive=True, name_only=True):
    search_path = join(path, '**') if recursive else path
    search_path = join(search_path, '*' + ext)

    if name_only:
        return [relpath(f, path) for f in glob(search_path, recursive=recursive)]
    else:
        return glob(search_path, recursive=recursive)


def getClassesInModule(module):
    classes = []
    for members in inspect.getmembers(module, inspect.isclass):
        classes.append(members[1])
    return classes


def getModuleNames(base_path):
    filenames = browseFileNames(path=base_path, ext='.py', name_only=False)
    return [name[:-3].replace(os.sep, '.') for name in filenames]


def importAllModules(base_path, mod_names=None):
    modules = []
    for name in getModuleNames(base_path) if mod_names is None else mod_names:
        logger.debug(f"Import module: {name}")
        modules.append(importlib.import_module(name))

    return modules
