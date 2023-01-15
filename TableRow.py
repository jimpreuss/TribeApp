from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from TextBoxes import *
from Map import *


class TableRow(QGroupBox):

    def __init__(self, map: Map, source: SourceNode, width: int, selected_fields: [TextBox], window: QMainWindow):
        super().__init__()
        self.window = window
        self.map = map
        self.source_node: SourceNode = source
        self.selected_fields = selected_fields
        # Width Dimensions
        self.number_width = int(width/15)
        self.space = int(width/60)
        self.text_width = int((width- self.number_width*2 - self.space*5)/2)
        # Layouts
        self.main_layout =  QHBoxLayout()
        self.v_numbers_layout = QVBoxLayout()
        self.h_numbers_layout = QHBoxLayout()
        self.source_layout = QVBoxLayout()
        self.map_node_layout = QVBoxLayout()


        # Page and Sentence Number Fields
        self.page_number_field = QLabel(str(self.source_node.page.get_page_number()))
        self.sentence_number_field = QLabel(str(self.source_node.get_number_on_page()))
        # Source Text
        self.source_field = TextBox(self.source_node, self.text_width, self.selected_fields, window=self.window)
        # Add Button
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.new_map_node)

        self.set_graphic_settings()
        self.combine_layouts()
        self.renew()

    def renew(self):
        self.source_field.renew_text()
        for i in reversed(range(self.map_node_layout.count()-1)):
            self.map_node_layout.itemAt(i).widget().setParent(None)

        for map_node in self.source_node.map_nodes:
                self.create_map_node_field(map_node)

    def create_map_node_field(self, node: MapNode):
        self.map_node_layout.insertWidget(self.map_node_layout.count() - 1, MapNodeTextBox(node, self.text_width,
                                                                                           self.selected_fields,
                                                                                           window= self.window))

    def combine_layouts(self):
        self.setFixedWidth(self.text_width*2 + self.text_width*2 + 100)
        self.setLayout(self.main_layout)
        # Add Number Fields
        self.h_numbers_layout.addWidget(self.page_number_field)
        self.h_numbers_layout.addWidget(self.sentence_number_field)
        self.v_numbers_layout.addLayout(self.h_numbers_layout)
        self.v_numbers_layout.addStretch()
        self.main_layout.addLayout(self.v_numbers_layout)
        # Add Source Field
        self.main_layout.addSpacing(self.space)
        self.source_layout.addWidget(self.source_field)
        self.source_layout.addStretch()
        self.main_layout.addLayout(self.source_layout)
        # Ad MapNode Field
        self.main_layout.addSpacing(self.space)
        self. map_node_layout.addWidget(self.add_button)
        self.main_layout.addLayout(self.map_node_layout)
        self.main_layout.addSpacing(self.space*2)

    def set_graphic_settings(self):
        self.main_layout.setContentsMargins(0, 0, 0, self.space)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.map_node_layout.setAlignment(Qt.AlignTop)
        self.map_node_layout.setSpacing(self.space*2)

        self.add_button.setFixedSize(self.number_width*2, self.number_width)
        self.page_number_field.setFixedSize(self.number_width, self.number_width)
        self.sentence_number_field.setFixedSize(self.number_width, self.number_width)
        font = QFont()
        style_sheet =   f"color: {C.black2};" \
                        f"background-color: {C.white3};" \
                        f"border: 0px solid {C.white3};" \
                        f"padding: 0px;" \
                        f"font-family: {C.schriftart};"
        font.setPointSize(self.source_field.fontPointSize())
        print(f" font pixel size numberfield: {font.pixelSize()}")
        print(f" font point size numberfield: {font.pointSize()}")

        self.page_number_field.setFont(font)
        self.sentence_number_field.setFont(font)
        self.page_number_field.setStyleSheet(style_sheet)
        self.sentence_number_field.setStyleSheet(style_sheet)
        print(f"size numberfield: {self.page_number_field.size()}")
        self.page_number_field.setAlignment(Qt.AlignCenter)
        self.sentence_number_field.setAlignment(Qt.AlignCenter)


    def new_map_node(self, kind = T.undefined):
        # Check if Text in SourceNode is Selected
        if self.source_field.createMimeDataFromSelection().text().strip():
            text = self.source_field.createMimeDataFromSelection().text()
            self.map_node_layout.count()
            self.create_map_node_field(self.map.add_map_node(source=self.source_node,text=text, kind=kind))
        else:
            self.create_map_node_field(self.map.add_map_node(source=self.source_node,
                                                             text=self.source_node.text, kind=kind))
