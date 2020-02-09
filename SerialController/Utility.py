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

def getCommandModules(path):
	module_names = [os.path.splitext(n)[0] for n in util.browseFileNames(path=path, ext='.py')]

	modules = []
	for name in module_names:
		modules.append(importlib.import_module(path.replace('\\', '.') + '.' + name))
	
	return modules

def getPythonCommandModulesAndClasses():
	path = 'Commands\PythonCommands'
	modules = getCommandModules(path)

	classes = []
	for mod in modules:
		classes.extend([c for c in getClassesInModule(mod)\
			if issubclass(c, PythonCommandBase.PythonCommand) and hasattr(c, 'NAME')])
	
	return modules, classes

def getMcuCommandModulesAndClasses():
	path = 'Commands\McuCommands'
	modules = getCommandModules(path)

	classes = []
	for mod in modules:
		classes.extend([c for c in getClassesInModule(mod)\
			if issubclass(c, McuCommandBase.McuCommand) and hasattr(c, 'NAME')])
	
	return modules, classes
