import viz
import vizinfo
import vizproximity
import viztask
import vizshape
import vizfx
import vizact
import vizmat
import vizcam
import time
import os.path
from random import shuffle

savepath = "C:\Users\Cyan\Documents\\"
subjid = raw_input("Enter participant ID: ")
flname = savepath + "test_subj" + subjid + ".txt"
results = open(flname, "a")
asset_dir = "C:\Users\Cyan\Documents\Viz_envmts\Thesis-Navigation\Navigation-Experiment\\"
global t0, trial_cond

#set graphic parameters
viz.setMultiSample(4)
viz.fov(80)

# Add collision
viz.collision(viz.ON)

#load textures
stone = viz.addTexture("images/tile_stone.jpg", wrap=viz.REPEAT)
tile = viz.addTexture("images/tile_slate.jpg", wrap=viz.REPEAT)
metal = viz.addTexture("metal.jpg", wrap=viz.REPEAT)
lava = viz.addTexture("lava.png", wrap=viz.REPEAT)

# Add white point light 
# light = vizfx.addPointLight(color=viz.WHITE, pos=(0,1,1))

def getData(choice, finish_time):
	global results, trial_cond
	print "\n" + trial_cond + "," + choice + "," + str(finish_time)
	results.write("\n" + trial_cond + "," + choice + "," + str(finish_time))
		
		
def loadBaseScene():
	"""Set up the scene for width, friction and texture conditions"""
	starting_pos = [-20, 2, 0]
	# Add ground
	ground = viz.addChild('ground.osgb')
	ground.texture(lava)
	ground.setScale(1.5,0,1.5)

	# Computer game controls
	viz.cam.setHandler(vizcam.KeyboardCamera(forward='w',backward='s', left='a',right='d',turnRight='e',turnLeft='q'))
	view = viz.MainView
	def mousemove(e):
		euler = view.get(viz.HEAD_EULER)
		euler[0] += e.dx*0.1
		euler[1] += -e.dy*0.1
		euler[1] = viz.clamp(euler[1],-90.0,90.0)
		euler[2] = 0
		view.setEuler(euler,viz.HEAD_ORI)
	viz.callback(viz.MOUSE_MOVE_EVENT,mousemove)

	viz.MainView.setPosition(starting_pos)
	viz.MainView.setEuler(90,0,0)

	global plankl, plankr

	# Room setup

	# Main areas: R, L, back wall and ceiling, respectively
	wall_r = vizshape.addPlane([75, 30])
	wall_r.setPosition(10,0,-35)
	wall_r.setEuler(x=0, y=90, z=0)
	wall_r.texture(metal)
	wall_l = vizshape.addPlane([75,30])
	wall_l.setPosition(10,0,35)
	wall_l.setEuler(x=0, y=-90, z=0)
	wall_l.texture(metal)
	wall_b = vizshape.addPlane([75, 30])
	wall_b.setPosition(-22.25, 0, 0)
	wall_b.setEuler(x=90, y=90, z=0)
	wall_b.texture(metal)
	ceiling = vizshape.addPlane([75,75])
	ceiling.setEuler(0, 180, 0)
	ceiling.setPosition(15,10, 0)
	ceiling.texture(metal)
	
	# Texture matrix for small walls on L and R of doors
	tex_mwall_tlr = vizmat.Transform()
	tex_mwall_tlr.setScale([1*0.35,2.5*0.4,1*0.35])

	# Texture matrix for centre wall between doors
	tex_mwall_tc = vizmat.Transform()
	tex_mwall_tc.setScale([1,1,1.3])

	# Texture wrapping mode
	tile.wrap(viz.WRAP_T, viz.REPEAT)
	tile.wrap(viz.WRAP_S, viz.REPEAT)

	# Floor/wall in the target area
	wall_tf = vizshape.addBox([25,0.5,75])
	wall_tf.setPosition(25,0,0)
	
	# Landing area in front of the doors
	floor_l = vizshape.addBox([8,0.5,8])
	floor_l.setEuler(45,0,0)
	floor_l.setPosition(11,0,33.25)
	floor_r = vizshape.addBox([8,0.5,8])
	floor_r.setEuler(45,0,0)
	floor_r.setPosition(11,0,-33.25)
	
	# Top wall in target area
	wall_tt = vizshape.addBox([25,6,75])
	wall_tt.setEuler(0,0,0)
	wall_tt.setPosition(25,7,0)
	wall_tt.texture(metal)
	
	# Target area, left wall
	wall_tl = vizshape.addBox([0.25,7.5,3])
	wall_tl.setEuler(0,0,0)
	wall_tl.setPosition(12.75,0.5,33.75)
	wall_tl.texmat(tex_mwall_tlr)
	wall_tl.texture(tile)
	
	# Target area, right wall
	wall_tr = vizshape.addBox([0.25,7.5,3])
	wall_tr.setEuler(0,0,0)
	wall_tr.setPosition(12.75,0.5,-33.75)	
	wall_tr.texmat(tex_mwall_tlr)
	wall_tr.texture(tile)
	
	# Texture wrap mode
	tile.wrap(viz.WRAP_T, viz.REPEAT)
	tile.wrap(viz.WRAP_S, viz.REPEAT)
	
	# Centre wall on target area
	wall_tc = vizshape.addBox([0.25,7.5,60.5])
	wall_tc.setEuler(0,0,0)
	wall_tc.setPosition(12.75,0.5,0.0)
	wall_tc.texmat(tex_mwall_tc)
	wall_tc.texture(tile)
	
	# Back wall of target area (only visible on entering)
	wall_tb = vizshape.addPlane([75,4])
	wall_tb.setPosition(35, 2, 0)
	wall_tb.setEuler(x=90, y=270, z=0)
	
def loadTextureConditions(tex):
	"""Set up paths for a texture condition trial.
	@args:
		tex (int): the parameter determining the exact condition
		for this trial.

	"""
	global door_l, door_r
	
	# Left and right doors, respectively
	door_l = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_l.setEuler(90,0,0)
	door_l.setPosition(12.5,2.0,29.75)
	door_r = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_r.setEuler(90,0,0)
	door_r.setPosition(12.5,2.0,-32.5)

	# Change the origin and where door will rotate
	door_l.center(0.5,0,0)
	door_r.center(0.5,0,0)
	
	# Make paths
	model_plankl = "p_mid_"
	model_plankr = "p_mid_"
	
	'''
	# Texture conditions
	0. Lrubber, Rstone
	1. Lstone, Rrubber
	2. Lrubber, Rgravel
	3. Lgravel, Rrubber
	4. Lstone, Rgravel
	5. Lgravel, Rstone
	
	'''
	if (tex == 0) or (tex == 2):
		model_plankl = model_plankl + "rubber"
	elif (tex == 1) or (tex == 4) or (tex == 6):
		model_plankl = model_plankl + "stone"
	elif (tex == 3) or (tex == 5):
		model_plankl = model_plankl + "gravel"
		
	if (tex == 0) or (tex == 5) or (tex == 6):
		model_plankr = model_plankr + "stone"
	elif (tex == 1) or (tex == 3):
		model_plankr = model_plankr + "rubber"
	elif (tex == 4) or (tex == 2):
		model_plankr = model_plankr + "gravel"
	
	plankl = vizfx.addChild(asset_dir + model_plankl + ".osgb")
	plankr = vizfx.addChild(asset_dir + model_plankr + ".osgb")
	
	plankl.setPosition([-5.95, -0.25, 16.25])
	plankl.setEuler([45,0,0])
	plankr.setPosition([-5.95, -0.25, -16.25])
	plankr.setEuler([135,0,0])
	
	# initialize starting plane
	plankstart = vizshape.addBox([5,0.5,5])
	plankstart.setPosition([-21.5,0,0])
	plankstart.setEuler([45,0,0])
	
def loadFrictionConditions(fri):
	"""Set up paths for a friction condition trial.
	@args:
		fri (int): the parameter determining the exact friction
		condition for this trial.

	"""
	# Left and right doors, respectively
	global door_l, door_r
	
	door_l = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_l.setEuler(90,0,0)
	door_l.setPosition(12.5,2.0,29.75)
	door_r = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_r.setEuler(90,0,0)
	door_r.setPosition(12.5,2.0,-32.5)

	# Change the origin and where door will rotate
	door_l.center(0.5,0,0)
	door_r.center(0.5,0,0)
	
	# Make paths
	plankl = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	plankr = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	
	'''
	# Friction conditions
	0. Lshiny, Rmatte
	1. Lmatte, Rshiny
	
	'''
	if (fri == 0):
		plankl.specular(0.3, 0.3, 0.3)
	elif (fri == 1):
		plankr.specular(0.3, 0.3, 0.3)
	
	plankl.setPosition([-5.95, -0.25, 16.25])
	plankl.setEuler([45,0,0])
	plankr.setPosition([-5.95, -0.25, -16.25])
	plankr.setEuler([135,0,0])
	
	# initialize starting plane
	plankstart = vizshape.addBox([5,0.5,5])
	plankstart.setPosition([-21.5,0,0])
	plankstart.setEuler([45,0,0])
	
def loadWidthGeometry(wid):
	"""Set up paths for a geometry condition trial.
	@args:
		wid (int): the parameter determining the exact width condition
		for this trial.

	"""
	global door_l, door_r
	
	# Left and right doors, respectively
	door_l = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_l.setEuler(90,0,0)
	door_l.setPosition(12.5,2.0,29.75)
	door_r = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_r.setEuler(90,0,0)
	door_r.setPosition(12.5,2.0,-32.5)

	#change the origin and where door will rotate
	door_l.center(0.5,0,0)
	door_r.center(0.5,0,0)
	
	'''
	Width conditions:
	0. L0.5x, R1x 
	1. L1x, R0.5x
	2. L2x, R1x
	3. L1x, R2x
	4. L0.5x, R2x
	5. L2x, R0.5x
	#6 possibilities
	
	'''
	# initialize width of first plane
	if (wid == 0) or (wid == 4):
		model_plankl = "p_nar_rubber"
	if (wid == 2) or (wid == 5):
		model_plankl = "p_wid_rubber"
	elif (wid == 1) or (wid == 3) or (wid == 6):
		model_plankl = "p_mid_rubber"

	# initialize width of second plane
	if (wid == 1) or (wid == 5):
		model_plankr = "p_nar_rubber"
	if (wid == 3) or (wid == 4):
		model_plankr = "p_wid_rubber"
	elif (wid == 0) or (wid == 2) or (wid == 6):
		model_plankr = "p_mid_rubber"
		
	plankl = vizfx.addChild(asset_dir + model_plankl + ".osgb")
	plankr = vizfx.addChild(asset_dir + model_plankr + ".osgb")
	
	plankl.setPosition([-5.95, -0.25, 16.25])
	plankl.setEuler([45,0,0])
	plankr.setPosition([-5.95, -0.25, -16.25])
	plankr.setEuler([135,0,0])
	
	# initialize starting plane
	plankstart = vizshape.addBox([5,0.5,5])
	plankstart.setPosition([-21.5,0,0])
	plankstart.setEuler([45,0,0])
	
	global inldoor, inrdoor, nearLDoor, nearRDoor,crispy
	inldoor = False
	inrdoor = False
	nearLDoor = False
	nearRDoor = False
	crispy = False
	
	#Create proximity manager 
	global autodoor, goal, crispy_manager
	goal = vizproximity.Manager()
	autodoor = vizproximity.Manager()
	crispy_manager = vizproximity.Manager()

	# Proximity sensor
	global rdoor_sensor, ldoor_sensor, ldoor_open_sensor, rdoor_open_sensor
	ldoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,32))
	rdoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,-32))
	ldoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,32))
	rdoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,-32))
	
	if wid == 0:
		crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (28.,2.5),(0,30.5)]),source=viz.Matrix.translate(-22,0,-35))
		crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (29.5,-3.75),(1.3,-32), (0.5,-31.3), (0,-31.75)]), source=viz.Matrix.translate(-22,0,35))
		crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-2.0,-28),(-31.55,1.4),(-3.5,29.5),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 1:
		crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (29.5,3.75),(1.3,32), (0.5,31.3), (0,31.75)]),source=viz.Matrix.translate(-22,0,-35))
		crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (28.,-2.5),(0,-30.5)]), source=viz.Matrix.translate(-22,0,35))
		crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-3.5,-29.5),(-31.55,-1.4),(-2.,28),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 2:
		crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (28.,2.5),(0,30.5)]),source=viz.Matrix.translate(-22,0,-35))
		crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,-29.1)]), source=viz.Matrix.translate(-22,0,35))
		crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-2.0,-28),(-29.35,-0.725),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 3:
		crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,29.1)]),source=viz.Matrix.translate(-22,0,-35))
		crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (28.,-2.5),(0,-30.5)]), source=viz.Matrix.translate(-22,0,35))
		crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-29.35,0.725),(-2.,28),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 4:
		crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,29.1)]),source=viz.Matrix.translate(-22,0,-35))
		crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (29.5,-3.75),(1.3,-32), (0.5,-31.3), (0,-31.75)]), source=viz.Matrix.translate(-22,0,35))
		crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-29.5,0.725),(-30.25,0.125),(-31.575,1.38),(-3.5,29.5),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 5:
		crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (29.5,3.75),(1.3,32), (0.5,31.3), (0,31.75)]),source=viz.Matrix.translate(-22,0,-35))
		crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,-29.1)]), source=viz.Matrix.translate(-22,0,35))
		crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-3.5,-29.5),(-31.575,-1.38),(-30.25,-0.125),(-29.5,-0.725),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))

	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	goal.addTarget(target)
	autodoor.addTarget(target)
	crispy_manager.addTarget(target)

	# Add destination sensors to manager
	goal.addSensor(ldoor_sensor)
	goal.addSensor(rdoor_sensor)
	autodoor.addSensor(ldoor_open_sensor)
	autodoor.addSensor(rdoor_open_sensor)
	crispy_manager.addSensor(crispy_sensor1)
	crispy_manager.addSensor(crispy_sensor2)
	crispy_manager.addSensor(crispy_sensor3)

	# Toggle debug shapes with keypress 
	vizact.onkeydown("l",goal.setDebug,viz.TOGGLE)
	vizact.onkeydown("o", autodoor.setDebug,viz.TOGGLE)
	vizact.onkeydown("9", crispy_manager.setDebug,viz.TOGGLE)
	
	autodoor.onEnter(None,openSensame)
	goal.onEnter(None,enterProximity)
	crispy_manager.onEnter(None,friedParticipant)
	
def sensorSetup():
	"""Initialize the proximity sensors for texture, width and 
	friction conditions.
	
	"""
	# Set up door opening and 'in' sensors
	global inldoor, inrdoor, nearLDoor, nearRDoor, crispy
	inldoor = False
	inrdoor = False
	nearLDoor = False
	nearRDoor = False
	crispy = False
	
	#Create proximity manager 
	global autodoor, goal, crispy_manager
	goal = vizproximity.Manager()
	autodoor = vizproximity.Manager()
	crispy_manager = vizproximity.Manager()

	# Proximity sensors
	global rdoor_sensor, ldoor_sensor, ldoor_open_sensor, rdoor_open_sensor
	ldoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,32))
	rdoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,-32))
	crispy_sensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (28.,2.5),(0,30.5)]),source=viz.Matrix.translate(-22,0,-35))
	crispy_sensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (28.,-2.5),(0,-30.5)]), source=viz.Matrix.translate(-22,0,35))
	crispy_sensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-2.0,-28),(-30,0),(-2.0,28),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))

	ldoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,32))
	rdoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,-32))
	
	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	goal.addTarget(target)
	autodoor.addTarget(target)
	crispy_manager.addTarget(target)

	# Add destination sensors to manager
	goal.addSensor(ldoor_sensor)
	goal.addSensor(rdoor_sensor)
	autodoor.addSensor(ldoor_open_sensor)
	autodoor.addSensor(rdoor_open_sensor)
	crispy_manager.addSensor(crispy_sensor1)
	crispy_manager.addSensor(crispy_sensor2)
	crispy_manager.addSensor(crispy_sensor3)

	# Toggle debug shapes with keypress 
	vizact.onkeydown("l",goal.setDebug,viz.TOGGLE)
	vizact.onkeydown("o", autodoor.setDebug,viz.TOGGLE)
	vizact.onkeydown("9", crispy_manager.setDebug,viz.TOGGLE)
	
	autodoor.onEnter(None,openSensame)
	goal.onEnter(None,enterProximity)
	crispy_manager.onEnter(None,friedParticipant)
	
def loadInclineParam(inc):
	"""Set up a trial where the condition is between inclines."""
	
	# Computer game controls
	viz.cam.setHandler(vizcam.KeyboardCamera(forward='w',backward='s', left='a',right='d',turnRight='e',turnLeft='q'))
	view = viz.MainView
	def mousemove(e):
		euler = view.get(viz.HEAD_EULER)
		euler[0] += e.dx*0.1
		euler[1] += -e.dy*0.1
		euler[1] = viz.clamp(euler[1],-90.0,90.0)
		euler[2] = 0
		view.setEuler(euler,viz.HEAD_ORI)
	viz.callback(viz.MOUSE_MOVE_EVENT,mousemove)
	
	viz.MainView.setPosition([-20, -10, 0])
	viz.MainView.setEuler(90,0,0)
	
	# Add ground
	ground = viz.addChild("ground.osgb")
	ground.texture(lava)
	ground.setScale(1.5,0,1.5)
	global inldoor, inrdoor, nearLDoor, nearRDoor,crispy, goal

	# Set up sensors
	inldoor = False
	inrdoor = False
	nearLDoor = False
	nearRDoor = False
	crispy = False
	
	# Create proximity manager 
	global autodoor, goal, crispy_manager
	goal= vizproximity.Manager()
	autodoor = vizproximity.Manager()
	crispy_manager = vizproximity.Manager()

	# Proximity sensor
	global rdoor_sensor, ldoor_sensor, ldoor_open_sensor, rdoor_open_sensor, plankl_sensor, plankr_sensor, \
	plankstarts_sensor, floor_lSensor, floor_rSensor, floort1_sensor, floorT2Sensor
	
	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	goal.addTarget(target)
	autodoor.addTarget(target)
	crispy_manager.addTarget(target)
	
	global plankl, plankr

	# Main room setup
	wall_b = vizshape.addPlane([75, 30])
	wall_b.setPosition(-22.25, 0, 0)
	wall_b.setEuler(x=90, y=90, z=0)
	wall_b.texture(metal)
	
	ceiling = vizshape.addPlane([75,75])
	ceiling.setEuler(0, 180, 0)
	ceiling.setPosition(15,10, 0)
	ceiling.texture(metal)

	global door_l, door_r
	door_l = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_l.setEuler(90,0,0)
	door_l.setPosition(22.5,-20,4.75)
		
	door_r = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	door_r.setEuler(90,0,0)
		
	door_l.center(0.5,0,0)
	door_r.center(0.5,0,0)
	
	plankl = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	plankr = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	
	# I've nicknamed the next section of code:
	# "I hate you for being right, Pythagoras"
	
	if (inc == 0):
		#slant up
		plankl.setEuler([45,-20,0])
	elif (inc == 1):
		#slant down
		plankl.setEuler([45,0,0])
	
	# initialize second plane
	if (inc == 1):
		# slant up
		plankr.setEuler([135,-20,0])
	elif (inc == 0):
		#slant down
		plankr.setEuler([135,0,0])
		
	if inc == 0:
		# rightmost wall
		wall_r = vizshape.addPlane([75, 30])
		wall_r.setPosition(10,0,-35)
		wall_r.setEuler(x=0, y=90, z=0)
		wall_r.texture(metal)
		# leftmost wall
		wall_l = vizshape.addPlane([75,30])
		wall_l.setPosition(10,0,35)
		wall_l.setEuler(x=0, y=-90, z=0)
		wall_l.texture(metal)
		
		# destination point
		plankl.setPosition([-6.7, -7.15, 15.55])
		plankr.setPosition([-5.95, -14, -16.25])
		
		tex_mwall_tlr = vizmat.Transform()
		tex_mwall_tlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		tex_mwall_tc = vizmat.Transform()
		tex_mwall_tc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# target area, top floor
		floorT1 = vizshape.addBox([25,0.5,75])
		floorT1.setPosition(22,0,0)
		# target area, bottom floor
		floorT2 = vizshape.addBox([25,0.5,75])
		floorT2.setPosition(23,-13.75,0)
		
		# target area, top ceiling	
		wall_tt = vizshape.addBox([25,6,75])
		wall_tt.setEuler(0,0,0)
		wall_tt.setPosition(25,7,0)
		wall_tt.texture(metal)
		
		# top left wall facing user, target area
		# is narrow in this condition
		wall_tl = vizshape.addBox([0.25,4,3])
		wall_tl.setEuler(0,0,0)
		wall_tl.setPosition(12.75,2.25,33.75)
		wall_tl.texmat(tex_mwall_tlr)
		wall_tl.texture(tile)
		
		# top right facing user
		# is wide in this condition
		wall_ttr = vizshape.addBox([0.25,4,65])
		wall_ttr.setEuler(0,0,0)
		wall_ttr.setPosition(12.75,2.25, -3)
		wall_ttr.texture(tile)
		
		# bottom left wall
		# is wide in this condition
		wall_tbl = vizshape.addBox([0.25,4.25,65])
		wall_tbl.setEuler(0,0,0)
		wall_tbl.setPosition(12.75,-11.5,3)	
		wall_tbl.texmat(tex_mwall_tlr)
		wall_tbl.texture(tile)
		
		# bottom right wall
		# is narrow in this condition
		wall_tbr = vizshape.addBox([0.25,4.25,3])
		wall_tbr.setEuler(0,0,0)
		wall_tbr.setPosition(12.75,-11.5,-33.75)
		wall_tbr.texmat(tex_mwall_tlr)
		wall_tbr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# central wall in target area
		wall_tc = vizshape.addBox([0.25,9.25,75])
		wall_tc.setEuler(0,0,0)
		wall_tc.setPosition(12.75,-4.75,0.0)
		wall_tc.texmat(tex_mwall_tc)
		wall_tc.texture(tile)
		
		# back wall behind target area
		wall_tb = vizshape.addPlane([75,4])
		wall_tb.setPosition(40, 2, 0)
		wall_tb.setEuler(x=90, y=270, z=0)
		
		#platforms in front of doors
		floor_l = vizshape.addBox([8,0.5,8])
		floor_l.setEuler(45,0,0)
		floor_l.setPosition(9.85,0,31)
		floor_r = vizshape.addBox([8,1,8])
		floor_r.setEuler(45,0,0)
		floor_r.setPosition(11,-14,-33.25)
		
		ground.setPosition([0, -14., 0])
		plankstart = vizshape.addBox([6,2,6])
		plankstart.setPosition([-22.2,-14.5,0])
		plankstart.setEuler([45,0,0])
		
		
		door_l.setPosition(12.5,2.0,29.75)
		door_r.setPosition(12.5,-11.5,-32.25)
		
		ldoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,32))
		rdoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,-10.5,-32))
		
		ldoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,32))
		rdoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,-10.5,-32))
		
		plankstarts_sensor = vizproximity.addBoundingBoxSensor(plankstart,scale=(1.0,10.0,1.0))
		plankl_sensor = vizproximity.addBoundingBoxSensor(plankl,scale=(1.0,18.0,1.0))
		plankr_sensor = vizproximity.addBoundingBoxSensor(plankr,scale=(1.0,18.0,1.0))
		floor_lSensor = vizproximity.addBoundingBoxSensor(floor_l,scale=(1.25,18.0,1.25))
		floor_rSensor = vizproximity.addBoundingBoxSensor(floor_r,scale=(1.25,18.0,1.25))
		floort1_sensor = vizproximity.addBoundingBoxSensor(floorT1,scale=(1.0,18.0,1.0))
		floorT2Sensor = vizproximity.addBoundingBoxSensor(floorT2,scale=(1.0,18.0,1.0))

	elif inc == 1:
		# rightmost wall
		wall_r = vizshape.addPlane([75, 30])
		wall_r.setPosition(10,0,-35)
		wall_r.setEuler(x=0, y=90, z=0)
		wall_r.texture(metal)
		# leftmost wall
		wall_l = vizshape.addPlane([75,30])
		wall_l.setPosition(10,0,35)
		wall_l.setEuler(x=0, y=-90, z=0)
		wall_l.texture(metal)
		
		# destination point
		plankl.setPosition([-5.95, -14, 16.25])
		plankr.setPosition([-6.7, -7.15, -15.55])
		
		tex_mwall_tlr = vizmat.Transform()
		tex_mwall_tlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		tex_mwall_tc = vizmat.Transform()
		tex_mwall_tc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# target area, top floor
		floorT1 = vizshape.addBox([25,0.5,75])
		floorT1.setPosition(22.5,0,0)
		# target area, bottom floor
		floorT2 = vizshape.addBox([25,0.5,75])
		floorT2.setPosition(25,-13.75,0)
		
		# target area, top ceiling	
		wall_tt = vizshape.addBox([25,6,75])
		wall_tt.setEuler(0,0,0)
		wall_tt.setPosition(25,7,0)
		wall_tt.texture(metal)
		
		# top left wall facing user, target area
		# is narrow in this condition
		wall_tl = vizshape.addBox([0.25,4,65])
		wall_tl.setEuler(0,0,0)
		wall_tl.setPosition(12.75,2.25,3)
		wall_tl.texmat(tex_mwall_tlr)
		wall_tl.texture(tile)
		
		# top right facing user
		# is wide in this condition
		wall_ttr = vizshape.addBox([0.25,4,3])
		wall_ttr.setEuler(0,0,0)
		wall_ttr.setPosition(12.75,2.25,-33.75)	
		wall_ttr.texmat(tex_mwall_tlr)
		wall_ttr.texture(tile)
		
		# bottom left wall
		# is wide in this condition
		wall_tbl = vizshape.addBox([0.25,4.25,3])
		wall_tbl.setEuler(0,0,0)
		wall_tbl.setPosition(12.75,-11.5,33.75)	
		wall_tbl.texmat(tex_mwall_tlr)
		wall_tbl.texture(tile)
		
		# bottom right wall
		# is narrow in this condition
		wall_tbr = vizshape.addBox([0.25,4.25,65])
		wall_tbr.setEuler(0,0,0)
		wall_tbr.setPosition(12.75,-11.5,-2.75)
		wall_tbr.texmat(tex_mwall_tlr)
		wall_tbr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# central wall in target area
		wall_tc = vizshape.addBox([0.25,9.25,75])
		wall_tc.setEuler(0,0,0)
		wall_tc.setPosition(12.75,-4.75,0.0)
		wall_tc.texmat(tex_mwall_tc)
		wall_tc.texture(tile)
		
		# back wall behind target area
		wall_tb = vizshape.addPlane([20,4])
		wall_tb.setPosition(40, 2, 0)
		wall_tb.setEuler(x=90, y=270, z=0)
		
		# Platforms in front of doors
		floor_l = vizshape.addBox([8,0.5,8])
		floor_l.setEuler(45,0,0)
		floor_l.setPosition(11.75,-14,32.5)
		floor_r = vizshape.addBox([8,0.5,8])
		floor_r.setEuler(45,0,0)
		floor_r.setPosition(9.85,0,-31.)
		
		ground.setPosition([0, -14., 0])
		plankstart = vizshape.addBox([6,2,6])
		plankstart.setPosition([-22.2,-14.5,0])
		plankstart.setEuler([45,0,0])
		
		door_l.setPosition(12.5,-11.5,29.75)
		door_r.setPosition(12.5,2.0,-32.25)
		
		ldoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,-10.5,32))
		rdoor_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,-32))
		ldoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,-10.5,32))
		rdoor_open_sensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,-32))
		
		plankstarts_sensor = vizproximity.addBoundingBoxSensor(plankstart,scale=(1.0,10.0,1.0))
		plankl_sensor = vizproximity.addBoundingBoxSensor(plankl,scale=(1.0,18.0,1.0))
		plankr_sensor = vizproximity.addBoundingBoxSensor(plankr,scale=(1.0,18.0,1.0))
		floor_lSensor = vizproximity.addBoundingBoxSensor(floor_l,scale=(1.25,18.0,1.25))
		floor_rSensor = vizproximity.addBoundingBoxSensor(floor_r,scale=(1.25,18.0,1.25))
		floort1_sensor = vizproximity.addBoundingBoxSensor(floorT1,scale=(1.0,18.0,1.0))
		floorT2Sensor = vizproximity.addBoundingBoxSensor(floorT2,scale=(1.0,18.0,1.0))
		
	# Add destination sensors to manager
	
	goal.addSensor(ldoor_sensor)
	goal.addSensor(rdoor_sensor)
	autodoor.addSensor(ldoor_open_sensor)
	autodoor.addSensor(rdoor_open_sensor)
	crispy_manager.addSensor(plankstarts_sensor)
	crispy_manager.addSensor(plankl_sensor)
	crispy_manager.addSensor(plankr_sensor)
	crispy_manager.addSensor(floor_lSensor)
	crispy_manager.addSensor(floor_rSensor)
	crispy_manager.addSensor(floort1_sensor)
	crispy_manager.addSensor(floorT2Sensor)
	
	# Toggle debug shapes with keypress 
	vizact.onkeydown("l",goal.setDebug,viz.TOGGLE)
	vizact.onkeydown("o", autodoor.setDebug,viz.TOGGLE)
	vizact.onkeydown("9", crispy_manager.setDebug,viz.TOGGLE)
	
	autodoor.onEnter(None,openSensame)
	goal.onEnter(None,enterProximity)
	crispy_manager.onEnter(None,deepfriedEnter)
	crispy_manager.onExit(None,deepfriedExit)
	
def friedParticipant(event):
	"""Reset participant location if they step out of bounds.
	@args:
		event (vizproximity.ENTER_PROXIMITY_EVENT):
		User walks into lava.
		
	"""
	viz.MainView.setPosition([-20, 2, 0])
	
def openSensame(event):
	"""Open doors when user steps in front of one of them."""
	global nearLDoor, nearRDoor
	opendoor = vizact.spinto([0,1,0, 181], 360)
	if event.sensor == ldoor_open_sensor:
		nearLDoor = True
		door_l.addAction(opendoor)
	elif event.sensor == rdoor_open_sensor:
		nearRDoor = True
		door_r.addAction(opendoor)
	
def enterProximity(event):
	"""End trial when participant makes a choice of L or R
	@args: 
		event (vizproximity.ENTER_PROXIMITY_EVENT):
		User walks into the goal area.
		
	"""
	global inldoor, inrdoor, t0, autodoor, goal, crispy_manager
	finish_time = time.time() - t0
	if event.sensor == ldoor_sensor:
		inldoor = True
		choice = "L"
		
	elif event.sensor == rdoor_sensor:
		inrdoor = True
		choice = "R"
		
	autodoor.clearSensors()
	goal.clearSensors()
	crispy_manager.clearSensors()
	children = viz.MainScene.getChildren()
	for child in children:
		child.remove()
	getData(choice, finish_time)
	
def deepfriedEnter(event):
	"""Triggered when user walks into a valid walking zone.

	Incline conditions-specific sensor. If this is triggered right
	after a user triggers the function deepfriedExit, then the user
	is still safe and the trial continues as normal.

	@args: 
		event (vizproximity.ENTER_PROXIMITY_EVENT):
		User walks into a valid walking area.
		
	"""
	global crispy
	if crispy == True:
		crispy = False
def deepfriedExit(event):
	"""Triggered when user walks out of a valid walking zone.

	Incline conditions-specific sensor. If this is triggered twice
	in a row, the user has walked out of a valid area (into lava),
	the misstep is recorded and the user's position is reset to start.

	@args: 
		event (vizproximity.ENTER_PROXIMITY_EVENT):
		User walks out of the walking goal area.
		
	"""
	global crispy
	if crispy == False:
		crispy = True
	elif crispy == True:
		viz.MainView.setPosition([-20, -10, 0])

def waitTrial():
	"""Keep trial running until the user finishes it."""
	yield vizproximity.waitEnter(manager=goal)

def run():
	"""Run the experiment."""
	#conds = ["00", "01", "02", "03", "04", "05", "10", "11", "12", "13", "14", "15", "20", "21", "30", "31"]
	conds = ["30", "31"]
	shuffle(conds)
	for c in conds:
		yield runTrial(c)
	viz.quit()


def runTrial(c):
	"""Run a trial in the experiment.
	@args:
		c (string): the identifier for this specific trial.
		
	"""
	global trial_cond, t0
	trial_cond = c
	if c[0] == "0":
		loadBaseScene()
		loadTextureConditions(int(c[1]))
		sensorSetup()
		t0 = time.time()

	elif c[0] == "1":
		loadBaseScene()
		loadWidthGeometry(int(c[1]))
		t0 = time.time()
		
	elif c[0]=="2":
		loadBaseScene()
		loadFrictionConditions(int(c[1]))
		sensorSetup()
		t0 = time.time()
		
	elif c[0]=="3":
		loadInclineParam(int(c[1]))
		t0 = time.time()
	
	yield waitTrial()

viz.go()
viztask.schedule(run())
#viz.quit()