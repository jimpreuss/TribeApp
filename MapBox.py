from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Data import *
from colors import Colors as C
from PyQt5.QtCore import *
from T import T, clear_item

class MapBox(QGroupBox):

    def __init__(self, node: MapNode, p_box = None):
        super(MapBox, self).__init__()
        self.node = node
        self.p_box = p_box

        self.main_layout = QVBoxLayout()
        self.label = QLabel(self.node.text)
        self.sub_layout = QGridLayout()
        self.sub_boxes = []
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.sub_layout)

        self.spawn_sub_boxes()

    def spawn_sub_boxes(self):
        x = self.width()
        y = self.height()

        children: list = sorted(self.node.children, key= lambda x: x._id)
        size = [n.size for n in children]
        s = sum(size)
        perc = [i/s for i in size]
        pix_size = [self.width()*i for i in perc]

        span = 0

        for i, node in enumerate(children):
            new_map_box = MapBox(node=node, p_box=self)
            self.sub_boxes.append(new_map_box)
            self.sub_layout.addWidget(a0=new_map_box, row=0, column=span, rowSpan=1, columnSpan=node.size)
            span += node.size

    def resizeEvent(self, a0: QResizeEvent) -> None:
        clear_item(self.sub_layout)
        super(MapBox, self).resizeEvent()
        self.spawn_sub_boxes()

    def 
