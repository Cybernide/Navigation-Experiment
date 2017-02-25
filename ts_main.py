# standard Vizard library
import viz
# infodump mode
import vizinfo
# planes and shapes
from random import shuffle
import os.path
# proximity sensing library
import vizproximity
# 'quests' library
import viztask
# planes and shapes
import vizshape
# lighting effects
import vizfx
#from random import randint, sample
import vizact
import vizmat
import vizcam
import time

trials = 5
savepath = "C:\Users\Cyan\Documents\\"
subjid = raw_input("Enter participant ID: ")
flname = savepath + "test_subj" + subjid + ".txt"
results = open(flname, "a")
asset_dir = "C:\Users\Cyan\Documents\Viz_envmts\Thesis-Navigation\Navigation-Experiment\\"
starting_pos = [-20, 2, 0]
t0 = time.time()

#set graphic parameters
viz.setMultiSample(4)
viz.fov(80)

# Add collision
viz.collision(viz.ON)



#load textures
stone = viz.addTexture('images/tile_stone.jpg', wrap=viz.REPEAT)
tile = viz.addTexture('images/tile_slate.jpg', wrap=viz.REPEAT)
metal = viz.addTexture('metal.jpg', wrap=viz.REPEAT)
lava = viz.addTexture('lava.png', wrap=viz.REPEAT)

# Add white point light 
#light = vizfx.addPointLight(color=viz.WHITE, pos=(0,1,1))

# Add ground
ground = viz.addChild('ground.osgb')
ground.texture(lava)
ground.setScale(1.5,0,1.5)

# this section is really just so I can walk around like it's a computer game
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
	
def getData(choice, finish_time):
	global results
	results.write("\n" + choice + "," + str(finish_time))
	
'''def runTrials(remaining_trials):
	remaining_trials -= 1
	print remaining_trials
	if remaining_trials != 0:
		pathcond = randint(0,2)
		if pathcond == 0:
			gentex = randint(0,5)
			ts_tex.loadscene(trials, gentex)
		elif pathcond == 1:
			genwid = randint(0,5)
			ts_wid.loadscene(trials, genwid)
		elif pathcond == 2:
			genfri = randint(0,1)
			ts_fri.loadscene(trials,genfri)
		elif pathcond == 3:
			geninc = randint(0,5)em
			ts_inc.loadscene(trials,geninc)
	else:
		results.close()
		viz.quit()'''
		
		
def loadBaseScene():
	viz.go()
	viz.MainView.setPosition(starting_pos)
	viz.MainView.setEuler(90,0,0)

	global plankL, plankR
	# Room setup
	wallR = vizshape.addPlane([75, 30])
	wallR.setPosition(10,0,-35)
	wallR.setEuler(x=0, y=90, z=0)
	wallR.texture(metal)

	wallL = vizshape.addPlane([75,30])
	wallL.setPosition(10,0,35)
	wallL.setEuler(x=0, y=-90, z=0)
	wallL.texture(metal)

	wallB = vizshape.addPlane([75, 30])
	wallB.setPosition(-22.25, 0, 0)
	wallB.setEuler(x=90, y=90, z=0)
	wallB.texture(metal)
	
	ceiling = vizshape.addPlane([75,75])
	ceiling.setEuler(0, 180, 0)
	ceiling.setPosition(15,10, 0)
	ceiling.texture(metal)
	
	texMwallTlr = vizmat.Transform()
	texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
	texMwallTc = vizmat.Transform()
	texMwallTc.setScale( [1,1,1.3] )
	
	tile.wrap(viz.WRAP_T, viz.REPEAT)
	tile.wrap(viz.WRAP_S, viz.REPEAT)
	
	wallTF = vizshape.addBox([25,0.5,75])
	wallTF.setPosition(25,0,0)
	
	floorL = vizshape.addBox([8,0.5,8])
	floorL.setEuler(45,0,0)
	floorL.setPosition(11,0,33.25)
	floorR = vizshape.addBox([8,0.5,8])
	floorR.setEuler(45,0,0)
	floorR.setPosition(11,0,-33.25)
	
	wallTT = vizshape.addBox([25,6,75])
	wallTT.setEuler(0,0,0)
	wallTT.setPosition(25,7,0)
	wallTT.texture(metal)
	
	wallTl = vizshape.addBox([0.25,7.5,3])
	wallTl.setEuler(0,0,0)
	wallTl.setPosition(12.75,0.5,33.75)
	wallTl.texmat(texMwallTlr)
	wallTl.texture(tile)
	
	wallTr = vizshape.addBox([0.25,7.5,3])
	wallTr.setEuler(0,0,0)
	wallTr.setPosition(12.75,0.5,-33.75)	
	wallTr.texmat(texMwallTlr)
	wallTr.texture(tile)
	
	tile.wrap(viz.WRAP_T, viz.REPEAT)
	tile.wrap(viz.WRAP_S, viz.REPEAT)
	
	wallTc = vizshape.addBox([0.25,7.5,60.5])
	wallTc.setEuler(0,0,0)
	wallTc.setPosition(12.75,0.5,0.0)
	wallTc.texmat(texMwallTc)
	wallTc.texture(tile)
	
	wallTb = vizshape.addPlane([75,4])
	wallTb.setPosition(35, 2, 0)
	wallTb.setEuler(x=90, y=270, z=0)
	
def loadTextureConditions(cond):
	global doorL, doorR
	
	doorL = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	doorL.setEuler(90,0,0)
	doorL.setPosition(12.5,2.0,29.75)
	
	doorR = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	doorR.setEuler(90,0,0)
	doorR.setPosition(12.5,2.0,-32.5)

	# change the origin and where door will rotate
	doorL.center(0.5,0,0)
	doorR.center(0.5,0,0)
	
	#Make paths
	model_plankL = "p_mid_"
	model_plankR = "p_mid_"
	
	'''
	#texture conditions
	0. Lrubber, Rstone
	1. Lstone, Rrubber
	2. Lrubber, Rgravel
	3. Lgravel, Rrubber
	4. Lstone, Rgravel
	5. Lgravel, Rstone;
	'''
	if (tex == 0) or (tex == 2):
		model_plankL = model_plankL + "rubber"
	elif (tex == 1) or (tex == 4) or (tex == 6):
		model_plankL = model_plankL + "stone"
	elif (tex == 3) or (tex == 5):
		model_plankL = model_plankL + "gravel"
		
	if (tex == 0) or (tex == 5) or (tex == 6):
		model_plankR = model_plankR + "stone"
	elif (tex == 1) or (tex == 3):
		model_plankR = model_plankR + "rubber"
	elif (tex == 4) or (tex == 2):
		model_plankR = model_plankR + "gravel"
	
	plankL = vizfx.addChild(asset_dir + model_plankL + ".osgb")
	plankR = vizfx.addChild(asset_dir + model_plankR + ".osgb")
	
	plankL.setPosition([-5.95, -0.25, 16.25])
	plankL.setEuler([45,0,0])
	plankR.setPosition([-5.95, -0.25, -16.25])
	plankR.setEuler([135,0,0])
	
	# initialize starting plane
	plankStart = vizshape.addBox([5,0.5,5])
	plankStart.setPosition([-21.5,0,0])
	plankStart.setEuler([45,0,0])
	t0 = time.time()
	
def loadFrictionConditions(cond):
	# Door setup
	global doorL, doorR
	
	doorL = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	doorL.setEuler(90,0,0)
	doorL.setPosition(12.5,2.0,29.75)
	
	doorR = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	doorR.setEuler(90,0,0)
	doorR.setPosition(12.5,2.0,-32.5)

	#change the origin and where door will rotate
	doorL.center(0.5,0,0)
	doorR.center(0.5,0,0)
	
	# Initialize paths
	plankL = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	plankR = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	
	'''
	#friction conditions
	0. Lshiny, Rmatte
	1. Lmatte, Rshiny
	'''
	if (fri == 0):
		plankL.specular(0.3, 0.3, 0.3)
	elif (fri == 1):
		plankR.specular(0.3, 0.3, 0.3)
	
	plankL.setPosition([-5.95, -0.25, 16.25])
	plankL.setEuler([45,0,0])
	plankR.setPosition([-5.95, -0.25, -16.25])
	plankR.setEuler([135,0,0])
	
	# initialize starting plane
	plankStart = vizshape.addBox([5,0.5,5])
	plankStart.setPosition([-21.5,0,0])
	plankStart.setEuler([45,0,0])
	t0 = time.time()
	
def loadWidthGeometry(cond):
	global doorL, doorR
	
	doorL = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	doorL.setEuler(90,0,0)
	doorL.setPosition(12.5,2.0,29.75)
	
	doorR = viz.add("box.wrl", pos = [0,1,8], scale = [2.5,3.8,.05])
	doorR.setEuler(90,0,0)
	doorR.setPosition(12.5,2.0,-32.5)

	#change the origin and where door will rotate
	doorL.center(0.5,0,0)
	doorR.center(0.5,0,0)
	
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
		model_plankL = "p_nar_rubber"
	if (wid == 2) or (wid == 5):
		model_plankL = "p_wid_rubber"
	elif (wid == 1) or (wid == 3) or (wid == 6):
		model_plankL = "p_mid_rubber"

	# initialize width of second plane
	if (wid == 1) or (wid == 5):
		model_plankR = "p_nar_rubber"
	if (wid == 3) or (wid == 4):
		model_plankR = "p_wid_rubber"
	elif (wid == 0) or (wid == 2) or (wid == 6):
		model_plankR = "p_mid_rubber"
		
		
	plankL = vizfx.addChild(asset_dir + model_plankL + ".osgb")
	plankR = vizfx.addChild(asset_dir + model_plankR + ".osgb")
	
	plankL.setPosition([-5.95, -0.25, 16.25])
	plankL.setEuler([45,0,0])
	plankR.setPosition([-5.95, -0.25, -16.25])
	plankR.setEuler([135,0,0])
	
	# initialize starting plane
	plankStart = vizshape.addBox([5,0.5,5])
	plankStart.setPosition([-21.5,0,0])
	plankStart.setEuler([45,0,0])
	
	global inLDoor, inRDoor, nearLDoor, nearRDoor,crispy
	inLDoor = False
	inRDoor = False
	nearLDoor = False
	nearRDoor = False
	crispy = False
	
	#Create proximity manager 
	manager = vizproximity.Manager()
	autodoor = vizproximity.Manager()
	deepfriedManager = vizproximity.Manager()

	# Proximity sensor
	global rDoorSensor, lDoorSensor, lDoorOpenSensor, rDoorOpenSensor, crispySensor1, crispySensor2, crispySensor3
	#crispySensor2, crispySensor3
	lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,32))
	rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,-32))
	lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,32))
	rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,-32))
	
	if wid == 0:
		crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (28.,2.5),(0,30.5)]),source=viz.Matrix.translate(-22,0,-35))
		crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (29.5,-3.75),(1.3,-32), (0.5,-31.3), (0,-31.75)]), source=viz.Matrix.translate(-22,0,35))
		crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-2.0,-28),(-31.55,1.4),(-3.5,29.5),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 1:
		crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (29.5,3.75),(1.3,32), (0.5,31.3), (0,31.75)]),source=viz.Matrix.translate(-22,0,-35))
		crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (28.,-2.5),(0,-30.5)]), source=viz.Matrix.translate(-22,0,35))
		crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-3.5,-29.5),(-31.55,-1.4),(-2.,28),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 2:
		crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (28.,2.5),(0,30.5)]),source=viz.Matrix.translate(-22,0,-35))
		crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,-29.1)]), source=viz.Matrix.translate(-22,0,35))
		crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-2.0,-28),(-29.35,-0.725),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 3:
		crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,29.1)]),source=viz.Matrix.translate(-22,0,-35))
		crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (28.,-2.5),(0,-30.5)]), source=viz.Matrix.translate(-22,0,35))
		crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-29.35,0.725),(-2.,28),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 4:
		crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,29.1)]),source=viz.Matrix.translate(-22,0,-35))
		crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (29.5,-3.75),(1.3,-32), (0.5,-31.3), (0,-31.75)]), source=viz.Matrix.translate(-22,0,35))
		crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-29.5,0.725),(-30.25,0.125),(-31.575,1.38),(-3.5,29.5),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))
	elif wid == 5:
		crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (29.5,3.75),(1.3,32), (0.5,31.3), (0,31.75)]),source=viz.Matrix.translate(-22,0,-35))
		crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(0,-29.1)]), source=viz.Matrix.translate(-22,0,35))
		crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-3.5,-29.5),(-31.575,-1.38),(-30.25,-0.125),(-29.5,-0.725),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))

	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	manager.addTarget(target)
	autodoor.addTarget(target)
	deepfriedManager.addTarget(target)

	# Add destination sensors to manager
	manager.addSensor(lDoorSensor)
	manager.addSensor(rDoorSensor)
	autodoor.addSensor(lDoorOpenSensor)
	autodoor.addSensor(rDoorOpenSensor)
	deepfriedManager.addSensor(crispySensor1)
	deepfriedManager.addSensor(crispySensor2)
	deepfriedManager.addSensor(crispySensor3)

	# Toggle debug shapes with keypress 
	vizact.onkeydown('l',manager.setDebug,viz.TOGGLE)
	vizact.onkeydown('o', autodoor.setDebug,viz.TOGGLE)
	vizact.onkeydown('9', deepfriedManager.setDebug,viz.TOGGLE)
	t0 = time.time()
	
def sensorSetup():
	# Set up door opening and 'in' sensors
	global inLDoor, inRDoor, nearLDoor, nearRDoor, crispy
	inLDoor = False
	inRDoor = False
	nearLDoor = False
	nearRDoor = False
	crispy = False
	
	#Create proximity manager 
	manager = vizproximity.Manager()
	autodoor = vizproximity.Manager()
	deepfriedManager = vizproximity.Manager()

	# Proximity sensors
	global rDoorSensor, lDoorSensor, lDoorOpenSensor, rDoorOpenSensor, crispySensor1, crispySensor2, crispySensor3
	lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,32))
	rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,-32))
	crispySensor1 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,1.75), (28.,2.5),(0,30.5)]),source=viz.Matrix.translate(-22,0,-35))
	crispySensor2 = vizproximity.Sensor(vizproximity.PolygonArea([(0,0),(29,0),(27.25,-1.75), (28.,-2.5),(0,-30.5)]), source=viz.Matrix.translate(-22,0,35))
	crispySensor3 = vizproximity.Sensor(vizproximity.PolygonArea([(0.15,-28.8),(-1.25,-27.5),(-2.0,-28),(-30,0),(-2.0,28),(-1.25,27.5),(0.15,28.8)]), source=viz.Matrix.translate(12.25,0,0))

	lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,32))
	rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,-32))

	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	manager.addTarget(target)
	autodoor.addTarget(target)
	deepfriedManager.addTarget(target)

	# Add destination sensors to manager
	manager.addSensor(lDoorSensor)
	manager.addSensor(rDoorSensor)
	autodoor.addSensor(lDoorOpenSensor)
	autodoor.addSensor(rDoorOpenSensor)
	deepfriedManager.addSensor(crispySensor1)
	deepfriedManager.addSensor(crispySensor2)
	deepfriedManager.addSensor(crispySensor3)

	# Toggle debug shapes with keypress 
	vizact.onkeydown('l',manager.setDebug,viz.TOGGLE)
	vizact.onkeydown('o', autodoor.setDebug,viz.TOGGLE)
	vizact.onkeydown('9', deepfriedManager.setDebug,viz.TOGGLE)
	
	autodoor.onEnter(None,openSensame)
	manager.onEnter(None,enterProximity,t0)
	deepfriedManager.onEnter(None,friedParticipant)
	
def loadInclineParam(inc):
	global inLDoor, inRDoor, nearLDoor, nearRDoor,crispy
	inLDoor = False
	inRDoor = False
	nearLDoor = False
	nearRDoor = False
	crispy = False
	
	#Create proximity manager 
	manager = vizproximity.Manager()
	autodoor = vizproximity.Manager()
	crispyManager = vizproximity.Manager()

	# Proximity sensor
	global rDoorSensor, lDoorSensor, lDoorOpenSensor, rDoorOpenSensor, plankLSensor, plankRSensor, \
	plankStartSensor, floorLSensor, floorRSensor, floorT1Sensor, floorT2Sensor
	
	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	manager.addTarget(target)
	autodoor.addTarget(target)
	crispyManager.addTarget(target)

	
	global plankL, plankR

	#room
	wallB = vizshape.addPlane([75, 30])
	wallB.setPosition(-22.25, 0, 0)
	wallB.setEuler(x=90, y=90, z=0)
	wallB.texture(metal)
	
	ceiling = vizshape.addPlane([75,75])
	ceiling.setEuler(0, 180, 0)
	ceiling.setPosition(15,10, 0)
	ceiling.texture(metal)

	global doorL, doorR
	doorL = viz.add('box.wrl', pos = [0,1,8], scale = [2.5,3.8,.05])
	doorL.setEuler(90,0,0)
	doorL.setPosition(22.5,-20,4.75)
		
	doorR = viz.add('box.wrl', pos = [0,1,8], scale = [2.5,3.8,.05])
	doorR.setEuler(90,0,0)
		
	doorL.center(0.5,0,0)
	doorR.center(0.5,0,0)
	
	plankL = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	plankR = vizfx.addChild(asset_dir + "p_mid_rubber.osgb")
	
	# I've nicknamed the next section of code:
	# "I hate you for being right, Pythagoras"
	
	if (inc == 0):
		#slant up
		plankL.setEuler([45,-20,0])
	elif (inc == 1):
		#slant down
		plankL.setEuler([45,0,0])
	
	# initialize second plane
	if (inc == 1):
		# slant up
		plankR.setEuler([135,-20,0])
	elif (inc == 0):
		#slant down
		plankR.setEuler([135,0,0])
		
	if inc == 0:
		# rightmost wall
		wallR = vizshape.addPlane([75, 30])
		wallR.setPosition(10,0,-35)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)
		# leftmost wall
		wallL = vizshape.addPlane([75,30])
		wallL.setPosition(10,0,35)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)
		
		# destination point
		plankL.setPosition([-6.7, -7.15, 15.55])
		plankR.setPosition([-5.95, -14, -16.25])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# target area, top floor
		floorT1 = vizshape.addBox([25,0.5,75])
		floorT1.setPosition(22,0,0)
		# target area, bottom floor
		floorT2 = vizshape.addBox([25,0.5,75])
		floorT2.setPosition(23,-13.75,0)
		
		# target area, top ceiling	
		wallTT = vizshape.addBox([25,6,75])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(25,7,0)
		wallTT.texture(metal)
		
		# top left wall facing user, target area
		# is narrow in this condition
		wallTl = vizshape.addBox([0.25,4,3])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(12.75,2.25,33.75)
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
		
		# top right facing user
		# is wide in this condition
		wallTTr = vizshape.addBox([0.25,4,65])
		wallTTr.setEuler(0,0,0)
		wallTTr.setPosition(12.75,2.25, -3)
		wallTTr.texture(tile)
		
		# bottom left wall
		# is wide in this condition
		wallTBl = vizshape.addBox([0.25,4.25,65])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(12.75,-11.5,3)	
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
		
		# bottom right wall
		# is narrow in this condition
		wallTBr = vizshape.addBox([0.25,4.25,3])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(12.75,-11.5,-33.75)
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# central wall in target area
		wallTc = vizshape.addBox([0.25,9.25,75])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(12.75,-4.75,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
		
		# back wall behind target area
		wallTb = vizshape.addPlane([75,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		#platforms in front of doors
		floorL = vizshape.addBox([8,0.5,8])
		floorL.setEuler(45,0,0)
		floorL.setPosition(9.85,0,31)
		floorR = vizshape.addBox([8,1,8])
		floorR.setEuler(45,0,0)
		floorR.setPosition(11,-14,-33.25)
		
		ground.setPosition([0, -14., 0])
		plankStart = vizshape.addBox([6,2,6])
		plankStart.setPosition([-22.2,-14.5,0])
		plankStart.setEuler([45,0,0])
		viz.MainView.setPosition(starting_pos)
		viz.MainView.setEuler(90,0,0)
		
		doorL.setPosition(12.5,2.0,29.75)
		doorR.setPosition(12.5,-11.5,-32.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,32))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,-10.5,-32))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,32))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,-10.5,-32))
		
		plankStartSensor = vizproximity.addBoundingBoxSensor(plankStart,scale=(1.0,10.0,1.0))
		plankLSensor = vizproximity.addBoundingBoxSensor(plankL,scale=(1.0,18.0,1.0))
		plankRSensor = vizproximity.addBoundingBoxSensor(plankR,scale=(1.0,18.0,1.0))
		floorLSensor = vizproximity.addBoundingBoxSensor(floorL,scale=(1.0,18.0,1.5))
		floorRSensor = vizproximity.addBoundingBoxSensor(floorR,scale=(1.0,18.0,1.0))
		floorT1Sensor = vizproximity.addBoundingBoxSensor(floorT1,scale=(1.0,18.0,1.0))
		floorT2Sensor = vizproximity.addBoundingBoxSensor(floorT2,scale=(1.0,18.0,1.0))

	if inc == 1:
		# rightmost wall
		wallR = vizshape.addPlane([75, 30])
		wallR.setPosition(10,0,-35)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)
		# leftmost wall
		wallL = vizshape.addPlane([75,30])
		wallL.setPosition(10,0,35)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)
		
		# destination point
		plankL.setPosition([-5.95, -14, 16.25])
		plankR.setPosition([-6.7, -7.15, -15.55])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# target area, top floor
		floorT1 = vizshape.addBox([25,0.5,75])
		floorT1.setPosition(22.5,0,0)
		# target area, bottom floor
		floorT2 = vizshape.addBox([25,0.5,75])
		floorT2.setPosition(25,-13.75,0)
		
		# target area, top ceiling	
		wallTT = vizshape.addBox([25,6,75])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(25,7,0)
		wallTT.texture(metal)
		
		# top left wall facing user, target area
		# is narrow in this condition
		wallTl = vizshape.addBox([0.25,4,65])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(12.75,2.25,3)
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
		
		# top right facing user
		# is wide in this condition
		wallTTr = vizshape.addBox([0.25,4,3])
		wallTTr.setEuler(0,0,0)
		wallTTr.setPosition(12.75,2.25,-33.75)	
		wallTTr.texmat(texMwallTlr)
		wallTTr.texture(tile)
		
		# bottom left wall
		# is wide in this condition
		wallTBl = vizshape.addBox([0.25,4.25,3])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(12.75,-11.5,33.75)	
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
		
		# bottom right wall
		# is narrow in this condition
		wallTBr = vizshape.addBox([0.25,4.25,65])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(12.75,-11.5,-2.75)
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
		
		# central wall in target area
		wallTc = vizshape.addBox([0.25,9.25,75])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(12.75,-4.75,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
		
		# back wall behind target area
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		# Platforms in front of doors
		floorL = vizshape.addBox([8,0.5,8])
		floorL.setEuler(45,0,0)
		floorL.setPosition(11.75,-14,32.5)
		floorR = vizshape.addBox([8,0.5,8])
		floorR.setEuler(45,0,0)
		floorR.setPosition(9.85,0,-31.)
		
		ground.setPosition([0, -14., 0])
		plankStart = vizshape.addBox([6,2,6])
		plankStart.setPosition([-22.2,-14.5,0])
		plankStart.setEuler([45,0,0])
		viz.MainView.setPosition(starting_pos)
		viz.MainView.setPosition(90,0,0)
		
		doorL.setPosition(12.5,-11.5,29.75)
		doorR.setPosition(12.5,2.0,-32.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,-10.5,32))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(15.5,1.5,-32))
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,-10.5,32))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(12,1.5,-32))
		
		plankStartSensor = vizproximity.addBoundingBoxSensor(plankStart,scale=(1.0,10.0,1.0))
		plankLSensor = vizproximity.addBoundingBoxSensor(plankL,scale=(1.0,18.0,1.0))
		plankRSensor = vizproximity.addBoundingBoxSensor(plankR,scale=(1.0,18.0,1.0))
		floorLSensor = vizproximity.addBoundingBoxSensor(floorL,scale=(1.0,18.0,1.0))
		floorRSensor = vizproximity.addBoundingBoxSensor(floorR,scale=(1.5,18.0,1.0))
		floorT1Sensor = vizproximity.addBoundingBoxSensor(floorT1,scale=(1.0,18.0,1.0))
		floorT2Sensor = vizproximity.addBoundingBoxSensor(floorT2,scale=(1.0,18.0,1.0))
		
	
	# Add destination sensors to manager
	manager.addSensor(lDoorSensor)
	manager.addSensor(rDoorSensor)
	autodoor.addSensor(lDoorOpenSensor)
	autodoor.addSensor(rDoorOpenSensor)
	crispyManager.addSensor(plankStartSensor)
	crispyManager.addSensor(plankLSensor)
	crispyManager.addSensor(plankRSensor)
	crispyManager.addSensor(floorLSensor)
	crispyManager.addSensor(floorRSensor)
	crispyManager.addSensor(floorT1Sensor)
	crispyManager.addSensor(floorT2Sensor)
	
	# Toggle debug shapes with keypress 
	vizact.onkeydown('l',manager.setDebug,viz.TOGGLE)
	vizact.onkeydown('o', autodoor.setDebug,viz.TOGGLE)
	vizact.onkeydown('9', crispyManager.setDebug,viz.TOGGLE)
	
	autodoor.onEnter(None,openSensame)
	manager.onEnter(None,enterProximity,t0)
	crispyManager.onEnter(None,deepfriedEnter)
	crispyManager.onExit(None,deepfriedExit)
	
def friedParticipant(event):
	global crispy
	print str(crispy)
	if event.sensor == crispySensor1:
		crispy = True
		print str(crispy)
	if event.sensor == crispySensor2:
		crispy = True
		print str(crispy)
	
def openSensame(event):
	global nearLDoor, nearRDoor
	opendoor = vizact.spinto([0,1,0, 181], 360)
	if event.sensor == lDoorOpenSensor:
		nearLDoor = True
		doorL.addAction(opendoor)
	elif event.sensor == rDoorOpenSensor:
		nearRDoor = True
		doorR.addAction(opendoor)
	
def enterProximity(event,tr,t0):
	"""@args vizproximity.ProximityEvent()"""
	global inLDoor, inRDoor
	if event.sensor == lDoorSensor:
		inLDoor = True
		children = viz.MainScene.getChildren()
		for child in children:
			child.remove()
		ts_main.getData('L',time.time()-t0)
		ts_main.runTrials(tr)

	elif event.sensor == rDoorSensor:
		inRDoor = True
		children = viz.MainScene.getChildren()
		for child in children:
			child.remove()
		ts_main.getData('R',time.time()-t0)
		ts_main.runTrials(tr)
		
def deepfriedEnter(event):
	global crispy
	if crispy == True:
		crispy = False
def deepfriedExit(event):
	global crispy
	if crispy == False:
		crispy = True
	elif crispy == True:
		print "you ded!"
		
conds = ["00", "01", "02", "03", "04", "05", "10", "11", "12", "13", "14", "15", "20", "21", "30", "31"]
shuffle(conds)
for c in conds:
	if c[0] == "0":
		print "test0"
		loadBaseScene()
	elif c[0] == "1":
		print "test1"
		loadBaseScene()
	elif c[0]=="2":
		print "test2"
		loadBaseScene()
	elif c[0]=="3":
		print "test3"
		loadInclineParam(int(c[1]))
		
