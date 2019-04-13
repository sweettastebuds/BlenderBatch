 # -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 10:33:45 2016

@author: mfernandez
"""

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import sys
import bpy
import os
import imp
from datetime import datetime

path_to_import = os.path.join(os.path.dirname(__file__), 'blenderbatch_settings.py')
BBS = imp.load_source('blenderbatch_settings.', path_to_import)

path_to_import = os.path.join(os.path.dirname(__file__), 'blenderbatchcommands.py')
BBC = imp.load_source('blenderbatchcommands.', path_to_import)

# Global Variables

C = bpy.context
S = C.scene
D = bpy.data
O = bpy.ops
M = D.materials


"""
	Import blender batch commands to run functions,
	use blenderbatch_setting to determine which functions to run in blenderbatch actions
	from blenderbatchcommands
"""
BBC.sep()

if BBS.GET_MATERIALS:
	mat_list = BBC.getMaterials()
	print(mat_list)

	# mat = BBC.selectMaterial("shagreen")
	# if not mat: print("didn't find material")
	# print("step 1")
	# node = BBC.selectNode("MAPPING", mat)
	# print("step 2")
	# BBC.adjustMapNode(.86, 1, 'scale', node)
	# print("adjusted %s" %node.name)

if BBS.RENDERSETTINGS:
	BBC.RenderSettings(
		BBS.RENDERSETTINGS_RES_X,
		BBS.RENDERSETTINGS_RES_Y,
		BBS.RENDERSETTINGS_RES_PERCENT,
		BBS.RENDERSETTINGS_COLOR_DEPTH,
		BBS.RENDERSETTINGS_COLOR_MODE,
		BBS.RENDERSETTINGS_COMPRESSION,
		BBS.RENDERSETTINGS_RENDER_SAMPLES,
		BBS.RENDERSETTINGS_SAMPLES_TYPE,
		BBS.RENDERSETTINGS_CLAMP_DIR,
		BBS.RENDERSETTINGS_CLAMP_INDIR,
		BBS.RENDERSETTINGS_CAUSTICS_REFLECT,
		BBS.RENDERSETTINGS_CAUSTICS_REFRACT,
		BBS.RENDERSETTINGS_FILTER_GLOSSY,
		BBS.RENDERSETTINGS_FILM_TRANS,
		BBS.RENDERSETTINGS_FILTER_WIDTH,
		BBS.RENDERSETTINGS_FILE_FORMAT
		)

if BBS.USE_DENOISING:
	try:
		if type(BBS.USE_DENOISING) is str:
			layer_name = BBC.getRenderLayer(BBS.USE_DENOISING)
			# if not type(layer_name) == bpy.types.SceneRenderLayer: layer_name = S.render.layers[layer_name]
			BBC.enableDenoising(layer_name)

			print("Setting Denoiser Settings: %s" %layer_name)
			layer_name = S.render.layers[layer_name]

			if BBS.DENOISING_DIFFUSE_DIRECT:
				try:
					layer_name.cycles.denoising_diffuse_direct = BBS.DENOISING_DIFFUSE_DIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_DIFFUSE_INDIRECT:
				try:
					layer_name.cycles.denoising_diffuse_indirect = BBS.DENOISING_DIFFUSE_INDIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_FEATURE_STRENGTH:
				try:
					layer_name.cycles.denoising_feature_strength = BBS.DENOISING_FEATURE_STRENGTH
				except Exception as e:
					print(e)

			elif BBS.DENOISING_GLOSSY_DIRECT:
				try:
					layer_name.cycles.denoising_glossy_direct = BBS.DENOISING_GLOSSY_DIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_GLOSSY_INDIRECT:
				try:
					layer_name.cycles.denoising_glossy_indirect = BBS.DENOISING_GLOSSY_INDIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_RADIUS:
				try:
					layer_name.cycles.denoising_radius = BBS.DENOISING_RADIUS
				except Exception as e:
					print(e)

			elif BBS.DENOISING_RELATIVE_PCA:
				try:
					layer_name.cycles.denoising_relative_pca = BBS.DENOISING_RELATIVE_PCA
				except Exception as e:
					print(e)

			elif BBS.DENOISING_STORE_PASSES:
				try:
					layer_name.cycles.denoising_store_passes = BBS.DENOISING_STORE_PASSES
				except Exception as e:
					print(e)

			elif BBS.DENOISING_STRENGTH:
				try:
					layer_name.cycles.denoising_strength = BBS.DENOISING_STRENGTH
				except Exception as e:
					print(e)

			elif BBS.DENOISING_SUBSURFACE_DIRECT:
				try:
					layer_name.cycles.denoising_subsurface_direct = BBS.DENOISING_SUBSURFACE_DIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_SUBSURFACE_INDIRECT:
				try:
					layer_name.cycles.denoising_subsurface_indirect = BBS.DENOISING_SUBSURFACE_INDIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_TRANSMISSION_DIRECT:
				try:
					layer_name.cycles.denoising_transmission_direct = BBS.DENOISING_TRANSMISSION_DIRECT
				except Exception as e:
					print(e)

			elif BBS.DENOISING_TRANSMISSION_INDIRECT:
				try:
					layer_name.cycles.denoising_transmission_indirect = BBS.DENOISING_TRANSMISSION_INDIRECT
				except Exception as e:
					print(e)


		elif type(BBS.USE_DENOISING) is list or tuple:
			for layer in BBS.USE_DENOISING:
				layer_name = BBC.getRenderLayer(layer)
				if not layer_name: continue

				# if not type(layer_name) == bpy.types.SceneRenderLayer: layer_name = S.render.layers[layer_name]
				BBC.enableDenoising(layer_name)

				print("Setting Denoiser Settings: %s" %layer_name)
				layer_name = S.render.layers[layer_name]


				if BBS.DENOISING_DIFFUSE_DIRECT:
					try:
						layer_name.cycles.denoising_diffuse_direct = BBS.DENOISING_DIFFUSE_DIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_DIFFUSE_INDIRECT:
					try:
						layer_name.cycles.denoising_diffuse_indirect = BBS.DENOISING_DIFFUSE_INDIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_FEATURE_STRENGTH:
					try:
						layer_name.cycles.denoising_feature_strength = BBS.DENOISING_FEATURE_STRENGTH
					except Exception as e:
						print(e)

				elif BBS.DENOISING_GLOSSY_DIRECT:
					try:
						layer_name.cycles.denoising_glossy_direct = BBS.DENOISING_GLOSSY_DIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_GLOSSY_INDIRECT:
					try:
						layer_name.cycles.denoising_glossy_indirect = BBS.DENOISING_GLOSSY_INDIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_RADIUS:
					try:
						layer_name.cycles.denoising_radius = BBS.DENOISING_RADIUS
					except Exception as e:
						print(e)

				elif BBS.DENOISING_RELATIVE_PCA:
					try:
						layer_name.cycles.denoising_relative_pca = BBS.DENOISING_RELATIVE_PCA
					except Exception as e:
						print(e)

				elif BBS.DENOISING_STORE_PASSES:
					try:
						layer_name.cycles.denoising_store_passes = BBS.DENOISING_STORE_PASSES
					except Exception as e:
						print(e)

				elif BBS.DENOISING_STRENGTH:
					try:
						layer_name.cycles.denoising_strength = BBS.DENOISING_STRENGTH
					except Exception as e:
						print(e)

				elif BBS.DENOISING_SUBSURFACE_DIRECT:
					try:
						layer_name.cycles.denoising_subsurface_direct = BBS.DENOISING_SUBSURFACE_DIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_SUBSURFACE_INDIRECT:
					try:
						layer_name.cycles.denoising_subsurface_indirect = BBS.DENOISING_SUBSURFACE_INDIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_TRANSMISSION_DIRECT:
					try:
						layer_name.cycles.denoising_transmission_direct = BBS.DENOISING_TRANSMISSION_DIRECT
					except Exception as e:
						print(e)

				elif BBS.DENOISING_TRANSMISSION_INDIRECT:
					try:
						layer_name.cycles.denoising_transmission_indirect = BBS.DENOISING_TRANSMISSION_INDIRECT
					except Exception as e:
						print(e)

		else:
			print("USE_DENOISING is not an acceptable type: str:"", list:[], tuple:()")

	except Exception as e:
		raise e


if BBS.AUTO_INDEX:
	BBC.AutoIndex()


if BBS.CLEAN_UP:
	print("*" * 100)
	print("CLEAN_UP")
	print("*" * 100)
	BBC.CleanUpBlend(
		BBS.CLEAN_UP_DELETE_OBJS_NOT_RENDERED,
		BBS.CLEAN_UP_MATERIAL_FEEDBACK
		)
	BBC.CheckBlendSetup(BBS.CLEAN_UP_LOG_FILEPATH)

if BBS.SAVE_TO_MSWAP:
	BBC.Save_to_MSwap()

if BBS.OPENGL_RENDER:
	BBC.do_main_opengl(
		BBS.OPENGL_RENDER_PATH,
		BBS.OPENGL_RENDER_ANIMATION
		)
if BBS.LIGHTS_ADJUSTMENTS is False:
	""

elif BBS.LIGHTS_ADJUSTMENTS == 0:
	print("Turning OFF all Lights")
	BBC.light_strength_adjustment(light_strength = 0)

elif BBS.LIGHTS_ADJUSTMENTS > 0:
	print("All Light emission values will be adjusted to:",BBS.LIGHTS_ADJUSTMENTS)
	BBC.light_strength_adjustment(light_strength = BBS.LIGHTS_ADJUSTMENTS)

elif type(BBS.LIGHTS_ADJUSTMENTS) is dict:
	print("adjustments based on dictionary Key:value pairs")

if BBS.HDR_ADJUST:
	BBC.hdr_adjust(BBS.HDR_ADJUST,BBS.HDR_NAME)

#-------------------------
if BBS.SAVE:
	BBC.save()

BBC.StatusPrint(BBC.D.filepath)

BBC.sep()