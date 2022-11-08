# Author Roganov G.V. roganovg@mail.ru
# License GNUGPL3 in LICENSE.txt file.
# Also see README.txt
from PyQt5.QtCore import QPointF

class Animate:
    def __init__(self,piece,startValue,stopValue, steps = 6):
        self.curstep = 0
        self.steps = steps
        self.finished = False
        self.piece = piece
        self.stopvalue = stopValue
        self.value = startValue
        self.step = (stopValue - startValue) / steps

    def doStep(self):
        self.curstep += 1
        if self.curstep == self.steps:
            self.finished = True
        self.value = self.stopvalue if self.finished else self.value + self.step
        self.piece.setPos(self.value)


class AniStack(list):
    def __init__(self):
        super(AniStack,self).__init__()
        self.lastvalue = None

    def addAni(self,piece,startvalue,stopvalue, maxsteps = 6):
        sv = startvalue
        if len(self)>0:
            sv = self.lastvalue
        self.lastvalue = stopvalue
        if stopvalue == sv: return
        a = Animate(piece,sv,stopvalue,maxsteps)
        self.append(a)

    def doStep(self):
        stop = True
        if len(self) > 0:
            a = self[0]
            a.doStep()
            if a.finished:
                self.pop(0)
            if len(self) > 0:
                stop = False
        return stop
