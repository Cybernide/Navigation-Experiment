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
import forktest

if __name__ == '__main__':
	forktest.loadscene()

# Proximity callback function that records if the user has entered the proximity of an avatar.  
# Entering avatar proxim	ity indicates the user did not avoid the avatar and sets the corresponding  
# trial variable to False   
		
def setPathConditions():
	
	# Clear planeL and planeR
	planeL.remove()
	planeR.remove()
	
	pathcond = sample(xrange(3),2)
	for i in pathcond:
		if i == 0:
			# change width of path
			pathgen = randint(0,5)
			changePathWidth(pathgen)
		elif i == 1:
			# change incline of path
			pathgen = randint(0,5)
			inclinePath(pathgen)
		elif i == 2:
			# change texture of 
			pathgen = randint(0,7)
			changePathTexture(pathgen)
			
def changePathWidth(path):
	global planeL
	global planeR
	
	# Clear planeL and planeR
	
	if path == 0:
		# Left is narrow
		planeL=vizshape.addBox([50,2,3])
		planeL.setPosition([6, 0, 4.5])
		planeL.texture(t1)
		# Right is baseline
		planeR=vizshape.addBox([50,2,6])
		planeR.setPosition([6.0, 0, -6])
		planeR.texture(t1)		
		
	elif path == 1:
		# Left is baseline, right is narrow
		planeL=vizshape.addBox([50,2,6])
		planeL.setPosition([6.0, 0, 6])
		planeL.texture(t1)
		# right is narrow
		planeR=vizshape.addBox([50,2,3])
		planeR.setPosition([6, 0, -4.5])
		planeR.texture(t1)
		
	elif path == 2:
		# Left is wide, 
		planeL=vizshape.addBox([50,2,12])
		planeL.setPosition([6.0, 0, 9])
		planeL.texture(t1)
		# right is baseline
		planeR=vizshape.addBox([50,2,6])
		planeR.setPosition([6.0, 0, -6])
		planeR.texture(t1)
		
	elif path == 3:
		# Left is baseline,
		planeL=vizshape.addBox([50,2,6])
		planeL.setPosition([6.0, 0, 6])
		planeL.texture(t1)
		#right is wide
		planeR=vizshape.addBox([50,2,12])
		planeR.setPosition([6.0, 0, -9])
		planeR.texture(t1)
		
	elif path == 4:
		# Left is narrow
		planeL=vizshape.addBox([50,2,3])
		planeL.setPosition([6, 0, 4.5])
		planeL.texture(t1)
		# Right is wide
		planeR=vizshape.addBox([50,2,12])
		planeR.setPosition([6, 0, -9])
		planeR.texture(t1)
		
	elif path == 5:
		# Left is wide, 
		planeL=vizshape.addBox([50,2,12])
		planeL.setPosition([6, 0, 9])
		planeL.texture(t1)
		# right is narrow
		planeR=vizshape.addBox([50,2,3])
		planeR.setPosition([6, 0, -4.5])
		planeR.texture(t1)

def inclinePath(path):
	global planeL
	global planeR
	
	# Clear planeL and planeR
	
	if path == 0:
		# Left inclines down, right is baseline
		# initialize first plane
		
		if not planeL:
			planeL=vizshape.addBox([50,2,6])
			planeL.setPosition([6.0, 0, 6])
			planeL.texture(t1)
		planeL.setEuler([0,0,-20])
		# initialize second plane
		
		if not planeR:
			planeR=vizshape.addBox([50,2,6])
			planeR.setPosition([6.0, 0, -6])
			planeR.texture(t1)
		
	elif path == 1:
		# Left is baseline, right inclines down
		if not planeL:
			planeL=vizshape.addBox([50,2,6])
			planeL.setPosition([6.0, 0, 6])
			planeL.texture(t1)
		
		if not planeR:
			planeR=vizshape.addBox([50,2,6])
			planeR.setPosition([6.0, 0, -6])
			planeR.texture(t1)
		planeR.setEuler([0,0,-20])
		
	elif path == 2:
		# Left inclines up, right is baseline
		if not planeL:
			planeL=vizshape.addBox([50,2,6])
			planeL.setPosition([6.0, 0, 6])
			planeL.texture(t1)
		planeL.setEuler([0,0,20]) # incline up
		
		if not planeR:
			planeR=vizshape.addBox([50,2,6])
			planeR.setPosition([6.0, 0, -6])
			planeR.texture(t1)
			
	elif path == 3:
		# Left is baseline, right inclines up
		if not planeL:
			planeL=vizshape.addBox([50,2,6])
			planeL.setPosition([6.0, 0, 6])
			planeL.texture(t1)
		
		if not planeR:
			planeR=vizshape.addBox([50,2,6])
			planeR.setPosition([6.0, 0, -6])
			planeR.texture(t1)
		planeR.setEuler([0,0,20]) # incline up
			
	elif path == 4:
		# Left inclines down, right inclines up
		if not planeL:
			planeL=vizshape.addBox([50,2,6])
			planeL.setPosition([6.0, 0, 6])
			planeL.texture(t1)
		planeL.setEuler([0,0,-20])
		
		if not planeR:
			planeR=vizshape.addBox([50,2,6])
			planeR.setPosition([6.0, 0, -6])
			planeR.texture(t1)
		planeR.setEuler([0,0,20])
		
	elif path == 5:
		# Left inclines up, right inclines down
		if not planeL:
			planeL=vizshape.addBox([50,2,6])
			planeL.setPosition([6.0, 0, 6])
			planeL.texture(t1)
		planeL.setEuler([0,0,20])
		
		if not planeR:
			planeR=vizshape.addBox([50,2,6])
			planeR.setPosition([6.0, 0, -6])
			planeR.texture(t1)
		planeR.setEuler([0,0,-20])
		
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

def curvePath(path):
	if path == 0:
		# Left is curved, right is straight
		return None
	elif path == 1:
		# Left is straight, right is curved
		return None



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
