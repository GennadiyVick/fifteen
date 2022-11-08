# Author Roganov G.V. roganovg@mail.ru
# License GNUGPL3 in LICENSE.txt file.
# Also see README.txt

class MvPiece:
    def __init__(self, piece, ledge, redge):
        self.piece = piece
        self.ledge = ledge
        self.redge = redge
        self.startX, self.startY = piece.pos().x(), piece.pos().y()
        self.cx = 0
        self.cy = 0

    def setPos(self, x,y):
        self.cx = x
        self.cy = y
        self.piece.setPos(x,y)

    #def status(self):
    #    return 1 if self.cx == self.redge else 0 if self

class HandMove:
    def __init__(self, pieces, mx, my, horizontal = True):
        self.pieces = pieces
        self.horizontal = horizontal
        self.mx = mx
        self.my = my
        self.canmove = True

    def contains(self, piece):
        for p in self.pieces:
            if p.piece == piece: return True
        return False

    def move(self, x,y):
        for piece in self.pieces:
            if self.horizontal:
                py = piece.startY
                px = piece.startX + x - self.mx
                if piece.ledge < piece.redge:
                    if px < piece.ledge+6:
                        px = piece.ledge
                    elif px > piece.redge-6:
                        px = piece.redge
                else:
                    if px < piece.redge+6:
                        px = piece.redge
                    elif px > piece.ledge-6:
                        px = piece.ledge
            else:
                px = piece.startX
                py = piece.startY + y - self.my
                if piece.ledge < piece.redge:
                    if py < piece.ledge+6:
                        py = piece.ledge
                    elif py > piece.redge-6:
                        py = piece.redge
                else:
                    if py < piece.redge+6:
                        py = piece.redge
                    elif py > piece.ledge-6:
                        py = piece.ledge
            piece.setPos(px,py)

    def checkfinish(self):
        piece = self.pieces[0]
        if self.horizontal:
            return 1 if piece.cx == piece.redge else 0 if piece.cx == piece.ledge else -1
        else:
            return 1 if piece.cy == piece.redge else 0 if piece.cy == piece.ledge else -1

    def setMatrix(self, plist):
        lpiece = plist[-1]
        lx = lpiece.matX
        ly = lpiece.matY
        lpiece.matX, lpiece.matY = self.pieces[-1].piece.matX, self.pieces[-1].piece.matY
        for i in range(len(self.pieces)-1,0,-1):
            self.pieces[i].piece.matX, self.pieces[i].piece.matY = self.pieces[i-1].piece.matX, self.pieces[i-1].piece.matY
        self.pieces[0].piece.matX, self.pieces[0].piece.matY = lx, ly


    @staticmethod
    def checkmove(plist, piece, mx, my, imagesize):
        x, y = piece.getMatPos()
        lpiece = plist[-1]
        lx,ly = lpiece.getMatPos()
        mvpieces = []
        horizontal = True
        ''' if you understand this ↓ code, and understand how to make it shorter, please let me know.  '''
        if ly == y:
            if x < lx:
                for i in range(lx-1,x-1,-1):
                    piec = plist.findByMPos(i,y)
                    if piec != None:
                        mvpiece = MvPiece(piec,piec.matX*imagesize,(i+1)*imagesize)
                        mvpieces.append(mvpiece)
            else:
                for i in range(lx+1,x+1):
                    piec = plist.findByMPos(i,y)
                    if piec != None:
                        mvpiece = MvPiece(piec,piec.matX*imagesize,(i-1)*imagesize)
                        mvpieces.append(mvpiece)
        elif lx == x:
            horizontal = False
            if y < ly:
                for i in range(ly-1,y-1,-1):
                    piec = plist.findByMPos(x,i)
                    if piec != None:
                        mvpiece = MvPiece(piec,piec.matY*imagesize,(i+1)*imagesize)
                        mvpieces.append(mvpiece)
            else:
                for i in range(ly+1,y+1):
                    piec = plist.findByMPos(x,i)
                    if piec != None:
                        mvpiece = MvPiece(piec,piec.matY*imagesize,(i-1)*imagesize)
                        mvpieces.append(mvpiece)
        else:
            return None

        if len(mvpieces) > 0:
            return HandMove(mvpieces,mx,my,horizontal)
        else:
            return None



