from os.path import join, relpath
from glob import glob
import inspect

# Show all file names right under the directory
def browseFileNames(path='.', ext=''):
	return [relpath(f, path) for f in glob(join(path, '*' + ext))]

def getClassesInModule(module):
	classes = []
	for members in inspect.getmembers(module, inspect.isclass):
		classes.append(members[1])
	return classes