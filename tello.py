from djitellopy import tello

lort = tello.Tello()
lort.takeoff()
lort.move_up(10)
lort.move_forward(20)

lort.move_back(30)
lort.land()
#hej