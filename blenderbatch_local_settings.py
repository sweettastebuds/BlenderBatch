# *************************************************************************
# *                                                                       *
# *                        BlenderBatch_local_settings.py                      *
# *              Please see BlenderBatch_settings.py for details.              *
# *                    Please DO NOT delete this block.                   *
# *                                                                       *
# * How to change settings:                                               *
# * copy the setting you need change from BlenderBatch_settings.py             *
# * paste it into this file                                               *
# * change the value according to instructions                            *
# * save the BlenderBatch_local_settings.py file                               *
# * use BlenderBatch                                                           *
# *************************************************************************

SAVE = True

# GET_MATERIALS = False 	# #	#Double Check code before running again!

# AUTO_INDEX = False

# CLEAN_UP = True

# CLEAN_UP_MATERIAL_FEEDBACK = True

# SAVE_TO_MSWAP = True

"""
	Render Settings
"""
RENDERSETTINGS_FILTER_WIDTH = 1.75


# USE_DENOISING = ['Assett', 'Shadow', 'ShadowsClean', 'Asset','Main']
# DENOISING_DIFFUSE_DIRECT = True # Boolean
# DENOISING_DIFFUSE_INDIRECT = True # Boolean
# DENOISING_FEATURE_STRENGTH = True # Boolean
# DENOISING_GLOSSY_DIRECT = True # Boolean
# DENOISING_GLOSSY_INDIRECT = True # Boolean
# DENOISING_RADIUS = 8 # Intiger
# DENOISING_RELATIVE_PCA = 0.5 # Float
# DENOISING_STORE_PASSES = False # Boolean
# DENOISING_STRENGTH = 0.5 # Float
# DENOISING_SUBSURFACE_DIRECT = True # Boolean
# DENOISING_SUBSURFACE_INDIRECT = True # Boolean
# DENOISING_TRANSMISSION_DIRECT = True # Boolean
# DENOISING_TRANSMISSION_INDIRECT = True # Boolean



####			Start of Adjustsment Options			####
####		Comment These options to turn them Off 		####

#clamp_dir = Takes any float
# RENDERSETTINGS_CLAMP_DIR = 0

#clamp_indir = Takes any float
# RENDERSETTINGS_CLAMP_INDIR = 0

"""
LIGHTS_ADJUSTMENTS:
FALSE = Off
0 = Sets off Lights to 'Hide from Render' and value of 0
n = Sets all lights to the value
{Light Name : Value} = Set specific lights to their own value
"""
# LIGHTS_ADJUSTMENTS = 0

# HDR_ADJUST, HDR_NAME = 1.2, 'Background'



####				End of options				####