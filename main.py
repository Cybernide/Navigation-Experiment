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
from random import randint



viz.go()

#set graphical parameters
viz.setMultiSample(4)
viz.fov(60)
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
t1 = viz.addTexture('images/tile_stone.jpg', wrap=viz.REPEAT)
grass = viz.addTexture('images/tile_grass.jpg', wrap=viz.REPEAT)

# Add white point light 
light = vizfx.addPointLight(color=viz.WHITE, pos=(0,2,2))

# Add ground
ground = viz.addChild('ground.osgb')
ground.texture(grass)

#Set fog color to gray 
viz.fogcolor(0.5,0.5,0.5) 

#Use linear fog that start from 1 meter in front of the user 
#And at 10 meters in front of the user 
viz.fog(1,10)

# initialize first plane
planeL=vizshape.addBox([50,2,6])
planeL.setPosition([6.0, 0, 6])
planeL.texture(t1)

# initialize second plane
planeR=vizshape.addBox([50,2,6])
planeR.setPosition([6.0, 0, -6])
planeR.texture(t1)

# initialize starting plane
planeS = vizshape.addBox([10,2,6])
planeS.setPosition([-10,0,0])

sky = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')

skybox = viz.add('skydome.dlc')
skybox.texture(sky)

inLDoor = False
inRDoor = False

#Create proximity manager 
manager = vizproximity.Manager()

# Proximity sensor
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

# Proximity callback function that records if the user has entered the proximity of an avatar.  
# Entering avatar proximity indicates the user did not avoid the avatar and sets the corresponding  
# trial variable to False   
def enterProximity(event):
	"""@args vizproximity.ProximityEvent()"""
	global inLDoor, inRDoor
	if event.sensor == lDoorSensor:
		inLDoor = True
		viz.MainView.setPosition([-9, 2, 0])
	elif event.sensor == rDoorSensor:
		inRDoor = True
		viz.MainView.setPosition([-9, 2, 0])
		
def setPathConditions():
	pathcond = sample(xrange(5),2)
	for i in pathcond:
		if i == 0:
			pathgen = randint(0,5)
			changePathWidth(pathgen)
		elif i == 1:
			pathgen = randint(0,5)
			inclinePath(pathgen)
		elif i == 2:
			pathgen = randint(0,1)
			setPathFriction(pathgen)
		elif i == 3:
			pathgen = randint(0,1)
			changePathTexture(pathgen)
		elif i == 4:
			pathgen = randint(0,1)
			curvePath(pathgen)
			
def changePathWidth(path):
	if path == 0:
		# Left is narrow, right is baseline
		return None
	elif path == 1:
		# Left is baseline, right is narrow
		return None
	elif path == 2:
		# Left is wide, right is baseline
		return None
	elif path == 3:
		# Left is baseline, right is wide
		return None
	elif path == 4:
		# Left is narrow, right is wide
		return None
	elif path == 5:
		# Left is wide, right is narrow
		return None
def inclinePath(path):
	if path == 0:
		# Left inclines down, right is baseline
		return None
	elif path == 1:
		# Left is baseline, right inclines down
		return None
	elif path == 2:
		# Left inclines up, right is baseline
		return None
	elif path == 3:
		# Left is baseline, right inclines up
		return None
	elif path == 4:
		# Left inclines down, right inclines up
		return None
	elif path == 5:
		# Left inclines up, right inclines down
		return None
def setPathFriction(path):
	if path == 0:
		# Left is shiny, right is matte
		return None
	elif path == 1:
		# Left is matte, right is shiny
		return None
def changePathTexture(path):
	if path == 0:
		# Left is packed, right is loose
		return None
	elif path == 1:
		# Right is packed, left is loose
		return None
def curvePath():
	if path == 0:
		# Left is curved, right is straight
		return None
	elif path == 1:
		# Left is straight, right is curved
		return None

manager.onEnter(None,enterProximity)

''' Path considerations
Width conditions (mutually exclusive):
path width - L0.5x, R0x; L0x, R0.5x; L2x, R0x; L0x, R2x; L0.5x, R2x; L2x, R0.5x
6 possibilities

Incline conditions (mutually exclusive)
incline -- L-20, R0; L0, R-20; L20, R0; R20, L0; L-20, R20; L20, R-20
6 possibilities

Friction conditions(mutually exclusive)
friction -- Lshiny, Rmatte; Lmatte, Rshiny
2 possibilities

Texture conditions
texture -- Lpacked, Rloose; Lloose, Rpacked
2 possibilities

Path conditions 
curve -- Lcurved, Rstraight; Lstraight, Rcurved
2 possibilities

'''

#plane_.setEuler([0,0,20]) # incline up
#plane_.setEuler([0,0,-20]) # incline down
