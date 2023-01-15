from TableRow import *
from Map import Map
import os
from PyQt5.QtCore import Qt
import threading
from Canvas import Canvas
# from Worker import WorkerThread

# noinspection PyArgumentList,PyTypeChecker
class Window(QMainWindow):

    def __init__(self):
        # Konstruktor von QWidget
        super().__init__(parent=None)

        self.settings = QSettings('tribe company', 'tribeApp')
        self.widget = QWidget(parent=self)
        self.setStyleSheet(C.standard_style)

        rect = self.screen().availableGeometry()
        print('Available: %d x %d' % (rect.width(), rect.height()))
        self.min_width = 1280
        self.min_height = 720
        self.space = int(rect.width()/160)
        self.left_side_width = int(rect.width()/9*2)
        self.middle_side_width = int(rect.width()/9)
        self.label_height = int(rect.width()/80)

        # Toolbar
        self.toolbar = QToolBar("Hello Toolbar!")
        self.addToolBar(self.toolbar)

        # Layouts
        self.upper_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.main_layout = QHBoxLayout()
        # SourceNodes and MapNodes
        self.left_layout = QVBoxLayout()
        self.le_scroll = QScrollArea()
        self.le_group_box = QGroupBox()
        self.table_rows: [TableRow] = []
        # Connections of currently selected Box
        self.mid_scroll = QScrollArea()
        self.mid_group_box = QGroupBox()
        self.middle_layout = QVBoxLayout()
        # Graphic Map
        self.right_layout = QVBoxLayout()
        self.pixmap = QPixmap(4000, 2000)
        self.canvas = Canvas(space=self.space, pixmap=self.pixmap)
        self.current_pixmap = QPixmap(200, 200)

        # Actions: Save, Load, Import
        self.load_action = QAction("Load")
        self.import_action = QAction("Import")
        self.save_action = QAction("Save")
        # MapNode create and change_kind Actions
        self.undefined_action = QAction("Undefined")
        self.wish_action = QAction("Wish")
        self.observation_action = QAction("Observation")
        self.observation_negativ_action = QAction("Negativ")
        self.solution_action = QAction("Solution")
        self.combine_action = QAction("Combine")
        # Other Actions
        self.delete_action = QAction("Delete")
        self.finished_action = QAction("Finished")
        self.paint_action = QAction("Paint")
        # Connect Actions
        self.add_parent_action = QAction("Add Reason")
        self.add_child_action = QAction("Add Means")
        self.equal_action = QAction("Add Equal")
        self.opposed_action = QAction("Add Opposite")
        self.export_img_action = QAction("Export Image")

        # Data
        self.map: Map = None
        self.fontsize = 400
        self.threads: [threading.Thread] = []
        # Autosave
        # self.timer = QBasicTimer()
        # self.timer.start(60000*5, self)

        # Selection
        self.selected_boxes: [TextBox] = []
        self.last_selected_box: TextBox = None

        # Functions
        self.init_pixmap()
        self.init_main_window()
        self.init_actions_and_shortcuts()
        self.customise_style()

        self.show()

    # def timerEvent(self, e: 'QTimerEvent') -> None:
    #    if e.timerId() == self.timer.timerId():
    #        if self.map is not None:
    #            n = self.settings.value(self.settings.value("last_save", ""), 1)
    #            self.map.export_csv(self.settings.value("last_save", "")[:-4]+str(n)+".csv")
    #            print(f"Autosave done{n}")
    #            self.settings.setValue(self.settings.value("last_save", ""), n+1)

    def paint(self):
        for t in self.threads:
            t.join()
            self.threads = []
        p1 = threading.Thread(target=self.painting)
        self.threads.append(p1)
        p1.start()

        # worker = WorkerThread(self.pixmap,self.map, self.canvas, self.font, self.space)
        # worker.start()

    def painting(self):
        size_factor = 100
        # get Data From Map
        width_height_locations = self.map.get_grafik_map()
        width = width_height_locations[0]*size_factor + T.offset*size_factor
        height = width_height_locations[1]*size_factor + T.offset*size_factor
        locations = width_height_locations[2]

        # set width at height to minimum available pixel
        width = max(width, self.canvas.width())
        height = max(height, self.canvas.height())

        # Create new Pixmap and Painter
        self.pixmap = QPixmap(width, height)
        self.pixmap.fill(QColor(C.white1))
        painter = QPainter(self.pixmap)

        # locations are stored as [[height, [x_cord, y_cord, MapNode]], [height, [x_cord, y_cord, MapNode]], ...]
        for loc in locations:
            font = QFont()
            font.setPixelSize(self.fontsize)
            font.setBold(True)
            x = loc[1][0]*size_factor
            y = loc[1][1]*size_factor
            node = loc[1][2]
            width = node.size * size_factor
            height = int(size_factor * T.standard_height*max(1, math.sqrt(len(node.children))))
            # color = QColor(T.get_color(kind=node.kind))
            color = QColor("#502379")
            if node.size == T.standard_height:
                color = QColor('#82D0F4')
            # gradient = QRadialGradient(QPoint(x+width/2,y+size_factor/2), width/2)
            # gradient.setColorAt(0, color)
            # gradient.setColorAt(0.5, QColor(C.pink3))
            # gradient.setColorAt(1, T.get_color(T.source))
            pen = QPen(QColor(QColor(C.white2)), 0)
            brush = QBrush(color)
            painter.setPen(pen)
            painter.setBrush(brush)

            # Draw Ellipse
            painter.drawEllipse(x, y, width, height)
            # calculate Rectangle inside Ellipse
            rot = -49.5
            e_x = abs(math.cos(rot) * (width/2))
            e_y = abs((height/2)*math.sin(rot))
            x_offset = int(abs(width/2 - e_x))
            y_offset = int(abs(height/2 - e_y))
            rect = QRect(x + x_offset, y + y_offset, width - 2*x_offset, height - 2*y_offset)
            # Calculate font height
            max_height_rec = QRect(x + x_offset, y + y_offset, width - 2*x_offset, size_factor*100)
            fm = QFontMetrics(font)
            font_rect = fm.boundingRect(rect, Qt.TextWordWrap | Qt.AlignCenter, node.text)
            while rect.height() < font_rect.height() or rect.width() < font_rect.width():
                font.setPixelSize(font.pixelSize()-1)
                fm = QFontMetrics(font)
                font_rect = fm.boundingRect(rect, Qt.TextWordWrap | Qt.AlignCenter, node.text)
            # Draw Text
            painter.setPen(QPen(QColor(C.white1), 15, Qt.SolidLine))
            painter.setFont(font)
            painter.drawText(rect, Qt.TextWordWrap | Qt.AlignCenter, node.text)
            # Draw Page Number
            id_font = QFont()
            id_font.setPixelSize(int(self.fontsize*0.2))
            rect = QRect(x+x_offset, y+y_offset + (height - 2*y_offset)+size_factor/5, width - 2*x_offset, int(size_factor/1.5))
            painter.setPen(QPen(QColor(C.white1), 1, Qt.SolidLine))
            painter.setFont(id_font)
            painter.drawText(rect, Qt.AlignCenter, node._id)
            painter.setBrush(QBrush(Qt.transparent))
            # painter.drawRect(rect)
        painter.end()
        self.canvas.setPixmap(self.pixmap)
        print(self.pixmap.size())
        # self.current_pixmap = self.pixmap.scaled(self.canvas.width(), self.canvas.height())
        # self.canvas.setPixmap(self.current_pixmap)

    def export_svg(self):
        size_factor = 100
        # get Data From Map
        width_height_locations = self.map.get_grafik_map()
        width = width_height_locations[0] * size_factor + T.offset * size_factor
        height = width_height_locations[1] * size_factor + T.offset * size_factor
        locations = width_height_locations[2]

        # set width at height to minimum available pixel
        width = max(width, self.canvas.width())
        height = max(height, self.canvas.height())

        # Create new Pixmap and Painter
        self.pixmap = QPixmap(width, height)
        self.pixmap.fill(QColor(C.white1))
        painter = QPainter(self.pixmap)

        # locations are stored as [[height, [x_cord, y_cord, MapNode]], [height, [x_cord, y_cord, MapNode]], ...]
        for loc in locations:
            font = QFont()
            font.setPixelSize(self.fontsize)
            font.setBold(True)
            x = loc[1][0] * size_factor
            y = loc[1][1] * size_factor
            node = loc[1][2]
            width = node.size * size_factor
            height = int(size_factor * T.standard_height * max(1, math.sqrt(len(node.children))))
            # color = QColor(T.get_color(kind=node.kind))
            color = QColor("#502379")
            if node.size == T.standard_height:
                color = QColor('#82D0F4')
            # gradient = QRadialGradient(QPoint(x+width/2,y+size_factor/2), width/2)
            # gradient.setColorAt(0, color)
            # gradient.setColorAt(0.5, QColor(C.pink3))
            # gradient.setColorAt(1, T.get_color(T.source))
            pen = QPen(QColor(QColor(C.white2)), 0)
            brush = QBrush(color)
            painter.setPen(pen)
            painter.setBrush(brush)

            # Draw Ellipse
            painter.drawEllipse(x, y, width, height)
            # calculate Rectangle inside Ellipse
            rot = -49.5
            e_x = abs(math.cos(rot) * (width / 2))
            e_y = abs((height / 2) * math.sin(rot))
            x_offset = int(abs(width / 2 - e_x))
            y_offset = int(abs(height / 2 - e_y))
            rect = QRect(x + x_offset, y + y_offset, width - 2 * x_offset, height - 2 * y_offset)
            # Calculate font height
            max_height_rec = QRect(x + x_offset, y + y_offset, width - 2 * x_offset, size_factor * 100)
            fm = QFontMetrics(font)
            font_rect = fm.boundingRect(rect, Qt.TextWordWrap | Qt.AlignCenter, node.text)
            while rect.height() < font_rect.height() or rect.width() < font_rect.width():
                font.setPixelSize(font.pixelSize() - 1)
                fm = QFontMetrics(font)
                font_rect = fm.boundingRect(rect, Qt.TextWordWrap | Qt.AlignCenter, node.text)
            # Draw Text
            painter.setPen(QPen(QColor(C.white1), 15, Qt.SolidLine))
            painter.setFont(font)
            painter.drawText(rect, Qt.TextWordWrap | Qt.AlignCenter, node.text)
            # Draw Page Number
            id_font = QFont()
            id_font.setPixelSize(int(self.fontsize * 0.2))
            rect = QRect(x + x_offset, y + y_offset + (height - 2 * y_offset) + size_factor / 5, width - 2 * x_offset,
                         int(size_factor / 1.5))
            painter.setPen(QPen(QColor(C.white1), 1, Qt.SolidLine))
            painter.setFont(id_font)
            painter.drawText(rect, Qt.AlignCenter, node._id)
            painter.setBrush(QBrush(Qt.transparent))
            # painter.drawRect(rect)
        painter.end()
        self.canvas.setPixmap(self.pixmap)
        print(self.pixmap.size())
        # self.current_pixmap = self.pixmap.scaled(self.canvas.width(), self.canvas.height())
        # self.canvas.setPixmap(self.current_pixmap)

    def customise_style(self):
            self.toolbar.setMovable(False)
            self.toolbar.setFixedHeight(35)
            self.left_layout.setContentsMargins(0, 0, 0, 0)
            self.setContentsMargins(0, 0, 0, 0)
            self.le_scroll.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setContentsMargins(5, 0, 5, 0)

    def init_main_window(self):
        # Set Window Title
        self.setWindowTitle("tribe V0.1")
        # Set Window Size and Place to last Window Size and Place
        self.setMinimumSize(self.min_width, self.min_height)
        self.resize(self.settings.value("size", QSize(self.min_width, self.min_height)))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        # Set Size of Left Layout
        self.le_scroll.setWidgetResizable(True)
        self.le_scroll.setFixedWidth(self.left_side_width)
        # Set Size of Middle Layout
        self.mid_scroll.setWidgetResizable(True)
        self.mid_scroll.setFixedWidth(self.middle_side_width)
        self.middle_layout.setAlignment(Qt.AlignTop)
        self.mid_scroll.setAlignment(Qt.AlignTop)


        # Order Layouts
        self.upper_layout.addLayout(self.header_layout)
        self.upper_layout.addLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.upper_layout)
        self.le_group_box.setLayout(self.left_layout)
        self.le_scroll.setWidget(self.le_group_box)
        self.mid_group_box.setLayout(self.middle_layout)
        self.mid_scroll.setWidget(self.mid_group_box)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.le_scroll)
        self.main_layout.addWidget(self.mid_scroll)
        self.main_layout.addLayout(self.right_layout)
        self.right_layout.addWidget(self.canvas)
        self.canvas.setStyleSheet(f"background-color: {C.white2};")
        # Add Headers
        left_header = QLabel("Source and Map Nodes")
        middle_header = QLabel("Connections")
        right_header = QLabel("Map")
        left_header.setFixedWidth(self.left_side_width)
        middle_header.setFixedWidth(self.middle_side_width)
        self.header_layout.addWidget(left_header)
        self.header_layout.addWidget(middle_header)
        self.header_layout.addWidget(right_header)

    def renew_connected_nodes(self, box: TextBox):
        if box is not self.last_selected_box:
            for i in range(self.middle_layout.count()).__reversed__():
                clear_item(self.middle_layout.itemAt(i))
            if isinstance(box.node, MapNode):
                reason_label = QLabel("Reasons")
                reason_label.setFixedHeight(self.label_height)
                self.middle_layout.addWidget(reason_label)
                for node in box.node.parents:
                    self.middle_layout.addWidget(ConnectionBox(node, box.node, self.middle_side_width,
                                                               self.selected_boxes, window=self))
                means_label = QLabel("Means")
                means_label.setFixedHeight(self.label_height)
                self.middle_layout.addWidget(means_label)
                for node in box.node.children:
                    self.middle_layout.addWidget(ConnectionBox(node, box.node, self.middle_side_width,
                                                               self.selected_boxes, window=self))
                eq_label = QLabel("Equals")
                eq_label.setFixedHeight(self.label_height)
                self.middle_layout.addWidget(eq_label)
                for node in box.node.equals:
                    self.middle_layout.addWidget(ConnectionBox(node, box.node, self.middle_side_width,
                                                               self.selected_boxes, window=self))
                opo_label = QLabel("Opposites")
                opo_label.setFixedHeight(self.label_height)
                self.middle_layout.addWidget(opo_label)
                for node in box.node.opposites:
                    self.middle_layout.addWidget(ConnectionBox(node, box.node, self.middle_side_width,
                                                               self.selected_boxes, window=self))
        self.last_selected_box = box

    def closeEvent(self, e):
        # Write window size and position to config file
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.ask_for_save()
        e.accept()

    def resizeEvent(self, event):
        self.canvas.setFixedSize(self.width() - self.left_side_width - self.middle_side_width, self.height())
        self.canvas.setPixmap(self.pixmap)

    def init_actions_and_shortcuts(self):
        # Set Status Tipp
        self.load_action.setStatusTip("This is load_action")
        self.import_action.setStatusTip("This is import_action")
        self.save_action.setStatusTip("This is save_action")
        self.wish_action.setStatusTip("This is wish_action")
        self.observation_action.setStatusTip("This is observation_action")
        self.solution_action.setStatusTip("This is solution_action")
        self.undefined_action.setStatusTip("This is undefined action")
        self.delete_action.setStatusTip("This is delete action")
        self.finished_action.setStatusTip("This is finished action")
        self.combine_action.setStatusTip("This is Combine Action")
        self.paint_action.setStatusTip("This is Paint Action.")
        self.add_parent_action.setStatusTip("This is Parent Action.")
        self.add_child_action.setStatusTip("This is Child Action.")
        self.equal_action.setStatusTip("This is Equal Action.")
        self.opposed_action.setStatusTip("This is Opposed Action.")
        self.export_img_action.setStatusTip("This is Picture Export Action")

        # Connect actions to functions
        self.load_action.triggered.connect(self.load_new_file)
        self.import_action.triggered.connect(self.import_file)
        self.save_action.triggered.connect(self.save_file)
        self.wish_action.triggered.connect(lambda: self.change_map_node_type(T.wish))
        self.observation_action.triggered.connect(lambda: self.change_map_node_type(T.observation))
        self.solution_action.triggered.connect(lambda: self.change_map_node_type(T.solution))
        self.undefined_action.triggered.connect(lambda: self.change_map_node_type(T.undefined))
        self.observation_negativ_action.triggered.connect(lambda: self.change_map_node_type(T.negativ))
        self.finished_action.triggered.connect(self.finished)
        self.delete_action.triggered.connect(self.delete)
        self.combine_action.triggered.connect(self.combine)
        self.paint_action.triggered.connect(self.paint)
        self.add_parent_action.triggered.connect(lambda: self.connect_map_nodes(T.parent))
        self.add_child_action.triggered.connect(lambda: self.connect_map_nodes(T.child))
        self.equal_action.triggered.connect(lambda: self.connect_map_nodes(T.equal))
        self.opposed_action.triggered.connect(lambda: self.connect_map_nodes(T.opposed))
        self.export_img_action.triggered.connect(self.export_img)

        # Add actions to Toolbar
        self.toolbar.addActions([self.load_action, self.import_action, self.save_action, self.delete_action,
                                 self.combine_action, self.finished_action, self.wish_action, self.observation_action,
                                 self.observation_negativ_action, self.solution_action, self.undefined_action,
                                 self.paint_action, self.add_parent_action, self.add_child_action, self. equal_action,
                                 self.opposed_action, self.export_img_action])

        # Connect shortcuts to functions
        self.load_action.setShortcut(QKeySequence('Ctrl+L'))
        self.import_action.setShortcut(QKeySequence('Ctrl+I'))
        self.save_action.setShortcut(QKeySequence('Ctrl+Shift+S'))
        self.undefined_action.setShortcut(QKeySequence('Ctrl+U'))
        self.wish_action.setShortcut(QKeySequence('Ctrl+W'))
        self.observation_action.setShortcut(QKeySequence('Ctrl+O'))
        self.observation_negativ_action.setShortcut(QKeySequence('Ctrl+N'))
        self.solution_action.setShortcut(QKeySequence('Ctrl+S'))
        self.combine_action.setShortcut(QKeySequence('Ctrl+K'))
        self.delete_action.setShortcut(QKeySequence('Ctrl+D'))
        self.finished_action.setShortcut(QKeySequence('Ctrl+F'))
        self.paint_action.setShortcut(QKeySequence('Ctrl+P'))
        self.add_parent_action.setShortcut(QKeySequence('Ctrl+R'))
        self.add_child_action.setShortcut(QKeySequence('Ctrl+M'))
        self.equal_action.setShortcut(QKeySequence('Ctrl+E'))
        self.opposed_action.setShortcut(QKeySequence('Ctrl+G'))

    def init_pixmap(self):
        # Create Blank Canvas
        self.pixmap.fill(QColor(C.white1))
        self.canvas.setPixmap(self.pixmap)

    def ask_for_save(self):
        msg = QMessageBox()
        msg.setText("Do you want to save your Map?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)

        msg.buttonClicked.connect(self.ask_for_save_options)
        msg.exec_()

    def ask_for_save_options(self, button):
        if button.text() == "Cancel":
            pass
        if button.text() == "Save":
            self.export_csv()

    def load_file(self, file_path: str = None):
        if file_path is None:
            file_path = self.settings.value("last_save", "")
        path_list = os.path.split(file_path)
        self.map = Map(path_list[1][:-4])
        self.map.import_file(file_path=file_path, document_name=path_list[1])
        self.settings.setValue("last_directory", path_list[0])
        for i in range(self.left_layout.count()):
            clear_item(self.left_layout.itemAt(i))
        self.show_table()
        self.setWindowTitle(f"TribeApp:    {path_list[1]}")

    def load_new_file(self):
        if self.map is not None:
            self.ask_for_save()
        file_path = QFileDialog.getOpenFileName(parent=self, caption="Load File",
                                                directory=self.settings.value("last_save", ""),
                                                filter="All Files(*.pdf; *.csv);;PDF Files (*.pdf);; CSV Files (*.csv)")
        self.load_file(file_path=file_path[0])
        self.paint()

    def import_file(self):
        file_path = QFileDialog.getOpenFileName(parent=self, caption="Import File",
                                                directory=self.settings.value("last_directory", ""),
                                                filter="All Files(*.pdf; *.csv);;PDF Files (*.pdf);; CSV Files (*.csv)")
        path_list = os.path.split(file_path[0])
        if self.map is None:
            self.map = Map(path_list[1][:-4])
        self.map.import_file(file_path=file_path[0], document_name=path_list[1])
        self.settings.setValue("last_directory", path_list[0])
        self.show_table()
        self.paint()

    def show_table(self):
        for node in self.map.get_rows():
            row = TableRow(map=self.map, source=node, width=self.left_side_width,
                           selected_fields=self.selected_boxes, window=self)
            self.table_rows.append(row)
            self.left_layout.addWidget(row)

    def save_file(self):
        self.export_csv()

    def change_map_node_type(self, kind: str):
        if all(isinstance(i, MapNodeTextBox) for i in self.selected_boxes):
            for sel_field in self.selected_boxes:
                sel_field.set_type(kind)
        elif len(self.selected_boxes) == 1:
            self.selected_boxes[0].parent().new_map_node(kind=kind)
        self.paint()

    def connect_map_nodes(self, kind: str):
        if all(isinstance(box, MapNodeTextBox) for box in self.selected_boxes):
            add_from = self.selected_boxes[:-1]
            add_to = self.selected_boxes[-1]
            for box in add_from:
                box.node.add(add_to.node, kind=kind)
        self.paint()

    def delete(self):
        if all(isinstance(i, MapNodeTextBox) for i in self.selected_boxes):
            for i in range(len(self.selected_boxes)).__reversed__():
                self.selected_boxes[i].delete()
        self.paint()
    def combine(self):
        # Check if online TextFields of SourceNodes are selected
        if all(not(isinstance(i, MapNodeTextBox)) for i in self.selected_boxes) and len(self.selected_boxes) > 1:
            # Get List of GroupBoxes Containing the TextFields
            group_list = [sel_field.parent() for sel_field in self.selected_boxes]
            # Check if GroupBoxes are right next to each other
            location_list: [int] = [self.table_rows.index(group) for group in group_list]
            ordered_list = sorted(location_list)

            if all((ordered_list[i] == ordered_list[i+1]-1) for i in range(len(ordered_list)-1)):
                group_list = [x for _, x in sorted(zip(location_list, group_list))]
                first_group_at = min(location_list)
                first_group = group_list[0]
                group_list.remove(first_group)

                for group in group_list:
                    first_group.source_node.combine(group.source_node)
                    self.table_rows.remove(group)
                    clear_item(group)

                self.selected_boxes.clear()
                self.selected_boxes.append(first_group.source_field)
                first_group.renew()

                for i in range(first_group_at, len(self.table_rows)):
                    self.table_rows[i].sentence_number_field.setText(str(i))

    def finished(self):
        pass

    def export_csv(self):
        file_path = QFileDialog.getSaveFileName(self, "Save File", self.settings.value("last_save", ""),
                                                "CSV Files (*.csv)")
        if os.path.exists(os.path.split(file_path[0])[0]):
            print("saving")
            self.map.export_csv(file_path[0])
        self.settings.setValue("last_save", file_path[0])

    def export_img(self):
        file_path = QFileDialog.getSaveFileName(self, "Save File", self.settings.value("last_save", ""),
                                                "JPG File (*.jpg)")
        img = self.pixmap.toImage()
        img.save(file_path[0])
        self.settings.setValue("last_save", file_path[0])


def clear_item(item):
    layout = None
    if hasattr(item, "layout"):
        if callable(item.layout):
            layout = item.layout()
    widget = None

    if hasattr(item, "widget"):
        if callable(item.widget):
            widget = item.widget()

    if widget:
        widget.setParent(None)
    elif layout:
        for i in reversed(range(layout.count())):
            clear_item(layout.itemAt(i))
