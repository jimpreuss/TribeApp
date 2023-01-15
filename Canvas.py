from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QWheelEvent, QPixmap
from PyQt5.QtCore import QPoint, Qt, QRect

class Canvas(QLabel):

    def __init__(self, space: int, pixmap = QPixmap):
        super().__init__()
        self.zoom: float = 1
        self.space: int = space
        self.large_pixmap: QPixmap = pixmap
        self.center = QPoint(self.large_pixmap.width()/2, self.large_pixmap.height()/2)

    def wheelEvent(self, e: QWheelEvent) -> None:
        angl = e.angleDelta()
        pos = e.position()
        # print(angl)
        # print(pos)
        # print(f" 1 Center before: {self.center} Set X to: {self.center.x()+e.angleDelta().x()}")


        modifier = QApplication.keyboardModifiers()
        if modifier == Qt.ControlModifier:
            old_zoom = self.zoom
            self.zoom = min(max(self.zoom * self.calculate_zoom(e.angleDelta().y()), 0), 1)
            # Move Center point to let Mouse stay in Place
            x = e.position().x()
            y = e.position().y()
            # Translate mouse Position from origin at 0/0 to orgin at Center
            x -= self.width()/2
            y -= self.height()/2
            # Translate mouse position on canvas to mouse position on large_pixmap
            # x = old_zoom*x -self.zoom*x
            # y = old_zoom * y - self.zoom * y
            x *= self.zoom
            y *= self.zoom

            self.center.setX(self.center.x() + x)
            self.center.setY(self.center.y()+y)


            self.pixmap().height()
            self.pixmap().width()

        else:
            self.center.setX(self.center.x()+e.angleDelta().x()*5)
            self.center.setY(self.center.y()+e.angleDelta().y())

        # print(f" 2 Center: {self.center} Zoom: {self.zoom}")
        self.setPixmap(self.large_pixmap)
        # print(f" 3 Center: {self.center} Zoom: {self.zoom}")

    def setPixmap(self, pixmap: QPixmap) -> None:
        # Recalculate Center base on percentage
        perc_width = self.center.x()/ self.large_pixmap.width()
        perc_height = self.center.y()/ self.large_pixmap.height()
        # print(f"perc width/ height {perc_width}/ {perc_height}")
        # Set Large Map
        self.large_pixmap = pixmap
        # Set New Center Point about where the old one was
        self.center = QPoint(int(self.large_pixmap.width()*perc_width), int(self.large_pixmap.height()*perc_height))
        # print(f" 4 Center: {self.center} Zoom: {self.zoom}")

        # Calculate max cut width, not smaller than the pixels available to the canvas
        cut_width = max(self.width(),self.large_pixmap.width()*self.zoom)
        cut_height = max(self.height(),self.large_pixmap.height()*self.zoom)

        # Is there space on the Canvas horizontally
        if cut_width/cut_height < self.width()/self.height():
            # Add width
            cut_width = min(cut_height / self.height() * self.width(), self.large_pixmap.width())
        else:
            # Add height to cut
            cut_height = min(cut_width / self.width() * self.height(), self.large_pixmap.height())


        # Move Center Point so that the cut does not fall out of the pixmap
        min_c_x = cut_width/2
        max_c_x = self.large_pixmap.width() - cut_width/2
        min_c_y = cut_height/2
        max_c_y = self.large_pixmap.height() - cut_height/2
        self.center.setX(min(max_c_x,max(min_c_x, self.center.x())))
        self.center.setY(min(max_c_y,max(min_c_y, self.center.y())))


        # Cut Pixmap
        rect = QRect(self.center.x()-cut_width/2, self.center.y()-cut_height/2, cut_width, cut_height)
        cut_pixmap = self.large_pixmap.copy(rect)

        max_width = self.width()- self.space *2
        max_height = self.height()

        org_width = cut_pixmap.width()
        org_height = cut_pixmap.height()

        if org_width/max_width < org_height/max_height:
            height = max_height
            width = max_height * (org_width/org_height)
        else:
            width = max_width
            height = max_width * (org_height/org_width)
        current_pixmap = cut_pixmap.scaled(width, height)

        super().setPixmap(current_pixmap)

    def calculate_zoom(self, w: int):
        f = 1000
        if w == 0:
            return 1
        elif w > 0:
            return 1+abs(w/f)
        else:
            return 1-abs(w/f)