# ******************************************************************************
# *                                                                            *
# *                           BlenderBatch_settings.py                              *
# *                        Please DO NOT edit this file.                       *
# *   If you need change settings, please edit in BlenderBatch_local_settings.py.   *
# *                                                                            *
# * How to change settings:                                                    *
# * copy the setting you need change and paste into BlenderBatch_local_settings.py  *
# * change the value according to instructions                                 *
# * save the BlenderBatch_local_settings.py file                                    *
# * use BlenderBatch                                                                *
# ******************************************************************************
import os

# BlenderBatch Document:

# Get list of materials in scene
GET_MATERIALS = False

"""
    Clean Up Settings
"""

# Need to clean up a file?
# OPTIONS:
# True: Run the clean up script.
# False: Will do nothing
CLEAN_UP = False

# OPTIONS:
# True: Runs with the clean up script, both must be True.
#       Will run material feedback, and
#       clear unused textures.
# False: Will do nothing.
CLEAN_UP_MATERIAL_FEEDBACK = False

# OPTIONS:
# True: Will delete objects that are not being
#       rendered.
# False: Will do nothing.
CLEAN_UP_DELETE_OBJS_NOT_RENDERED = False

# OPTIONS:
# True: 
# False: 
CLEAN_UP_LOG_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BlenderBatchActions_log.txt')

# Need to reassign pass indexes?
# OPTIONS:
# True: Assigns pass index to all objects under properly named empties.
# False: Does nothing. Not sorry.
AUTO_INDEX = False


"""
    ####################################################################################
    RENDER SETTINGS
        Any Render adjusting settings are below.
"""

# Need to Quick OpenGL Renders?
# OPTIONS:
# True: Renders blend file using OpenGL Renderer.
# False: Does nothing. Not sorry.
OPENGL_RENDER = False

# Output filepath of the OpenGL render
OPENGL_RENDER_PATH = None

# Need to Quick OpenGL Renders?
# OPTIONS:
# True: Renders frame range of blend file using OpenGL Renderer.
# False: Renders the first frame of the blend file. Not sorry.
OPENGL_RENDER_ANIMATION = False

# Need to Quickly Change a Blendfile's Render Settings?
# OPTIONS:
# True: Changes the renders settings based on options that were inputted below
# False: Does nothing. Not sorry.
RENDERSETTINGS = True

#res_x = Takes integers
RENDERSETTINGS_RES_X = None

#res_y = Takes integers
RENDERSETTINGS_RES_Y = None

#res_percent = Takes integers
RENDERSETTINGS_RES_PERCENT = None

#color_depth = Only take '8' or '16', include the quotes
RENDERSETTINGS_COLOR_DEPTH = None

#color_mode = Takes only these values ('BW', 'RGB', 'RGBA')
RENDERSETTINGS_COLOR_MODE = None

#compression = Anything from 0 to 100 
RENDERSETTINGS_COMPRESSION = None

#render_samples = Any number you want just don't be ridiculous
RENDERSETTINGS_RENDER_SAMPLES = None

#samples_type = has two options, BRANCHED_PATH' and 'PATH'
RENDERSETTINGS_SAMPLES_TYPE = None

#clamp_dir = Takes any float
RENDERSETTINGS_CLAMP_DIR = None

#clamp_indir = Takes any float
RENDERSETTINGS_CLAMP_INDIR = None

#caustics_reflect = True or False
RENDERSETTINGS_CAUSTICS_REFLECT = None

#caustics_refract = True or False
RENDERSETTINGS_CAUSTICS_REFRACT = None

#filter_glossy = Takes any float, keep this number pretty low
RENDERSETTINGS_FILTER_GLOSSY = None

#film_trans = True or False
RENDERSETTINGS_FILM_TRANS = None

#filter_width = Takes in a float (i.e '1.75')
RENDERSETTINGS_FILTER_WIDTH = None

#file_format = Takes in a string with all caps for the file format "PNG"
RENDERSETTINGS_FILE_FORMAT = None

# Enable Denoising to the layers listed
# A list, or string must be present
USE_DENOISING = None # Must be a str, ex. "Layer1" or a list, ex. ["layer1", "lyr2"], or tuple, ex. ("layer1", "lyr2").

# Denoising Settings
DENOISING_DIFFUSE_DIRECT = True # Boolean
DENOISING_DIFFUSE_INDIRECT = True # Boolean
DENOISING_FEATURE_STRENGTH = True # Boolean
DENOISING_GLOSSY_DIRECT = True # Boolean
DENOISING_GLOSSY_INDIRECT = True # Boolean
DENOISING_RADIUS = 8 # Intiger
DENOISING_RELATIVE_PCA = 0.5 # Float
DENOISING_STORE_PASSES = False # Boolean
DENOISING_STRENGTH = 0.5 # Float
DENOISING_SUBSURFACE_DIRECT = True # Boolean
DENOISING_SUBSURFACE_INDIRECT = True # Boolean
DENOISING_TRANSMISSION_DIRECT = True # Boolean
DENOISING_TRANSMISSION_INDIRECT = True # Boolean




"""
    #######################################################################
    Light, Material, and Texture Settings

"""

"""
LIGHTS_ADJUSTMENTS:
FALSE = Off
0 = Sets off Lights to 'Hide from Render' and value of 0
n = Sets all lights to the value
{Light Name : Value} = Set specific lights to their own value
"""
LIGHTS_ADJUSTMENTS = False

#Adjust the HDR Strength
#False: is OFF
#value
HDR_ADJUST = False
#Node name of the Background Node you want to adjust
HDR_NAME = None

# Need to Save the blend file to MSwap?
# OPTIONS:
# True: Will save the blend files to the MSwap of each asset.
# False: Will do nothing. Not sorry.
SAVE_TO_MSWAP = False

# Batch Texture Swapper
#List of materials 
TSWAP_MATLABEL = None
TSWAP_TEXQUALITY = None
TSWAP_PACKFILE = True







#----------------------
#Saves the current file.
#False: Will not save, good for deubugging
SAVE = False



print('-before setting import local_settings')
import os
import imp
try:
    path_to_import = os.path.join(os.path.dirname(__file__), 'blenderbatch_local_settings.py')
    local_settings = imp.load_source('local_settings', path_to_import)
    from local_settings import *

except Exception as e:
    if os.path.exists(path_to_import):
        # syntax error
        print('\n*************************************')
        print('* settings get error in importing blenderbatch_local_settings: ' + str(e))
        print('*************************************\n')
        exit(1)
    else:
        # no local_settings.py file exists
        print('\n*************************************')
        print('* no local_settings.py file detected')
        print('*************************************\n')
print('-after setting import local_settings')