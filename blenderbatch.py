

import os
import sys
import imp
import subprocess
import logging
import datetime


try:
    sys.path.append(r"C:\Outward")
    import common_settings
    
except Exception as e:
    print(r'''
************************************************************************
* Please install the newest version at
*    "T:\OutwardSoftware\install_all_packages.bat"
************************************************************************
''')
    print(str(e))
    exit(1)

# Pulls Blender Path
BLENDER_EXE_PATH = common_settings.BLENDER_INSTALLED_LOCATION

path_to_import = os.path.join(os.path.dirname(__file__), 'blenderbatch_settings.py')
blenderbatch_settings = imp.load_source('blenderbatch_settings.', path_to_import)

path_to_import = os.path.join(os.path.dirname(__file__), 'blenderbatchactions.py')
print("*" * 100)
print("path_to_import contains %s" % (path_to_import))
print("*" * 100)
blenderbatch_actions = path_to_import

##########
#	DEFINITIONS START

#	LOGGER CONFIG
LOGGER_CONFIGED = False

logger = logging.getLogger('blenderbatch_logger')
log_dir = os.path.join(os.path.dirname(__file__), 'log')
#	Checks if log dir exists, and creates it if not
if not os.path.exists(log_dir):
	os.makedirs(log_dir)
#	Sets log filenames per run instance
log_file = os.path.join(log_dir, 'log_' + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.txt')
error_log_file = os.path.join(log_dir, 'error_log_' + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.txt')
assets_log_file = os.path.join(log_dir, 'asset_log_' + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + '.txt')

#	ASSET LOG FILE CREATION
with open(assets_log_file, 'w') as assets_log:
	assets_log.write("*" * 100+"\n")
	assets_log.write("Assets Log - " + datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S") + "\n")
	assets_log.write("*" * 100+"\n")

assets_log.close()

def configure_logging():
	# http://stackoverflow.com/questions/4136129/managing-loggers-with-python-logging
	global LOGGER_CONFIGED
	if not LOGGER_CONFIGED:
		format = "%(asctime)s - %(levelname)s - %(message)s"
		formatter = logging.Formatter(format)
		#logging.basicConfig(format=format)
		logger.setLevel(logging.DEBUG) # or whatever
		console = logging.StreamHandler()
		file = logging.FileHandler(log_file)
		error_file = logging.FileHandler(error_log_file)
		console.setFormatter(formatter)
		file.setFormatter(formatter)
		error_file.setFormatter(formatter)
		error_file.setLevel(logging.ERROR)
		#set a level on the handlers if you want;
		#if you do, they will only output events that are >= that level
		logger.addHandler(console)
		logger.addHandler(file)
		logger.addHandler(error_file)
		LOGGER_CONFIGED = True
		logger.debug('Configure logging')


def get_user_input():
	return raw_input()

def query_yes_no(question, default="yes"):
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".
	"""
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = get_user_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")

def parse_inputs():
	# skip first one since it's barkeep.py itself
	print sys.argv
#	blend_filepath_list = [r"G:\CrateAndBarrel\Assets\Blake_Uph_Ottoman\BlenderFiles\batch\Blake_UphOttoman_GalaxyLinenLinenBlend_AnimS.blend",r"G:\CrateAndBarrel\Assets\Blake_Uph_Ottoman\BlenderFiles\batch\Blake_UphOttoman_SunbrellaSailSeagullBasketweave_AnimS.blend",r"G:\CrateAndBarrel\Assets\Blake_Uph_Ottoman\BlenderFiles\batch\Blake_UphOttoman_SunbrellaSundialCementCanvas_AnimS.blend",r"G:\CrateAndBarrel\Assets\Blake_Uph_Ottoman\BlenderFiles\batch\Blake_UphOttoman_SunbrellaSundialCharcoalCanvas_AnimS.blend",r"G:\CrateAndBarrel\Assets\Blake_Uph_Ottoman\BlenderFiles\batch\Blake_UphOttoman_SunbrellaSundialCoalCanvas_AnimS.blend"]
	blend_filepath_list = []
	for filepath in sys.argv[1:]:
		if filepath.startswith('-' or '--'):
			 # is a config argument, skip
			continue
		if filepath.endswith('.blend'):
			blend_filepath_list.append(filepath)
			logger.debug('blend file detected')
		elif not os.path.isdir(filepath):
			logger.debug('input is not blend file, reading file...')
			with open(filepath, 'r') as text_input_file:
				filepath_list = text_input_file.readlines()
				for filepath in filepath_list:
					filepath = filepath.rstrip()
					logger.debug('filepath: ' + str(filepath))
					if filepath.endswith('.blend'):
						blend_filepath_list.append(filepath)
					else:
						logger.error('Invalid filepath "' +
									filepath +
									'": expected .blend file')
	return blend_filepath_list

if __name__ == "__main__":
	"""
	for blendfile
	subprocess call blendfile python batch_actions

	"""
	configure_logging()
	parsed_blendfile_list = parse_inputs()

	with open(blenderbatch_settings.CLEAN_UP_LOG_FILEPATH, 'w') as f:
		f.close()
	parsed_blendfile_list = [files for files in parsed_blendfile_list if files.endswith('.blend')]
	count = 0      
	for blend in parsed_blendfile_list:
		count +=1
		if blenderbatch_settings.OPENGL_RENDER:
			subprocess.call(['call', BLENDER_EXE_PATH, blend, '-P', blenderbatch_actions], shell=True)
		else:
			subprocess.call(['call', BLENDER_EXE_PATH, '-b', blend, '-P', blenderbatch_actions], shell=True)
			
	print 'Batch Process complete!', count

