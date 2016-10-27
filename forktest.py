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
from random import randint, sample
import main


def loadscene(wid, tex):
	# take genwid as the parameter for width of path, and gentex as the parameter for the texture
	viz.go()

	#set graphic parameters
	viz.setMultiSample(4)
	viz.fov(50)
	viz.go()

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

	viz.MainView.setPosition([-12, 2, 0])

	#load textures
	stone = viz.addTexture('images/tile_stone.jpg', wrap=viz.REPEAT)
	gravel = viz.addTexture('gravel.jpg', wrap=viz.REPEAT)
	tile = viz.addTexture('images/tile_slate.jpg', wrap=viz.REPEAT)
	metal = viz.addTexture('metal.jpg', wrap=viz.REPEAT)
	rubber = viz.addTexture('rubber.jpg', wrap=viz.REPEAT)

	# Add white point light 
	light = vizfx.addPointLight(color=viz.WHITE, pos=(0,1,1))

	##Get a handle to the main headlight and disable it 
	#headLight = viz.MainView.getHeadLight() 
	#headLight.disable() 
	##Turn the headlight back on with a keypress. 
	#vizact.onkeydown( ' ', headLight.enable )

	# Add ground
	ground = viz.addChild('ground.osgb')
	ground.texture(tile)
	
	global planeL, planeR

	#room
	wallR = vizshape.addPlane([75, 30])
	wallR.setPosition(10,0,-10)
	wallR.setEuler(x=0, y=90, z=0)
	wallR.texture(metal)

	wallL = vizshape.addPlane([75,30])
	wallL.setPosition(10,0,10)
	wallL.setEuler(x=0, y=-90, z=0)
	wallL.texture(metal)

	wallB = vizshape.addPlane([25, 30])
	wallB.setPosition(-20, 0, 0)
	wallB.setEuler(x=90, y=90, z=0)
	wallB.texture(metal)
	
	ceiling = vizshape.addPlane([75,30])
	ceiling.setEuler(0, 180, 0)
	ceiling.setPosition(15,10, 0)
	ceiling.texture(metal)

	#destination point
	wallF = vizshape.addBox([10,0.5,20])
	wallF.setPosition(30,0,0)
	
	wallTT = vizshape.addBox([15,6,25])
	wallTT.setEuler(0,0,0)
	wallTT.setPosition(32.5,7,0)
	wallTT.texture(metal)
	
	wallTl = vizshape.addBox([0.25,8,3])
	wallTl.setEuler(0,0,0)
	wallTl.setPosition(25.25,0.5,8.75)
	wallTl.texture(tile)
	
	wallTr = vizshape.addBox([0.25,8,3])
	wallTr.setEuler(0,0,0)
	wallTr.setPosition(25.25,0.5,-8.75)	
	wallTr.texture(tile)
	
	wallTc = vizshape.addBox([0.25,8,9.5])
	wallTc.setEuler(0,0,0)
	wallTc.setPosition(25.25,0.5,0.0)
	wallTc.texture(tile)
	
	global doorL, doorR
	
	doorL = viz.add('box.wrl', pos = [0,1,8], scale = [2.5,3.8,.05])
	doorL.setEuler(90,0,0)
	doorL.setPosition(24.75,2.0,4.75)
	
	doorR = viz.add('box.wrl', pos = [0,1,8], scale = [2.5,3.8,.05])
	doorR.setEuler(90,0,0)
	doorR.setPosition(24.75,2.0,-7.25)

	#change the origin and where door will rotate
	doorL.center(0.5,0,0)
	doorR.center(0.5,0,0)

	#Width conditions (mutually exclusive):
	#path width - L0.5x, R1x; L1x, R0.5x; L2x, R1x; L1x, R2x; L0.5x, R2x; L2x, R0.5x
	#6 possibilities

	# initialize first plane
	if (wid == 0) or (wid == 4):
		planeL = vizshape.addBox([45,0.6,3])
	if (wid == 2) or (wid == 5):
		planeL = vizshape.addBox([45, 0.5, 12])
	else:
		planeL=vizshape.addBox([45,0.5,6])
	planeL.setPosition([2.5, 0, 6])
	planeL.texture(gravel)

	# initialize second plane
	planeR=vizshape.addBox([45,0.5,6])
	planeR.setPosition([2.5, 0, -6])
	planeR.texture(gravel)

	# initialize starting plane
	planeS = vizshape.addBox([10,0.5,6])
	planeS.setPosition([-10,0,0])

	sky = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
	skybox = viz.add('skydome.dlc')
	skybox.texture(sky)
	
	global inLDoor, inRDoor, nearLDoor, nearRDoor
	inLDoor = False
	inRDoor = False
	nearLDoor = False
	nearRDoor = False
	#Create proximity manager 
	manager = vizproximity.Manager()
	autodoor = vizproximity.Manager()

	# Proximity sensor
	global rDoorSensor, lDoorSensor, lDoorOpenSensor, rDoorOpenSensor
	lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,6))
	rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,-6))
	
	lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,6))
	rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,-6))

	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	manager.addTarget(target)
	autodoor.addTarget(target)

	# Add collision
	viz.collision(viz.ON)

	# Add destination sensors to manager
	manager.addSensor(lDoorSensor)
	manager.addSensor(rDoorSensor)
	autodoor.addSensor(lDoorOpenSensor)
	autodoor.addSensor(rDoorOpenSensor)

	# Toggle debug shapes with keypress 
	vizact.onkeydown('l',manager.setDebug,viz.TOGGLE)
	vizact.onkeydown('o', autodoor.setDebug,viz.TOGGLE)
	
	manager.onEnter(None,enterProximity)
	autodoor.onEnter(None,openSensame)
	
def openSensame(event):
	global nearLDoor, nearRDoor
	#create a spinning action for the door
	opendoor = vizact.spinto([0,1,0, 181], 360)
	#opendoor = vizact.spinTo(euler=[90,0,0], speed=50)
	if event.sensor == lDoorOpenSensor:
		nearLDoor = True
		doorL.addAction(opendoor)
	elif event.sensor == rDoorOpenSensor:
		nearRDoor = True
		doorR.addAction(opendoor)
	
def enterProximity(event):
	"""@args vizproximity.ProximityEvent()"""
	global inLDoor, inRDoor
	if event.sensor == lDoorSensor:
		inLDoor = True
		viz.MainView.setPosition([-9, 2, 0])
		#changePathWidth(1)
		main.setPathConditions()
		
	elif event.sensor == rDoorSensor:
		inRDoor = True
		viz.MainView.setPosition([-9, 2, 0])
		main.setPathConditions()