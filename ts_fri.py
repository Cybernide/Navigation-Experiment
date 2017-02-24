# standard Vizard library
import viz
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
#from random import randint, sample
import vizact
import ts_main
import vizmat
import time

# Assets directory
asset_dir = "C:\Users\Cyan\Documents\Viz_envmts\Thesis-Navigation\Navigation-Experiment\\"


def loadscene(remaining, fri):
	t0 = time.time()
	print "friction condition: " + str(fri)
	# take genwid as the parameter for width of path, and gentex as the parameter for the texture
	viz.go()

	#set graphic parameters
	viz.setMultiSample(4)
	viz.fov(80)
	viz.go()
	
	# Add collision
	#viz.collision(viz.ON)

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

	viz.MainView.setPosition([-20, 2, 0])

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

	wallL = vizshape.addPlane([75,50])
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
	
	# Sensors for doors
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
	manager.onEnter(None,enterProximity,remaining,t0)
	deepfriedManager.onEnter(None,friedParticipant)
	
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