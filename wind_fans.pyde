from Fan import Fan

def setup():
    size(800, 800)
    for _ in range(20):
        Fan()

def draw():
    background(0)
    colorMode(HSB, 255, 255, 255)
    noStroke()
    Fan.update()
    Fan.draw()