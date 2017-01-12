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

# Assets directory
asset_dir = "C:\Users\Cyan\Documents\Viz_envmts\Thesis-Navigation\Navigation-Experiment\\"

def loadscene(inc, tex):
	print 'incline = ' + str(inc)
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
	keycam = vizcam.KeyboardCamera()
	keycam.sensitivity(3,1)
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

	# Add white point light 
	#light = vizfx.addPointLight(color=viz.WHITE, pos=(0,1,1))

	# Add ground
	ground = viz.addChild('ground.osgb')
	ground.texture(tile)
	
	global plankL, plankR

	#room
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

	wallB = vizshape.addPlane([25, 30])
	wallB.setPosition(-22.25, 0, 0)
	wallB.setEuler(x=90, y=90, z=0)
	wallB.texture(metal)
	
	ceiling = vizshape.addPlane([75,30])
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
	
	model_plankL = "p_mid_rubber"
	model_plankR = "p_mid_rubber"

	
	'''
	#friction conditions
	0. Lshiny, Rmatte
	1. Lmatte, Rshiny
	'''
	if (fri == 0):
		plankL.specular(0.3, 0.3, 0.3)
	elif (fri == 1):
		plankR.specular(0.3, 0.3, 0.3)

		
	plankL = vizfx.addChild(asset_dir + model_plankL + ".osgb")
	plankR = vizfx.addChild(asset_dir + model_plankR + ".osgb")
	
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
	
	if (inc == 0) or (inc == 4):
		plankL.setEuler([90,20,0])
	if (inc == 2) or (inc == 5):
		plankL.setEuler([90,-20,0])
	elif (inc == 1) or (inc == 3) or (inc == 6):
		plankL.setEuler([90,0,0])
	
	# initialize second plane
	if (inc == 1) or (inc == 5):
		plankR.setEuler([90,20,0])
	if (inc == 3) or (inc == 4):
		plankR.setEuler([90,-20,0])
	elif (inc == 0) or (inc == 2) or (inc == 6):
		plankR.setEuler([90,0,0])
	
	
	
# initialize starting plane
	if inc == 0:
		
		wallR = vizshape.addPlane([75, 30])
		wallR.setPosition(10,0,-10)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)

		wallL = vizshape.addPlane([75,30])
		wallL.setPosition(10,0,10)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)
		#destination point
		plankL.setPosition([1.25, -6.8, 6])
		plankR.setPosition([2.5, 0, -6])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		floorT1 = vizshape.addBox([25,0.5,25])
		floorT1.setPosition(35,0,0)
		floorT2 = vizshape.addBox([25,0.5,25])
		floorT2.setPosition(32.5,-13.75,0)
	
		wallTT = vizshape.addBox([25,6,25])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(35,7,0)
		wallTT.texture(metal)
	
		wallTl = vizshape.addBox([0.25,4,15])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(22.75,2,2.5)
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
	
		wallTTr = vizshape.addBox([0.25,4,3])
		wallTTr.setEuler(0,0,0)
		wallTTr.setPosition(22.75,2.25,-8.75)	
		wallTTr.texmat(texMwallTlr)
		wallTTr.texture(tile)
		
		wallTBl = vizshape.addBox([0.25,4.25,3])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(22.75,-11.5,8.75)	
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
		
		wallTBr = vizshape.addBox([0.25,4.25,15])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(22.75,-11.5,-2.75)
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTc = vizshape.addBox([0.25,9.25,20])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(22.75,-4.75,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
	
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		ground.setPosition([0, -14., 0])
		plankStart = vizshape.addBox([5,0.5,18])
		plankStart.setPosition([-20,0,0])
		
		doorL.setPosition(22.5,-11.5,4.75)
		doorR.setPosition(22.5,2.0,-7.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,-10.5,6))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,-6))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,-10.5,6))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,-6))

		#change the origin and where door will rotate
		
	if inc == 1:
		wallR = vizshape.addPlane([75, 30])
		wallR.setPosition(10,0,-10)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)

		wallL = vizshape.addPlane([75,30])
		wallL.setPosition(10,0,10)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)
		
		plankL.setPosition([2.5, 0, 6])
		plankR.setPosition([1.25, -6.8, -6])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		floorT1 = vizshape.addBox([25,0.5,25])
		floorT1.setPosition(35,0,0)
		floorT2 = vizshape.addBox([25,0.5,25])
		floorT2.setPosition(35,-13.75,0)
	
		wallTT = vizshape.addBox([25,6,25])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(35,7,0)
		wallTT.texture(metal)
	
		wallTBl = vizshape.addBox([0.25,4.25,15])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(22.75,-11.5,2.5)
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
	
		wallTBr = vizshape.addBox([0.25,4.25,3])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(22.75,-11.5,-8.75)	
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
		
		wallTl = vizshape.addBox([0.25,4,3])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(22.75,2.25,8.75)	
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
		
		wallTr = vizshape.addBox([0.25,4,15])
		wallTr.setEuler(0,0,0)
		wallTr.setPosition(22.75,2.25,-2.75)
		wallTr.texmat(texMwallTlr)
		wallTr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTc = vizshape.addBox([0.25,9.25,20])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(22.75,-4.75,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
	
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		ground.setPosition([0, -14., 0])
		plankStart = vizshape.addBox([5,0.5,18])
		plankStart.setPosition([-20,0,0])
		
		doorL.setPosition(22.5,2.0,4.75)
		doorR.setPosition(22.5,-11.5,-7.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,6))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,-10.5,-6))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,6))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,-10.5,-6))
		
	if inc == 2:
		wallR = vizshape.addPlane([75, 30])
		wallR.setPosition(10,0,-10)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)

		wallL = vizshape.addPlane([75,30])
		wallL.setPosition(10,0,10)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)
		plankL.setPosition([1.25, -7.0, 6])
		plankR.setPosition([2.5, -13.5, -6])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTF1 = vizshape.addBox([25,0.5,25])
		wallTF1.setPosition(32.5,0,0)
		wallTF2 = vizshape.addBox([25,0.5,25])
		wallTF2.setPosition(35,-13.75,0)
	
		wallTT = vizshape.addBox([25,6,25])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(35,7,0)
		wallTT.texture(metal)
	
		wallTBl = vizshape.addBox([0.25,4.25,15])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(22.75,-11.5,2.5)
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
	
		wallTBr = vizshape.addBox([0.25,4.25,3])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(22.75,-11.5,-8.75)	
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
		
		wallTl = vizshape.addBox([0.25,4,3])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(22.75,2.25,8.75)	
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
		
		wallTr = vizshape.addBox([0.25,4,15])
		wallTr.setEuler(0,0,0)
		wallTr.setPosition(22.75,2.25,-2.75)
		wallTr.texmat(texMwallTlr)
		wallTr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTc = vizshape.addBox([0.25,9.25,20])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(22.75,-4.75,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
	
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		ground.setPosition([0, -14., 0])
		plankStart = vizshape.addBox([5,0.5,18])
		planeStart.setPosition([-20,-13.5,0])
		
		doorL.setPosition(22.5,2.0,4.75)
		doorR.setPosition(22.5,-11.25,-7.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,6))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,-10.5,-6))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,6))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,-10.5,-6))
		
	if inc == 3:
		wallR = vizshape.addPlane([75, 30])
		wallR.setPosition(10,0,-10)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)

		wallL = vizshape.addPlane([75,30])
		wallL.setPosition(10,0,10)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)
		plankL.setPosition([2.5, -13.75, 6])
		plankR.setPosition([1.25, -7.0, -6])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTF1 = vizshape.addBox([25,0.5,25])
		wallTF1.setPosition(32.5,0,0)
		wallTF2 = vizshape.addBox([25,0.5,25])
		wallTF2.setPosition(35,-13.75,0)
	
		wallTT = vizshape.addBox([25,6,25])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(35,7,0)
		wallTT.texture(metal)
	
		wallTl = vizshape.addBox([0.25,4,15])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(22.75,2,2.5)
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
	
		wallTTr = vizshape.addBox([0.25,4,3])
		wallTTr.setEuler(0,0,0)
		wallTTr.setPosition(22.75,2.25,-8.75)	
		wallTTr.texmat(texMwallTlr)
		wallTTr.texture(tile)
		
		wallTBl = vizshape.addBox([0.25,4.25,3])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(22.75,-11.5,8.75)	
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
		
		wallTBr = vizshape.addBox([0.25,4.25,15])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(22.75,-11.5,-2.75)
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTc = vizshape.addBox([0.25,9.25,20])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(22.75,-4.75,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
	
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		ground.setPosition([0, -14., 0])
		plankStart = vizshape.addBox([5,0.5,18])
		plankStart.setPosition([-20,-13.75,0])
		
		doorL.setPosition(22.5,-11.5,4.75)
		doorR.setPosition(22.5,2.0,-7.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,-10.5,6))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,-6))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,-10.5,6))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,-6))
	if inc == 4:
		wallR = vizshape.addPlane([75, 40])
		wallR.setPosition(10,-10,-10)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)

		wallL = vizshape.addPlane([75,40])
		wallL.setPosition(10,-10,10)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)		
		
		plankL.setPosition([1.25, -20.75, 6])
		plankR.setPosition([1.25, -7.0, -6])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTF1 = vizshape.addBox([25,0.5,25])
		wallTF1.setPosition(32.5,0,0)
		wallTF2 = vizshape.addBox([25,0.5,25])
		wallTF2.setPosition(32.5,-27,0)
	
		wallTT = vizshape.addBox([25,6,25])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(35,7,0)
		wallTT.texture(metal)
	
		wallTl = vizshape.addBox([0.25,4,15])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(22.75,2,2.5)
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
	
		wallTTr = vizshape.addBox([0.25,4,3])
		wallTTr.setEuler(0,0,0)
		wallTTr.setPosition(22.75,2.25,-8.75)	
		wallTTr.texmat(texMwallTlr)
		wallTTr.texture(tile)
		
		wallTBl = vizshape.addBox([0.25,4,3])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(22.75,-25.25,8.75)	
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
		
		wallTBr = vizshape.addBox([0.25,4,15])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(22.75,-25.25,-2.75)
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTc = vizshape.addBox([0.25,23,20])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(22.75,-11.25,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
	
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		wallTceilB = vizshape.addBox([25,0.5,25])
		wallTceilB.setPosition(35,-23,0)
		
		ground.setPosition([0, -27.5, 0])
		plankStart = vizshape.addBox([5,0.5,18])
		plankStart.setPosition([-20,-14.0,0])
		
		doorL.setPosition(22.5,-25.25,4.75)
		doorR.setPosition(22.5,2.0,-7.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,-24.5,6))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,-6))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,-24.5,6))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,-6))
		
	elif inc == 5:
		wallR = vizshape.addPlane([75, 40])
		wallR.setPosition(10,-10,-10)
		wallR.setEuler(x=0, y=90, z=0)
		wallR.texture(metal)

		wallL = vizshape.addPlane([75,40])
		wallL.setPosition(10,-10,10)
		wallL.setEuler(x=0, y=-90, z=0)
		wallL.texture(metal)		
		
		plankL.setPosition([1.25, -7.0, 6])
		plankR.setPosition([1.25, -20.75, -6])
		
		texMwallTlr = vizmat.Transform()
		texMwallTlr.setScale( [1*0.35,2.5*0.4,1*0.35] )
	
		texMwallTc = vizmat.Transform()
		texMwallTc.setScale( [1,1,1.3] )
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTF1 = vizshape.addBox([25,0.5,25])
		wallTF1.setPosition(32.5,0,0)
		wallTF2 = vizshape.addBox([25,0.5,25])
		wallTF2.setPosition(32.5,-27,0)
	
		wallTT = vizshape.addBox([25,6,25])
		wallTT.setEuler(0,0,0)
		wallTT.setPosition(35,7,0)
		wallTT.texture(metal)
	
		wallTl = vizshape.addBox([0.25,4,3])
		wallTl.setEuler(0,0,0)
		wallTl.setPosition(22.75,2,8.75)
		wallTl.texmat(texMwallTlr)
		wallTl.texture(tile)
	
		wallTTr = vizshape.addBox([0.25,4,15])
		wallTTr.setEuler(0,0,0)
		wallTTr.setPosition(22.75,2.25,-2.75)	
		wallTTr.texmat(texMwallTlr)
		wallTTr.texture(tile)
		
		wallTBl = vizshape.addBox([0.25,4,15])
		wallTBl.setEuler(0,0,0)
		wallTBl.setPosition(22.75,-25.25,2.75)	
		wallTBl.texmat(texMwallTlr)
		wallTBl.texture(tile)
		
		wallTBr = vizshape.addBox([0.25,4,3])
		wallTBr.setEuler(0,0,0)
		wallTBr.setPosition(22.75,-25.25,-8.75)
		wallTBr.texmat(texMwallTlr)
		wallTBr.texture(tile)
	
		tile.wrap(viz.WRAP_T, viz.REPEAT)
		tile.wrap(viz.WRAP_S, viz.REPEAT)
	
		wallTc = vizshape.addBox([0.25,23,20])
		wallTc.setEuler(0,0,0)
		wallTc.setPosition(22.75,-11.25,0.0)
		wallTc.texmat(texMwallTc)
		wallTc.texture(tile)
	
		wallTb = vizshape.addPlane([20,4])
		wallTb.setPosition(40, 2, 0)
		wallTb.setEuler(x=90, y=270, z=0)
		
		wallTceilB = vizshape.addBox([25,0.5,25])
		wallTceilB.setPosition(35,-23,0)
		
		ground.setPosition([0, -27.5, 0])
		plankStart = vizshape.addBox([5,0.5,18])
		plankStart.setPosition([-20,-14.0,0])
		
		doorL.setPosition(22.5,2.0,4.75)
		doorR.setPosition(22.5,-25.25,-7.25)
		
		lDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,1.5,6))
		rDoorSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(27,-24.5,-6))
		
		lDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,1.5,6))
		rDoorOpenSensor = vizproximity.Sensor(vizproximity.Box([5,5,5]),source=viz.Matrix.translate(22,-24.5,-6))
		
		
	
	
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