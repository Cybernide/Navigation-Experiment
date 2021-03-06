﻿# standard Vizard library
import viz
# actors library
# import vizact
# proximity sensing library
import vizproximity
# 'quests' library
import viztask
# infodump mode
import vizinfo
# planes and shapes
import vizshape
# lighting effects
import vizfx
import vizact
#from random import randint, sample
import ts_main
import time
import vizmat

# Assets directory
asset_dir = "C:\Users\Cyan\Documents\Viz_envmts\Thesis-Navigation\Navigation-Experiment\\"
starting_pos = [-20, 2, 0]

def loadscene(remaining, wid):
	t0 = time.time()
	print "width condition: " + str(wid)
	# take genwid as the parameter for width of path, and gentex as the parameter for the texture
	viz.go()

	#set graphic parameters
	viz.setMultiSample(4)
	viz.fov(80)
	viz.go()
	
	# Add collision
	viz.collision(viz.ON)

	# this section is really just so I can walk around like it's a computer game
	###########################
	import vizcam
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
	###################################################

	viz.MainView.setPosition(starting_pos)
	viz.MainView.setEuler(90,0,0)

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
	
	autodoor.onEnter(None,openSensame)
	manager.onEnter(None,enterProximity,remaining,t0)
	deepfriedManager.onEnter(None,friedParticipant)
	
def friedParticipant(event):
	global crispy
	crispy = True
	print str(crispy)
		
def openSensame(event):
	"""@args event"""
	global nearLDoor, nearRDoor
	opendoor = vizact.spinto([0,1,0, 181], 360)
	if event.sensor == lDoorOpenSensor:
		nearLDoor = True
		doorL.addAction(opendoor)
	elif event.sensor == rDoorOpenSensor:
		nearRDoor = True
		doorR.addAction(opendoor)
	
def enterProximity(event,tr,t0):
	"""@args vizproximity.ProximityEvent(), trial, time 0"""
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