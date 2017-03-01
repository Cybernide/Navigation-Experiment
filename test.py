import viz
import viztask
viz.go()

viz.add('dojo.osgb')

def ZoomTask():

    viz.fov(60)

    zoom_in = vizact.mix(60, 20, time=0.5, interpolate=vizact.easeOutStrong)
    zoom_out = vizact.mix(20, 60, time=0.5, interpolate=vizact.easeOutStrong)

    while True:

        yield viztask.waitKeyDown(' ')

        yield viztask.waitCall(viz.fov,zoom_in)

        yield viztask.waitKeyDown(' ')

        yield viztask.waitCall(viz.fov,zoom_out)


viztask.schedule( ZoomTask() )