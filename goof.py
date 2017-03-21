import viz
viz.go(viz.STEREO)

texture = viz.add('ball.jpg')
quad = viz.addTexQuad(viz.SCREEN,align=viz.ALIGN_CENTER,pos=(0,0,0))
quad.texture(texture)