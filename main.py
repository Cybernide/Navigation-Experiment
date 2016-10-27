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
import widtex

if __name__ == '__main__':
	widtex.loadscene(6,6)
		
def run_initPathConditions():
	
	pathcond = sample(xrange(3),2)
#	for i in pathcond:
#		if i == 0:
#			pathgen = randint(0,5)
#			changePathWidth(pathgen)
#		elif i == 1:
#			pathgen = randint(0,5)
#			inclinePath(pathgen)
#		elif i == 2:
#			pathgen = randint(0,5)
#			setPathTexture(pathgen)
	genwid = randint(0,5)
	gentex = randint(0,5)
	widtex.loadscene(genwid, gentex)
#	if (0 in pathcond) and (2 in pathcond):
#		genwid = randint(0,5)
#		gentex = randint(0,5)
#		widtex.loadscene(genwid, gentex)
#	else:
#		widtex.loadscene(6, 6)
#		print 'IMPLEMENT ME!'
'''	

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

'''

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

Updated texture
texture -- Lrubber, Rstone; Lstone, Rrubber; Lrubber, Rgravel; Lgravel, Rrubber; Lstone, Rgravel; Rgravel, Lstone;

'''

#plane_.setEuler([0,0,20]) # incline up
#plane_.setEuler([0,0,-20]) # incline down
