"""
This script is really just a playground for things I haven't quite gotten the hang of yet.
"""
import viz
import vizfx
import vizact
import vizcam
import vizinfo
import vizconfig
import vizshape
viz.setMultiSample(8)
viz.fov(60)
viz.go()

# Setup info panel
info = vizinfo.InfoPanel()

# Setup camera navigation
cam = vizcam.PivotNavigate(distance=8.0, center=(0,1,0))

# Setup lighting
#viz.MainView.getHeadLight().remove()
mylight = viz.addLight() 
mylight.enable() 
mylight.position(25, 25, 10) 
mylight.spread(90) 
mylight.intensity(1)
#light = vizfx.addDirectionalLight(euler=(0,60,0))
vizfx.setAmbientColor([0.01,0.01,0.03])
stone = viz.addTexture('images/tile_stone.jpg', wrap=viz.REPEAT)

# Setup environment
vizfx.addChild('sky_day.osgb').renderToBackground()

# Setup models
# Section commented out because vizShape elements can't have fx applied.
# This is going to be quite a bit of work after all
fibpt = vizshape.addBox([1.0, 1.0, 1.0])
#flarght = vizfx.addChild(fibpt)
foo = vizfx.addChild('C:\Users\Cyan\Documents\Viz_envmts\Thesis-Navigation\Navigation-Experiment\p_wid_gravel.osgb')
logo = vizfx.addChild('logo.osgb')
logo.setPosition(0, 1.5, 0)
# Seems like simply saying a vizfx object has a texture is not enough.
# I'm going to have to apply it using a projector?
# Probably not. See code below:
'''


box = vizfx.addChild('basketball.osgb')

diffuse_map = viz.addTexture("pattern_66_diffuse.png") 
diffuse_map.wrap(viz.WRAP_T, viz.REPEAT)
diffuse_map.wrap(viz.WRAP_S, viz.REPEAT)
normal_map = viz.addTexture("pattern_66_normal.png")
normal_map.wrap(viz.WRAP_T, viz.REPEAT)
normal_map.wrap(viz.WRAP_S, viz.REPEAT)
specular_map = viz.addTexture("pattern_66_specular.png")
specular_map.wrap(viz.WRAP_T, viz.REPEAT)
specular_map.wrap(viz.WRAP_S, viz.REPEAT)
material = vizfx.addMaterialEffect(
    Diffuse(diffuse_map, 0), Bump(normal_map, 1), Specular(specular_map, 2)
)
box.apply(material)
'''

'''
Weird inconsistencies between sizes in Blender/Collada
generated files, OSGB and 3DS Max. Meters in 3DS Max do
not correspond with meters when imported to Vizard.
It seems that the sizes are reduced by a factor of about
40.

As such, I've taken the dimensions of Blender generated
models and am recording them here:
Narrow
X: 1574.803
Y: 118.11
Z: 19.685

Medium
X: 1574.803
Y: 236.22
Z: 19.685

Wide
X: 1574.803
Y: 314.96
Z: 19.685
'''

diffuse_map = viz.addTexture('196.jpg') 
diffuse_map.wrap(viz.WRAP_T, viz.REPEAT)
diffuse_map.wrap(viz.WRAP_S, viz.REPEAT)
normal_map = viz.addTexture('196_norm.jpg')
normal_map.wrap(viz.WRAP_T, viz.REPEAT)
normal_map.wrap(viz.WRAP_S, viz.REPEAT)
#specular_map = viz.addTexture("pattern_66_specular.png")
#specular_map.wrap(viz.WRAP_T, viz.REPEAT)
#specular_map.wrap(viz.WRAP_S, viz.REPEAT)
material = vizfx.addMaterialEffect(
    vizfx.Diffuse(diffuse_map, 0), vizfx.Bump(normal_map, 1)
)

foo.specular([0.1,0.1,0.1] ) # Make this matte
foo.apply(material) # Apply diffuse and normal map



#logo.apply(diffuseeffect)

#def PickModel():
#
#	# Check which node was picked
#	node = viz.pick()
#	if node in models:
#
#		# Remove highlight effect from all existing nodes
#		pulseEffect.unapply()
#
#		# Apply effect to selected node
#		node.apply(pulseEffect)
#
#vizact.onmousedown(viz.MOUSEBUTTON_LEFT, PickModel)