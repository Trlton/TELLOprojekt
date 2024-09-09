from djitellopy import tello

lort = tello.Tello()
lort.takeoff()
lort.move_up(30)
lort.move_down(25)
lort.land()