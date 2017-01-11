# standard Vizard library
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
import vizmat


def loadscene(wid, tex):
	print 'width = ' + str(wid)
	print 'texture = ' + str(tex)
	# take genwid as the parameter for width of path, and gentex as the parameter for the texture
	viz.go()

	#set graphic parameters
	viz.setMultiSample(4)
	viz.fov(50)
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
	gravel = viz.addTexture('gravel.jpg', wrap=viz.REPEAT)
	tile = viz.addTexture('images/tile_slate.jpg', wrap=viz.REPEAT)
	metal = viz.addTexture('metal.jpg', wrap=viz.REPEAT)
	rubber = viz.addTexture('rubber.jpg', wrap=viz.REPEAT)

	# Add white point light 
	light = vizfx.addPointLight(color=viz.WHITE, pos=(0,1,1))

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
	wallB.setPosition(-22.25, 0, 0)
	wallB.setEuler(x=90, y=90, z=0)
	wallB.texture(metal)
	
	ceiling = vizshape.addPlane([75,30])
	ceiling.setEuler(0, 180, 0)
	ceiling.setPosition(15,10, 0)
	ceiling.texture(metal)
	
	texMwallTlr = vizmat.Transform()
	texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
	texMwallTc = vizmat.Transform()
	texMwallTc.setScale( [1,1,1.3] )
	
	tile.wrap(viz.WRAP_T, viz.REPEAT)
	tile.wrap(viz.WRAP_S, viz.REPEAT)
	
	wallTF = vizshape.addBox([25,0.5,25])
	wallTF.setPosition(35,0,0)
	
	wallTT = vizshape.addBox([25,6,25])
	wallTT.setEuler(0,0,0)
	wallTT.setPosition(35,7,0)
	wallTT.texture(metal)
	
	wallTl = vizshape.addBox([0.25,7.5,3])
	wallTl.setEuler(0,0,0)
	wallTl.setPosition(22.75,0.5,8.75)
	wallTl.texmat(texMwallTlr)
	wallTl.texture(tile)
	
	wallTr = vizshape.addBox([0.25,7.5,3])
	wallTr.setEuler(0,0,0)
	wallTr.setPosition(22.75,0.5,-8.75)	
	wallTr.texmat(texMwallTlr)
	wallTr.texture(tile)
	
	tile.wrap(viz.WRAP_T, viz.REPEAT)
	tile.wrap(viz.WRAP_S, viz.REPEAT)
	
	wallTc = vizshape.addBox([0.25,7.5,9.5])
	wallTc.setEuler(0,0,0)
	wallTc.setPosition(22.75,0.5,0.0)
	wallTc.texmat(texMwallTc)
	wallTc.texture(tile)
	
	wallTb = vizshape.addPlane([20,4])
	wallTb.setPosition(40, 2, 0)
	wallTb.setEuler(x=90, y=270, z=0)
	
	global doorL, doorR
	
	doorL = viz.add('box.wrl', pos = [0,1,8], scale = [2.5,3.8,.05])
	doorL.setEuler(90,0,0)
	doorL.setPosition(22.5,2.0,4.75)
	
	doorR = viz.add('box.wrl', pos = [0,1,8], scale = [2.5,3.8,.05])
	doorR.setEuler(90,0,0)
	doorR.setPosition(22.5,2.0,-7.25)

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
	# initialize first plane
	if (wid == 0) or (wid == 4):
		planeL = vizshape.addBox([40,0.5,2])
		texMplaneL = vizmat.Transform()
		texMplaneL.setScale( [1*20,1,1] )
		planeL.texmat(texMplaneL)
	if (wid == 2) or (wid == 5):
		planeL = vizshape.addBox([40, 0.5, 8])
		texMplaneL = vizmat.Transform()
		texMplaneL.setScale( [1*5,1,1] )
		planeL.texmat(texMplaneL)
	elif (wid == 1) or (wid == 3) or (wid == 6):
		planeL=vizshape.addBox([40,0.5,6])
		texMplaneL = vizmat.Transform()
		texMplaneL.setScale( [1*6.5,1,1] )
		planeL.texmat(texMplaneL)
	planeL.setPosition([2.5, 0, 6])

	# initialize second plane
	if (wid == 1) or (wid == 5):
		planeR = vizshape.addBox([40,0.5,3])
		texMplaneR = vizmat.Transform()
		texMplaneR.setScale( [1*20,1,1] )
		planeR.texmat(texMplaneR)
	if (wid == 3) or (wid == 4):
		planeR = vizshape.addBox([40, 0.5, 8])
		texMplaneR = vizmat.Transform()
		texMplaneR.setScale( [1*5,1,1] )
		planeR.texmat(texMplaneR)
	elif (wid == 0) or (wid == 2) or (wid == 6):
		planeR=vizshape.addBox([40,0.5,6])
		texMplaneR = vizmat.Transform()
		texMplaneR.setScale( [1*6.5,1,1] )
		planeR.texmat(texMplaneR)
	planeR.setPosition([2.5, 0, -6])
	
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
		planeL.texture(rubber)
	if (tex == 1) or (tex == 4):
		planeL.texture(stone)
	elif (tex == 3) or (tex == 5):
		planeL.texture(gravel)
		
	if (tex == 0) or (tex == 5):
		planeR.texture(stone)
	if (tex == 1) or (tex == 3):
		planeR.texture(rubber)
	if (tex == 4) or (tex == 2):
		planeR.texture(gravel)
	
	# initialize starting plane
	
	planeS = vizshape.addBox([5,0.5,18])
	planeS.setPosition([-20,0,0])
	
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
	opendoor = vizact.spinto([0,1,0, 181], 360)
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
		#changePathWidth(1)
		children = viz.MainScene.getChildren()
		for child in children:
			child.remove()
		main.run_initPathConditions()
		
	elif event.sensor == rDoorSensor:
		inRDoor = True
		children = viz.MainScene.getChildren()
		for child in children:
			child.remove()
		main.run_initPathConditions()