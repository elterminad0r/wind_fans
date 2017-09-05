from random import choice

def apply_to(l):
    def to_all(func):
        def f(*args, **kwargs):
            for i in list(l):
                func(i, *args, **kwargs)
        return f
    return to_all

def default(val, d):
    if val is not None:
        return val
    else:
        return d

def touches(x1, y1, x2, y2, r1, r2):
    return dist(x1, y1, x2, y2) < r1 + r2

class Fan(object):
    inst = []
    max_r = 80

    def __init__(self, x=None, y=None, r=None, n=None, c1=None, c2=None, dir=None):
        self._init(x, y, r, n, c1, c2, dir)
    
    def _init(self, x, y, r, n, c1, c2, dir, attempts=500):
        if attempts == 0:
            print("could not find position")
            return
        tx = default(x, random(self.max_r, width - self.max_r))
        ty = default(y, random(self.max_r, height - self.max_r))
        tr = default(r, random(self.max_r * 0.5, self.max_r))
        if any(touches(tx, ty, o.x, o.y, tr, o.r) for o in self.inst):
            if x is not None:
                print("invalid fan position")
                return
            else:
                self._init(x, y, r, n, c1, c2, dir, attempts - 1)
                return
        self.x = tx
        self.y = ty
        self.r = tr
        self.n = default(n, int(random(1, 4)))
        self.c1 = default(c1, random(255))
        self.c2 = default(c2, random(255))
        self.dir = default(dir, choice([-1, 1]))
        self.aofs = random(TWO_PI)
        self.av = 0
        
        self.inst.append(self)

    @staticmethod
    @apply_to(inst)
    def update(self):
        acc = map(constrain(dist(self.x, self.y, mouseX, mouseY), 0, 300), 0, 300, 0.002, 0)
        self.av += acc
        self.av *= 0.99
        self.aofs += self.av * self.dir
    
    @staticmethod
    @apply_to(inst)
    def draw(self):
        pushMatrix()
        translate(self.x, self.y)
        rotate(self.aofs)
        clip(-self.r, -self.r, self.r * 2, self.r * 2)
        for _ in range(2):
            for rot in xrange(0, self.n * 4, 2):
                fill(self.c1, 255, 255)
                for srot in range(2):
                    rotate(self.dir * -TWO_PI / float(self.n * 4))
                    ellipse(0, self.r * 0.5, self.r, self.r)
                    fill(self.c2, 255, 255)
            clip(-self.r, 0, self.r * 2, self.r)
            rotate(PI)
        popMatrix()
