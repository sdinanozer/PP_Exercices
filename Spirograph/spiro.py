'''
A program that simulates a Sprirograph.

Original author: Mahesh Venkitachalam
'''

import turtle
import fractions
import math

#Class for drawing a spirograph
class Spiro:
    def __init__(self, xc, yc, color, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape('turtle')

        self.step = 5
        self.drawing_complete = False

        self.set_params(xc, yc, color, R, r, l)

        self.restart()

    def set_params(self, xc, yc, color, R, r, l):
        self.xc = xc
        self.yc = yc
        self.color = color
        self.R = int(R)
        self.r = int(r)
        self.l = l

        gcd_val = fractions.gcd(self.r, self.R)
        self.rots = self.r // gcd_val
        self.k = r / float(R)

        self.t.color(*color)

        self.angle = 0

    def restart(self):
        self.drawing_complete = False
        self.t.showturtle()
        self.t.up()

        R, k, l = self.R, self.k, self.l

        a = 0.0
        x = R*((l-k)*math.sin(a) + l*k*math.cos((l - k)*a/k))
        y = R*((l-k)*math.cos(a) + l*k*math.sin((l - k)*a/k))

        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        R, k, l = self.R, self.k, self.l

        for i in range(0, 360*self.rots + 1, self.step):
            a = math.radians(i)
            x = R*((l-k)*math.cos(a) + l*k*math.cos((l - k)*a/k))
            y = R*((l-k)*math.sin(a) + l*k*math.sin((l - k)*a/k))

            self.t.setpos(self.xc + x, self.yc + y)
        
        self.t.hideturtle()

    def update(self):
        if self.drawing_complete:
            return
        
        self.angle += self.step
        R, k, l = self.R, self.k, self.l

        a = math.radians(self.angle)
        x = R*((l-k)*math.cos(a) + l*k*math.cos((l - k)*a/k))
        y = R*((l-k)*math.sin(a) + l*k*math.sin((l - k)*a/k))

        self.t.setpos(self.xc + x, self.yc + y)

        if self.angle >= 360*self.rots:
            self.drawing_complete = True
            self.t.hideturtle()
