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


def loadscene():
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
	ground.texture(gr)
	
	global planeL, planeR

	#room
	wallR = vizshape.addPlane([75, 30])
	wallR.setPosition(10,0,-10)
	wallR.setEuler(x=0, y=90, z=0)

	wallL = vizshape.addPlane([75,30])
	wallL.setPosition(10,0,10)
	wallL.setEuler(x=0, y=-90, z=0)

	wallB = vizshape.addPlane([25, 30])
	wallB.setPosition(-20, 0, 0)
	wallB.setEuler(x=90, y=90, z=0)

	#destination point
	wallF = vizshape.addBox([10,0.5,20])
	wallF.setPosition(30,0,0)


	# initialize first plane
	planeL=vizshape.addBox([45,0.5,6])
	planeL.setPosition([2.5, 0, 6])
	planeL.texture(t1)

	# initialize second plane
	planeR=vizshape.addBox([45,0.5,6])
	planeR.setPosition([2.5, 0, -6])
	planeR.texture(t1)

	# initialize starting plane
	planeS = vizshape.addBox([10,0.5,6])
	planeS.setPosition([-10,0,0])

	sky = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
	skybox = viz.add('skydome.dlc')
	skybox.texture(sky)

	inLDoor = False
	inRDoor = False

	#Create proximity manager 
	manager = vizproximity.Manager()

	# Proximity sensor
	global rDoorSensor, lDoorSensor
	lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(16,1.5,6))
	rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(16,1.5,-6))

	# Add main viewpoint as proximity target 
	target = vizproximity.Target(viz.MainView)
	manager.addTarget(target)

	# Add collision
	viz.collision(viz.ON)

	# Add destination sensors to manager
	manager.addSensor(lDoorSensor)
	manager.addSensor(rDoorSensor)

	# Toggle debug shapes with keypress 
	vizact.onkeydown('l',manager.setDebug,viz.TOGGLE)
	
	manager.onEnter(None,enterProximity)
	
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