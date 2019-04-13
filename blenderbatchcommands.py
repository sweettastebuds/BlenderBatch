
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:29:36 2017

@author: mfernandez
"""
import os
import sys
import bpy
import math
from mathutils import Vector
from bpy.app.handlers import persistent

# Global Variables

C = bpy.context
S = C.scene
D = bpy.data
O = bpy.ops
M = D.materials

######################################################################
## Log Methods
######################################################################

def sep():
	print("\n")
	print("#"*50)
	print("\n")

def StatusPrint(string):
	if type(string) == str:
		print("\n")
		print("-"*50)
		print("\n %s" % (string))
		print("-"*50)
		print("\n")
	elif type(string) != str:
		string = str(string)
		print("\n")
		print("-"*50)
		print("\n %s" % (string))
		print("-"*50)
		print("\n")
	else:
		print("\n")
		print("-"*50)
		print('Input is not a string')
		print("-"*50)
		print("\n")

# Logs data on a per asset process
## Only logs data from methods with log commandsw
# def AssetLog(log_path, log_list):
# 	with open(log_path, 'a') as log:
# 		for l in 
######################################################################
## Blender Methods
######################################################################

# Renames Materials
def Material_Rename(m_name, m_newname):
	for material in data.materials:
		if material.name == m_name:
			material.name = m_newname

# Returns List of Materials in a Scene
def getMaterials():
	mat_list = []

	for mat in M:
		mat_list.append(mat.name)

	return mat_list

def getRenderLayer(layernames):
	render_layers = S.render.layers
	layers = []

	if type(layernames) is str:
		for layer in render_layers.keys():
			if layernames in layer:
				print("Get Render Layer: %s" %layer)
				return layer

	
	elif type(layernames) is str or tuple:
		for layerName in layernames:
			for layer in render_layers.keys():
				if layerName in layer:
					layers.append(layer)

		print("Get Render Layers: %s" %str(layers))
		return layers

	else:
		print("arg supplied is not of a supported type")

def enableDenoising(layer):
	print("Enabling Denoiser for layer: %s" %layer)

	try:
		if type(layer) is str:
			active_layer =S.render.layers[layer]

			if not active_layer.cycles.use_denoising:
				active_layer.cycles.use_denoising = True

		elif type(layer) == bpy.types.SceneRenderLayer:
			active_layer = layer
			if not active_layer.cycles.use_denoising: active_layer.cycles.use_denoising = True

	except Exception as e:
		raise e


def AutoIndex(floorName = ''):
	ops.autoindex.auto()

	if floorName:
		for emty in data.objects:
			if emty.type == "EMPTY":
				if emty.name == 'Scene' or 'Scene.0' in emty.name:
					S.objects.active = emty
					ops.object.select_grouped(type='CHILDREN_RECURSIVE')
					for obj in context.selected_objects:
						if obj.type == 'MESH' and floorName in obj.name:
							obj.pass_index = 997
							StatusPrint(obj.name, obj.pass_index)


def Make_Camera_Active(obj):
	for scene in data.scenes:
		data.scenes[0].camera = obj



#Get object and UV map given their names
def GetObjectAndUVMap( objName, uvMapName ):
	try:
		obj = data.objects[objName]

		if obj.type == 'MESH':
			uvMap = data.uv_layers[uvMapName]
			return obj, uvMap
	except:
		pass

	return None, None


#Scale a 2D vector v, considering a scale s and a pivot point p
def Scale2D( v, s, p ):
	return ( p[0] + s[0]*(v[0] - p[0]), p[1] + s[1]*(v[1] - p[1]) )	 


#Scale a UV map iterating over its coordinates to a given scale and with a pivot point
def ScaleUV( uvMap, scale, pivot ):
	for uvIndex in range( len(uvMap.data) ):
		uvMap.data[uvIndex].uv = Scale2D( uvMap.data[uvIndex].uv, scale, pivot )


def ObjScaleUV(geoName, UVMap = 'UVMap', uvScale = (1.0, 1.0), uvPivot = (0.5, 0.5), singleObj = True):
	"""
	This piece of code scales the UVs of an object dependent on the pivot vector location
	"""
	if singleObj:
		for obj in data.objects:
			if geoName in obj.name:
				objName = obj.name

				#Defines the pivot and scale
				pivot = Vector( uvPivot )
				scale = Vector( uvScale )

				uvMapName = UVMap

				# ------------- Scales Single Object UVs ---------------
				#Get the object from names
				obj, uvMap = GetObjectAndUVMap( objName, uvMapName )

				# #If the object is found, scale its UV map
				if not obj:
					ScaleUV( uvMap, scale, pivot )

		# ------------- Scales Multiple Object UVs ---------------
	elif not singleObj:
		for obj in data.objects:
			for obj in geoName:
				if geoName in obj.name:
					objName = obj.name

					#Defines the pivot and scale
					pivot = Vector( uvPivot )
					scale = Vector( uvScale )

					uvMapName = UVMap

					#Get the object from names
					obj, uvMap = GetObjectAndUVMap( objName, uvMapName )
					if not obj:
						ScaleUV( uvMap, scale, pivot )


def ObjRayVis(objName, camera = True, diffuse = True, glossy = True, transmission = True, scatter = True, shadow = True, world = False):
	"""
	Allows the change of ray visibility according to the parameters set
	"""
	if not world:
		for obj in data.objects:
			for objMesh in objName:
				if objMesh in obj.name:
					if obj is not None:
						obj.cycles_visibility.camera = camera
						obj.cycles_visibility.diffuse = diffuse
						obj.cycles_visibility.glossy = glossy
						obj.cycles_visibility.transmission = transmission
						obj.cycles_visibility.scatter = scatter
						obj.cycles_visibility.shadow = shadow
	elif world:
		for wrld in data.worlds:
			wrld.cycles_visibility.camera = camera
			wrld.cycles_visibility.diffuse = diffuse
			wrld.cycles_visibility.glossy = glossy
			wrld.cycles_visibility.transmission = transmission
			wrld.cycles_visibility.scatter = scatter


def MTswap(Material_Label, Texture_Quality, packFile = False):
	"""
	Material_Label takes a string or a list of material names.
	Texture_Quality takes a string to for texture quality, must be named identical to folder

	This function allows you to change the texture quality of a material/s without having to run through texture swapper

	"""
	bdm = data.materials
	ops.file.make_paths_absolute()
	matList = []


	if type(Material_Label) == str:

		for mat in bdm:

			if Material_Label in mat.name:
				StatusPrint('Found %s' % (mat.name))
				matList.append(mat.name)
				tNodes = []

				for node in mat.node_tree.nodes:

					if "Image Texture" in node.name:
						cTextureFile = node.image.filepath
						tNodes.append(node.name)

						if cTextureFile.split("\\")[-2] != Texture_Quality:
							
							StatusPrint('Unpacking texture!!')
							node.image.unpack()
							cTexture = cTextureFile.split("\\")[-2]
							newTextureFile = cTextureFile.replace(cTexture, Texture_Quality)
							StatusPrint(newTextureFile)
							newTextureFile = newTextureFile.replace(newTextureFile.split('\\')[0], 'G:')
							node.image.filepath = newTextureFile
							StatusPrint('%s, %s, Changing Quality of texture from %s to %s' % (mat.name, node.image.name, cTexture, Texture_Quality))
							StatusPrint('Old Texture filepath: %s, \n New Texture filepath: %s' % (cTextureFile, newTextureFile))

							if packFile == True:
								try:
									node.image.pack()
								except Exception as e:
									StatusPrint(e)
								

						else:
							StatusPrint('%s, %s, Texute quality is already %s' % (mat.name, node.image.name, Texture_Quality))

					elif not tNodes:
						StatusPrint("%s Node, is not a Texture node found in %s " % (node.name, mat.name) + "!!")

		if not matList:
			StatusPrint(Material_Label + " not found in blend file!!")
			return False
		else:
			return True

	elif type(Material_Label) == list:

		for mat in bdm:

			for material in Material_Label:

				if material in mat.name:
					StatusPrint('Found %s' % (mat.name))
					matList.append(mat.name)
					tNodes = []

					for node in mat.node_tree.nodes:

						if "Image Texture" in node.name:
							tNodes.append(node.name)
							cTextureFile = node.image.filepath

							if cTextureFile.split("\\")[-2] != Texture_Quality:
								StatusPrint('Unpacking texture!!')
								node.image.unpack()
								cTexture = cTextureFile.split("\\")[-2]
								newTextureFile = cTextureFile.replace(cTexture, Texture_Quality)
								StatusPrint(newTextureFile)
								newTextureFile = newTextureFile.replace(newTextureFile.split('\\')[0], 'G:')
								node.image.filepath = newTextureFile
								StatusPrint('%s, %s, Changing Quality of textures from %s to %s' % (mat.name, node.name, cTexture, Texture_Quality))
								StatusPrint('Old Texture filepath: %s, \n New Texture filepath: %s' % (cTextureFile, newTextureFile))

								if packFile == True:
									node.image.pack()

							else:
								StatusPrint('%s, %s, Texute quality is already %s' % (mat.name, node.name, Texture_Quality))

						elif not tNodes:
							StatusPrint("Node %s, is not a Texture node found in " + str(node.name, mat.name) + "!!")

			if not matList:
				StatusPrint(Material_Label + " not found in blend file!!")
				return False
			else:
				return True


def LightAdjust(emptyName, sEmpty = False, **kwargs):
	"""
	This only adjust lamp objects, this does not adjust objects with emission nodes on them

	implementation coming soon
	"""
	for emty in data.objects:
		if emty.type == "EMPTY":
			if emptyName in emty.name:
				for lamp in emty.children:
					if lamp.type == "LAMP":
						for key, value in kwargs.items():
							if key in lamp.name:
								lamp.data.node_tree.nodes['Emission'].inputs[1].default_value = value
								StatusPrint("Adjusting %s to %f" % (key, value))
							else:
								StatusPrint("Could NOT find %s in blend file" % (key))
		else:
			for lamp in data.objects:
				if lamp.type == "LAMP":
					for key, value in kwargs.items():
						if key in lamp.name:
							lamp.data.node_tree.nodes['Emission'].inputs[1].default_value = value
							StatusPrint("Adjusting %s to %f" % (key, value))
						else:
							StatusPrint("Could NOT find %s in blend file" % (key))


def RenderLayers(SceneName = 'Scene', **kwargs):
	"""
	Example of how kwargs works:
	kwargs = {"RenderLayer1" : False, "RenderLayer2": True}

	This function allows you to turn on and off specified render layers.
	"""
	rlayers = data.scenes[SceneName].render.layers
	bScriptRan = False
	bAlreadyDone = False

	for layers in rlayers:
		for key, value in kwargs.items():
			if key in layers.name:
				StatusPrint("Found %s Render Layer! \n" % (key))
				if layers.use == value:
					bAlreadyDone = True
					bScriptRan = True
					StatusPrint("%s Render Layer is already %s \n" % (key, value))
					StatusPrint("Continuing with next Asset! \n")
				else:
					layers.use = value
					bScriptRan = True
					StatusPrint("Setting %s Render Layer to %s! \n" % (key, value))
	if bScriptRan == True and bAlreadyDone == False:
		bpy.ops.wm.save_mainfile(relative_remap = False)
		bScriptRan = False
		bAlreadyDone = False
	elif bScriptRan == True and bAlreadyDone == True:
		StatusPrint("\n Blend file is good, don't need to run script \n")
		bScriptRan = False
		bAlreadyDone = False
	elif bScriptRan == False and bAlreadyDone == False:
		StatusPrint("\n Script did NOT run \n")


def createObjFromOperator(name, objType, origin = (0, 0, 0)):
	"""
	Types of objs that can be created:
	['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'CAMERA', 'LAMP', 'SPEAKER']

	# This is an example on how to use this function
	createObjFromOperator('Scene', 'EMPTY')  ## this piece creates the obj
	empty_scene = bpy.context.object  ## this piece of code capsulates that obj into a variable, so you can use it elsewhere

	"""
	bpy.ops.object.add(
		type=objType, 
		enter_editmode=False,
		location=origin,
		layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
	ob = bpy.context.object
	ob.name = name


def RenderSettings(res_x = None, res_y = None, res_percent = None, color_depth = None, color_mode = None,
	compression = None, render_samples = None, samples_type = None, clamp_dir = None, clamp_indir = None,
	caustics_reflect = None, caustics_refract = None, filter_glossy = None, film_trans = None, filter_width = None, file_format = None):
	"""
	You don't need to change every setting in this function for it to work, just change the setting that you
	want to adjust.

	res_x = Takes integers

	res_y = Takes integers

	res_percent = Takes integers

	color_depth = Only take '8' or '16', include the quotes

	color_mode = Takes only these values ('BW', 'RGB', 'RGBA')

	compression = Anything from 0 to 100 

	render_samples = Any number you want just don't be ridiculous

	samples_type = has two options, BRANCHED_PATH' and 'PATH'

	clamp_dir = Takes any float

	clamp_indir = Takes any float

	caustics_reflect = True or False

	caustics_refract = True or False

	filter_glossy = Takes any float, keep this number pretty low

	film_trans = True or False

	"""
	#initilize variables
	S = bpy.context.scene

	print('''Adjusting Render Setting to the following settings:\n
			RES_X: %s,
			RES_Y: %s,
			RES_PERCENT: %s,
			COLOR_DEPTH: %s,
			COLOR_MODE: %s,
			COMPRESSION: %s,
			RENDER_SAMPLES: %s,
			SAMPLES_TYPE: %s,
			CLAMP_DIR: %s,
			CLAMP_INDIR: %s,
			CAUSTICS_REFLECT: %s,
			CAUSTICS_REFRACT: %s,
			FILTER_GLOSSY: %s,
			FILM_TRANS: %s,
			FILTER_WIDTH: %s,
			FILE_FORMAT: %s
			''' 
			%(str(res_x),
			str(res_y),
			str(res_percent),
			str(color_depth),
			str(color_mode),
			str(compression),
			str(render_samples),
			str(samples_type),
			str(clamp_dir),
			str(clamp_indir),
			str(caustics_reflect),
			str(caustics_refract),
			str(filter_glossy),
			str(film_trans),
			str(filter_width),
			str(file_format)))
	
	# set res_x
	if res_x:
		S.render.resolution_x = res_x
	else:
		res_x = S.render.resolution_x
	
	# set res_y
	if res_y:
		S.render.resolution_y = res_y
	else:
		res_y = S.render.resolution_y
	
	# set res_percent
	if res_percent:
		S.render.resolution_percentage = res_percent
	else:
		res_percent = S.render.resolution_percentage

	# set color_depth
	if color_depth:
		S.render.image_settings.color_depth = color_depth
	else:
		color_depth = S.render.image_settings.color_depth
	
	# set color_mode
	if color_mode:
		S.render.image_settings.color_mode = color_mode
	else:
		color_mode = S.render.image_settings.color_mode
	
	# set compression
	if compression:
		S.render.image_settings.compression = compression
	else:
		compression = S.render.image_settings.compression

	# set render_samples
	if render_samples:
		S.cycles.samples = render_samples
	else:
		render_samples = S.cycles.samples

	# set samples_type
	if samples_type:
		S.cycles.progressive = samples_type
	else:
		samples_type = S.cycles.progressive

	# set clamp_dir
	if clamp_dir:
		S.cycles.sample_clamp_direct = clamp_dir
	else:
		clamp_dir = S.cycles.sample_clamp_direct

	# set clamp_indir
	if clamp_indir:
		S.cycles.sample_clamp_indirect = clamp_indir
	else:
		clamp_indir = S.cycles.sample_clamp_indirect

	# set caustics_reflect
	if caustics_reflect:
		S.cycles.caustics_reflective = caustics_reflect
	else:
		caustics_reflect = S.cycles.caustics_reflective

	# set caustics_refract
	if caustics_refract:
		S.cycles.caustics_refractive = caustics_refract
	else:
		caustics_refract = S.cycles.caustics_refractive

	# set filter_glossy
	if filter_glossy:
		S.cycles.blur_glossy = filter_glossy
	else:
		filter_glossy = S.cycles.blur_glossy

	# set film_trans
	if film_trans:
		S.cycles.film_transparent = film_trans
	else:
		film_trans = S.cycles.film_transparent

	# set filter_width
	if filter_width:
		S.cycles.filter_width = filter_width
	else:
		filter_width = S.cycles.filter_width

	# set film_trans
	if file_format:
		S.render.image_settings.file_format = file_format
	else:
		file_format = S.render.image_settings.file_format


def parentObjsTo(parent, child):
	"""
	child takes single objects and a list of objects, it can an empty that has children that you want nested under
	the parent.

	this script will check the type of object and make the appropriate parenting
	"""

	bObjs = bpy.data.objects

	for obj in bObjs:
		if parent in obj.name:
			obj.hide = False ## unhide the object if it is hidden
			parent = obj
			StatusPrint("Found %s" % (parent.name))
			if type(child) == list:
				StatusPrint("Looping through child list")
				for chld in child:	## loops through the child list
					if chld in obj.name:	## if an instance of child matches the object name, then continue to next line
						StatusPrint("Found %s, selecting %s" % (chld, obj.name))
						obj.hide = False ## unhide the object if it is hidden
						obj.select = True ## selects child
			else:
				if child in obj.name:
					StatusPrint("Found %s, selecting %s" % (child, obj.name))
					obj.hide = False ## unhide the object if it is hidden
					obj.select = True
			parent.select = True
			bpy.context.scene.objects.active = parent
			StatusPrint("Parenting child objects to %s" % (parent.name))
			bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
		else:
			StatusPrint("Can't find %s in blend file" % (parent))

def selectMaterial(mat_search_key):
	"""
	This function returns the material instance that matches the mat_search_key.
	"""
	mat_search_key = mat_search_key
	for mat in D.materials:
		if mat_search_key.lower() in mat.name.lower():
			print("Found %s" %mat.name)
			return mat
		elif mat_search_key.lower() in mat.name.lower():
			print("Found %s" %mat.name)
			return mat
		elif mat_search_key.lower() in mat.type.lower():
			print("Found %s" %mat.name)
			return mat
		elif mat.type.lower() in mat_search_key.lower():
			print("Found %s" %mat.name)
			return mat
		else:
			print("%s did not match any material.name or material.type in the scene." %(mat_search_key))


def selectNode(node_search_key, material):
	"""
	This function returns the node instance that matches the mat_search_key.
	"""
	node_search_key=node_search_key
	if not material.use_nodes: material.use_nodes = True
	for node in material.node_tree.nodes:
		if node.name.lower() in node_search_key.lower():
			print("Found %s" %node.name)
			return node
		elif node_search_key.lower() in node.name.lower():
			print("Found %s" %node.name)
			return node
		elif node_search_key.lower() in node.type.lower():
			print("Found %s" %node.name)
			return node
		elif node.type.lower() in node_search_key.lower():
			print("Found %s" %node.name)
			return node
		else:
			print("%s did not match any node.name or node.type in the scene." %(node_search_key))

def adjustMapNode(x,y,mapping,node):
	"""
	This function adjust the rotation or scale of a mapping node on a specified material
	"""
	# x = float(x)
	# y= float(y)
	if mapping in ('scale','Scale','s'):
		print("Adjusting %s, to x:%f, y:%f" %(node,x,y))
		node.scale[0] = x
		node.scale[1] = y
		
	elif mapping in ('rotation', 'Rotation','r'):
		print("Adjusting %s, to x:%i*, y:%i*" %(node,x,y))
		node.rotation[0] = math.radians(x)
		node.rotation[1] = math.radians(y)
		
	else:
		print("Mapping type did not match possible choices ('scale, 'Scale', 'rotation', 'Rotation').")
		


@persistent
def do_render_opengl(outputFilePath, animation=False):
	"""
	This function can't be run in the background!
	You will need to change one thing in BlenderBatchRun.py

	comment out the old subprocess.call and add this one underneath:

	subprocess.call(['call', BLENDER_EXE_PATH, blend_filepath, '-P', custom_py_path], shell=True) 

	## This process DOES NOT run in background ##
	"""
	# get the scene
	S = bpy.context.scene

	# set image output format
	S.render.image_settings.file_format = 'PNG'

	# get blend data
	data = bpy.data

	# get blend name
	bname = data.filepath.split('.blend')[0].split('\\')[-1]

	#set render output
	if outputFilePath:
		S.render.filepath = os.path.join(
			outputFilePath,
			bname + '_001')
	else:
		S.render.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OpenGL Renders" ,bname, bname + '_001')

	#set render frame
	S.frame_set(1)

	bpy.ops.render.opengl(animation, view_context=False, write_still=True)
	bpy.ops.wm.quit_blender()

def do_main_opengl(outputFilePath, animation=False):
	"""
	This function goes hand in hand with do_render_opengl,
	you need this function to run the once above.

	You must also provide an output path, this is where your render will export out to.
	"""
	bpy.app.handlers.load_post.append(do_render_opengl(outputFilePath, animation))


def modifierAdd(mesh, modifier, name, **kwargs):
	"""
	This function allows you to add a multitude of modifiers to objects of your choise,
	you can also choose to apply these modifiers.

	Types of modifiers you can add:
	['DATA_TRANSFER', 'MESH_CACHE', 'NORMAL_EDIT', 'UV_PROJECT', 'UV_WARP', 'VERTEX_WEIGHT_EDIT', 
	'VERTEX_WEIGHT_MIX', 'VERTEX_WEIGHT_PROXIMITY', 'ARRAY', 'BEVEL', 'BOOLEAN', 'BUILD', 'DECIMATE', 
	'EDGE_SPLIT', 'MASK', 'MIRROR', 'MULTIRES', 'REMESH', 'SCREW', 'SKIN', 'SOLIDIFY', 'SUBSURF', 
	'TRIANGULATE', 'WIREFRAME', 'ARMATURE', 'CAST', 'CORRECTIVE_SMOOTH', 'CURVE', 'DISPLACE', 'HOOK', 
	'LAPLACIANSMOOTH', 'LAPLACIANDEFORM', 'LATTICE', 'MESH_DEFORM', 'SHRINKWRAP', 'SIMPLE_DEFORM', 
	'SMOOTH', 'WARP', 'WAVE', 'CLOTH', 'COLLISION', 'DYNAMIC_PAINT', 'EXPLODE', 'FLUID_SIMULATION', 
	'OCEAN', 'PARTICLE_INSTANCE', 'PARTICLE_SYSTEM', 'SMOKE', 'SOFT_BODY', 'SURFACE']

	NEEDS IMPLEMENTATION
	"""
	bO = bpy.data.objects

	for obj in bO:
		if mesh in obj.name:
			# get the object
			mesh = obj
			## adds a new modifier to the object and captures that modifier to the var
			mod = mesh.modifiers.new(name, modifier.upper())
			for key, value in kwargs.items():
				mod.key = value


def assignFromAssetM(mesh, libType, lib, cat, mat):
	"""
	Assign a material to an object or children nested under empties from Asset Manager!

	mesh can be a single object, a list of objects, or a list of objects with a mix of empties
	"""

	##### initilize global vars ######

	# get windows manager
	winMan = bpy.data.window_managers["WinMan"]
	# get all objects
	bO = bpy.data.objects


	winMan.asset_m.library_type = libType
	winMan.asset_m.libraries = lib
	winMan.asset_m.categories = cat
	winMan.AssetM_previews = (mat + ".png")

	bpy.ops.object.select_all(action='DESELECT')
	for obj in bO:
		if type(mesh) == str:
			pass
		elif type(mesh) == list:
			pass
			

def ShadowBlendCleanUp():
	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			for space in area.spaces:
				if space.type == 'VIEW_3D':
					space.show_only_render = False
					print("-" * 20)
					print("Show Render Only is False")
					print("-" * 20)
	AName = str(bpy.data.filepath.split("\\")[-1])
	AName = str(AName.split("_")[0])
	bpy.ops.object.showrenderable()
	for emty in bpy.data.objects:
		if emty.type == "EMPTY":
			bpy.ops.object.select_all(action='DESELECT')
			if "Geometry" in emty.name:
				if len(emty.children) != 1:
					for child in emty.children:
						if "scene" in child.name:
							bpy.ops.object.select_all(action='DESELECT')
							child.select = True
							bpy.context.scene.objects.active = child
							bpy.ops.object.delete()
			if "Animated" in emty.name:
				emty.hide = False
				emty.select = True
				if len(emty.children): # checks if emty has atleast 1 child, len of 0 results in false
					for child in emty.children: 
						child.hide = False
						child.select = True
						bpy.context.scene.objects.active = child
						bpy.ops.object.delete()
				else:
					continue
			if AName in emty.name:
				emty.select = True
				bpy.context.scene.objects.active = emty
				for child in emty.children:
					child.hide = False
					child.select = True
					bpy.context.scene.objects.active = child
					for sib in child.children:
						sib.hide = False
						sib.select = True
						bpy.context.scene.objects.active = sib
						bpy.ops.object.move_to_layer(layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


def CheckBlendSetup(log_filepath = None):
	"""
	************************************************************************************************
	**************** Check CT Blendfile Set-up *****************************************************
	************************************************************************************************
	"""
	context = bpy.context
	S = context.scene # Get the scene
	obs = S.objects # All the objects in the scene

	"""
	Checks Outliner against a list and prints out the empties that match the list

	"""
	emptyList = []
	
	# if emptyList is not assigned use default emptyList
	if not emptyList:
		emptyList = ['360Scene','Geometry','Scene','Animation','CameraPoint','Lights','Frame','Cushions','Pillows','Legs',
		'Nailheads','Stitching','BedPillows','Wild1','Wild2','BrassTips','Piping','Metal','PillowPiping']

	if not log_filepath:
		log_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BlenderBatchActions_log.txt')


	with open(log_filepath, 'a') as f:
		SObjs = [o for o in obs if o.name.split('_')[0].split('.')[0] in emptyList]
		f.write(('*' * 150)+'\n'+('*' * 50)+ ('		') + bpy.data.filepath.split('\\')[-1]+ ('		')+('*' * 50)+'\n'+('*' * 150)+'\n'+'\n' )
		f.write(str('\n' + 'BLENDFILE : ' + bpy.data.filepath + '\n').upper())

		f.write('\n' + 
			'*' * 50 + 
			' LIST OF EMPTIES THAT MATCH emptyList ' + 
			'*' * 50 + '\n')
		print('\n')
		print('*' * 50)
		print('List of Empties that match emptyList')
		print('*' * 50)
		for obj in SObjs:
			if obj.type == "EMPTY":
				print(obj.name)
				f.write(obj.name + '\n')
			
			
		"""
		Prints a list of parent and child groupings

		"""
		f.write('\n' + 
			'*' * 50 + 
			' OUTLINER HIERARCHY ' + 
			'*' * 50 + '\n')
		print('\n')
		print('*' * 50)
		print('Outliner Hierarchy')
		print('*' * 50)


		# Select objects in scene that have no parent, and objects that have children
		objs = [o for o in obs if not o.parent or len(o.children)] 
		for o in objs:
			if not o.parent:
				print('Scene Parent Object is: %s' % (o.name))
				f.write('Scene Parent Object is: %s' % (o.name) + '\n')

				for child in o.children:
					print(' ' + child.name)
					f.write(' ' + child.name + '\n')

					if len(child.children):
						for c in child.children:
							print('	 ' + c.name)
							f.write('	 ' + c.name + '\n')

							if len(c.children):
								for gc in c.children:
									print('		 ' + gc.name)
									f.write('		 ' + gc.name + '\n')

									if len(gc.children):
										for ggc in gc.children:
											print('			 ' + ggc.name)
											f.write('			 ' + ggc.name + ' : ' + 'PASS ID: ' + str(ggc.pass_index)+ '\n')
		
		# Runs through the materials in the scene
		mats = bpy.data.materials # Selects all the materials in the scene
		matList = []
		matTextures = []
		for m in mats:
			if m.name not in matList:
				matList.append(m.name)
				#print(m.name)
				nodes = m.node_tree.nodes
				for node in nodes:
					if 'Image' in node.name:
						matTextures.append('%s || TEXTURE: %s' % (m.name, node.image.name))
						#print('Mat: %s, Texture: %s' % (m.name, node.image.name))
						#print('Mat: %s, has not texure nodes' % (m.name))
		f.write('\n' + '*' * 50 + ' MATERIALS IN SCENE ' + '*' * 50 + '\n')
		for mat in matList:
			f.write(' ' + mat + '\n')
		f.write('\n' + '*' * 50 + ' MATERIALS WITH TEXTURES ' + '*' * 50 + '\n')
		for mat in matTextures:
			f.write(' ' + mat + '\n')
		f.write('\n' + ('*'*100)+ '\n' + ('*'*100)+ '\n'+'\n'+'\n'+'\n')
	f.close()


def ClearAnimatedLights():

	'''
	*******************************************************************************
	****************** REMOVES GROUND LIGHTS FROM IMAGER SCENES *******************
	*******************************************************************************

	'''

	bdo = bpy.data.objects
	l = []

	for emty in bdo:
		if emty.type == 'EMPTY':
			bpy.ops.object.select_all(action='DESELECT')
			if "Animated" in emty.name:
				emty.hide = False
				emty.select = True
				l.append(emty.name)
				if len(emty.children): # checks if emty has atleast 1 child, len of 0 results in false
					for child in emty.children: 
						child.hide = False
						child.select = True
						bpy.context.scene.objects.active = child
						l.append(child.name)
						bpy.ops.object.delete()
	if l:
		bpy.ops.wm.save_mainfile(relative_remap = False)
		return True
	else:
		return False


def select_object_and_all_descendants(scene, obj):
	scene.objects[obj.name].select = True
	for child_obj in obj.children:
		select_object_and_all_descendants(scene, child_obj)


def link_object_and_all_descendants(scene, obj):
	# print('linking object {}'.format(obj.name))
	scene.objects.link(obj)
	# print("object's children: {}".format(obj.children))
	for child_obj in obj.children:
		link_object_and_all_descendants(scene, child_obj)


def makeLocal_object_and_all_descendants(scene, obj, type ='SELECT_OBDATA'):
	select_object_and_all_descendants(scene, obj)
	bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')


def ImportAssetFromBlend(asset_dir, blend_dir):
	# Blender Data
	bd = bpy.data

	# All objects in current scene
	bdo = bd.objects

	# current scene
	S = bpy.context.scene

	# Get Geometry Empty
	geom_empty = [o for o in S.objects if o.name.startswith('Geometry')]
	geom_empty = geom_empty[0]
	#print(geom_empty)

	# name of object(s) to append or link
	#obj_name = "Hathaway_Slip_Swivel_Glider"
	obj_name = bd.filepath.split('\\')[-1]
	obj_name = obj_name.split('-')[0]
	print(obj_name)


	# Asset Dir
	asset_dir = r'G:\CrateAndBarrel\Assets'

	# Blend Dir
	blend_dir = r'Silho\_Imager'

	# path to the blend
	#filepath = r"G:\CrateAndBarrel\Assets\Hathaway_Slip_Swivel_Glider\Silho\_Imager\Hathaway_Slip_Swivel_Glider_Anim.blend"
	filepath = (asset_dir + '\\' + obj_name + '\\' + blend_dir + '\\' + obj_name + "_Anim.blend")

	# Remove existing Asset
	'''
	for child in geom_empty.children:
		if obj_name in child.name:
			select_object_and_all_descendants(S, child)
			bpy.ops.object.delete()
	'''

	# append, set to true to keep the link to the original file
	link = True

	# link all objects starting with 'Cube'
	with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
		#data_to.objects = [name for name in data_from.objects if name.startswith(obj_name)]
		#data_to.scenes = data_from.scenes
		data_to.objects = data_from.objects
		#print(data_to.objects)
		print(data_to.scenes)
		
	for obj in data_to.objects:
			if obj:
				if obj_name in obj.name:
					print(obj)
					link_object_and_all_descendants(S, obj)
					bbc.StatusPrint('Linking %s to scene' % (obj.name))
					obj.parent = geom_empty
					bpy.ops.object.select_all(action='DESELECT')
					makeLocal_object_and_all_descendants(S, obj)
					bbc.StatusPrint('Making %s local' % (obj.name))


def ImportObjFromBlend(blend_dir, ObjMesh, parent = None, del_old = False):
	# Blender Data
	bd = bpy.data

	# All objects in current scene
	bdo = bd.objects

	# current scene
	S = bpy.context.scene

	# Get Geometry Empty
	if parent:
		parent_empty = [o for o in S.objects if o.name.startswith(parent)]
		parent_empty = parent_empty[0]
		print(parent_empty)

	filepath = (blend_dir)

	# Remove Old existing Asset
	if del_old:
		bpy.ops.object.select_all(action='DESELECT')
		Mesh = [o for o in S.objects if o.name.startswith(ObjMesh)] ## Filter through scene and grab ObjMesh
		print(Mesh)
		Mesh = [o for o in Mesh if ObjMesh == o.name]
		Mesh = Mesh[0]
		bbc.StatusPrint("Deleting Old Geo, %s" % [Mesh.name])
		select_object_and_all_descendants(S, Mesh)
		bpy.ops.object.delete()
	
	# append, set to true to keep the link to the original file
	link = True

	# link all objects starting with 'Cube'
	with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
		#data_to.objects = [name for name in data_from.objects if name.startswith(obj_name)]
		#data_to.scenes = data_from.scenes
		data_to.objects = data_from.objects
		#print(data_to.objects)
		print(data_to.scenes)

	# Get ObjMesh
	Mesh = [o for o in data_to.objects if o.name.startswith(ObjMesh)]
	print(Mesh)
	Mesh = [o for o in Mesh if ObjMesh == o.name]
	print("Mesh variable contains %s" % Mesh)
	Mesh = Mesh[0]
		
	link_object_and_all_descendants(S, Mesh)
	bbc.StatusPrint('Linking %s to scene' % (Mesh.name))
	bbc.StatusPrint('Parenting %s to %s' % (Mesh.name, parent_empty.name))
	Mesh.parent = parent_empty
	bpy.ops.object.select_all(action='DESELECT')
	makeLocal_object_and_all_descendants(S, Mesh)
	bbc.StatusPrint('Making %s local' % (Mesh.name))


def CleanUpBlend(Delete_Objs_Not_Rendered = False, MATERIAL_FEEDBACK = False):
	"""
	Cleans up blend file of any objects that are not being rendered and any empty that has no children.

	"""

	con = bpy.context
	S = con.scene
	data = bpy.data
	objs = data.objects

	# Delete_Objs_Not_Rendered = False

	bpy.ops.object.select_all(action='DESELECT')
	for obj in objs:
		# Deletes Any Object that is not being rendered
		if Delete_Objs_Not_Rendered:
			if obj.hide_render:
				if obj.hide_select:
					obj.hide_select = False
					obj.select = True
					bpy.ops.object.delete()
				else:
					obj.select = True
					bpy.ops.object.delete()
					
		# Deletes Unused Empties, Empties without any children
		if obj.type == "EMPTY":
			if not obj.children:
				obj.hide_select = False
				obj.select = True
				bpy.ops.object.delete()

	if MATERIAL_FEEDBACK:
		bpy.ops.material.feedback()
		bpy.ops.texture.clear_unused_images()
		bpy.ops.wm.save_mainfile(relative_remap = False)

def hdr_adjust(hdr_strength, node_name):
	print("Adjusting HDR..")
	# hdr_strength = hdr_strength

	for world in D.worlds:
		for node in world.node_tree.nodes:
			if node.name == 'Background':
				print(node.name)
				node.inputs[1].default_value = hdr_strength



def light_strength_adjustment(light_strength, light_name = None, light_visible = None):
	#Deselects all objects in the scene
	O.object.select_all(action='DESELECT')

	#Argument assignment
	l_name = light_name
	l_str = light_strength
	l_visible = light_visible

	#Searching for the Lights empty
	for empty in D.objects:
		if empty.type == "EMPTY":
			#Selects the Lights empty and avoids the Ground Lights
			if "Lights" in empty.name and "Rotating" not in empty.name:

				#if LIGHT_ADJUSTEMTNS IS not empty
				if l_str == 0:
					#Loop through Lights
					for child in empty.children:
						#Selects the light object and hides from render view
						child.select = True
						print("Hiding %s from Render View" %child.name)
						child.hide_render = True
						child.hide = True

						#Access Light Object Data
						lamp = child.data
						lamp_emission = lamp.node_tree.nodes['Emission']
						#Replace lamp strength
						lamp_strength = lamp_emission.inputs['Strength'].default_value
						lamp_strength = l_str
						print("%s =  STR: %i, Hidden: %s" %(lamp.name, lamp_strength, child.hide_render))

						#Deselect Light
						# child.select = False

				elif l_str > 0:
					#Loop through Lights
					for child in empty.children:
						#Selects the light object and hides from render view
						child.select = True
						#Access Light Object Data
						lamp = child.data
						lamp_emission = lamp.node_tree.nodes['Emission']
						#Replace lamp strength
						lamp_emission.inputs['Strength'].default_value = l_str

						#Deselect Light
						child.select = False

				else:
					#UNFINISHED
					continue

def texture_swapper(texture_dir, material_key_list, texture_key_list, texture_map_list = ['color', 'spec', 'bump']):
	mat_list = [m.lower() for m in material_key_list]
	tex_list = [m.lower() for m in texture_key_list]
	t_dir = texture_dir

	for mat in D.materials:
		if mat.name in mat_list:
			# Change image node, image filepath
			for node in mat.node_tree.nodes:
				if "Image Texture" in node.name:
					for m in texture_map_list:
						if m in node.image.name:
							t_path = node.image.filepath
							# t_path = 
						node.image.filepath = t_path
						print(node.image.filepath)
						node.image.pack()


def Save_to_MSwap(skip_if_exists = True):
	SKIP_IF_ALREADY_EXIST = skip_if_exists

	save_path = os.path.join(bpy.data.filepath.rsplit('\\', 1)[0], 'MSwap')
	asset_blend = bpy.data.filepath.split('\\', 4)[3] + "_AnimS.blend"
	save_as_path = os.path.join(save_path, asset_blend)

	if not os.path.isdir(save_path):
		os.mkdir(save_path)

	if SKIP_IF_ALREADY_EXIST and os.path.exists(save_as_path):
		print("MSwap exists!   Skipping saving asset...")
		print(save_as_path)

	else:
		O.wm.save_mainfile(filepath = save_as_path, relative_remap = False)

		print("AnimS: ",asset_blend)
		print("Saving to MSwap...")


"""
	Below here lies the incompleted methods:
"""

def Comp_FileOutput(file_output):
	print (hello)



#=====================================================
def save():
	O.wm.save_mainfile()

