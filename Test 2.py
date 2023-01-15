from PyQt5.QtCore import *

def mirror_point_on_line (p: QPoint, l: QLine):
    x1, y1 = p.x(), p.y()
    x2, y2 = l.p1().x(), l.p1().y()
    x3, y3 = l.p2().x(), l.p2().y()
    dx, dy = x2 - x1, y2 - y1
    det = dx * dx + dy * dy
    a = (dy * (y3 - y1) + dx * (x3 - x1)) / det

    s = QPoint(int(x1 + a * dx), int(y1 + a * dy))
    return (s-p)*2 +p

point = QPoint(1,1)
l1 = QPoint(3,0)
l2 = QPoint(3,3)
line = QLine(l1, l2)

print(mirror_point_on_line(point, line))