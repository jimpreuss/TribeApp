from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Data import *
from colors import Colors as C
from PyQt5.QtCore import *
from T import T


class TextBox(QTextEdit):

    def __init__(self, node: Node, width: int, selected_boxes: list, window: QMainWindow):
        self.node = node
        super().__init__(node.text)
        self.window = window
        self.setStyleSheet(C.normal_text_edit_style)
        self.selected_boxes = selected_boxes
        self.width = width
        self.setFixedWidth(width)
        self.setFixedHeight(self.calculate_height())
        self.setReadOnly(True)
        self.textChanged.connect(self.textChangedEvent)
        self.is_selected = False
        self.is_edited = False
        self.edited_style = C.edited_text_edit_style
        self.normal_style = C.normal_text_edit_style
        self.selected_style = C.selected_text_edit_style
        self.last_selected_style = C.last_selected_text_edit_style
        self.setFontPointSize(width/13)

    def renew_text(self):
        self.setText(self.node.text)
        self.setFixedHeight(self.calculate_height())

    def calculate_height(self):
        return self.fontMetrics().boundingRect(0, 0, self.width, 10000, 0x1000,
                                               self.toPlainText()).height()*1.1 + self.fontMetrics().height()*1.3

    def deselected(self):
        # Let self know its deselected
        self.is_selected = False
        # Reverse StyleSheet to normal
        self.setStyleSheet(self.normal_style)
        # Undo Selection of Text inside of edit field
        curser = self.textCursor()
        curser.clearSelection()
        self.setTextCursor(curser)
        self.renew_text()


    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        if not self.is_edited:
            modifier = QApplication.keyboardModifiers()
            if not(modifier == Qt.ShiftModifier):
                for box in self.selected_boxes:
                    box.deselected()
                self.selected_boxes.clear()
            self.selected_boxes.append(self)
            self.is_selected = True
            for box in self.selected_boxes:
                box.setStyleSheet(box.selected_style)
            if self.is_edited:
                self.setStyleSheet(self.edited_style)
            else:
                self.setStyleSheet(self.last_selected_style)
            self.renew_connect_nodes()

    def renew_connect_nodes(self):
        self.window.renew_connected_nodes(self)


    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)
        self.setReadOnly(False)
        self.is_edited = True
        self.setStyleSheet(self.edited_style)
        self.setFixedHeight(self.height()+40)

    def focusOutEvent(self, e: QFocusEvent) -> None:
        super().focusOutEvent(e)
        self.setStyleSheet(self.normal_style)
        if self.is_selected:
            self.setStyleSheet(self.selected_style)
        self.setReadOnly(True)
        self.is_edited = False

    def textChangedEvent(self):
        self.node.text = self.toPlainText()
        self.setFixedHeight(self.fontMetrics().boundingRect(0, 0, self.width, 2000, 0x1000, self.toPlainText()).height() + 32)


class MapNodeTextBox(TextBox):

    def __init__(self, node: MapNode, width: int, selected_boxes: list, window: QMainWindow, kind: int = T.undefined):
        super().__init__(node, width, selected_boxes, window=window)
        if isinstance(self.node, MapNode):
            self.set_type(self.node.kind)

    def set_type(self, kind: int):
        self.node.kind = kind

        if kind is T.undefined:
            self.edited_style = C.edited_text_edit_style
            self.normal_style = C.normal_text_edit_style
            self.selected_style = C.selected_text_edit_style
            self.last_selected_style = C.last_selected_text_edit_style
        elif kind is T.wish:
            self.edited_style = C.wish_edited_text_edit_style
            self.normal_style = C.wish_normal_text_edit_style
            self.selected_style = C.wish_selected_text_edit_style
            self.last_selected_style = C.last_wish_selected_text_edit_style
        elif kind is T.solution:
            self.edited_style = C.solution_edited_text_edit_style
            self.normal_style = C.solution_normal_text_edit_style
            self.selected_style = C.solution_selected_text_edit_style
            self.last_selected_style = C.last_solution_selected_text_edit_style
        elif kind is T.negativ:
            self.edited_style = C.negativ_edited_text_edit_style
            self.normal_style = C.negativ_normal_text_edit_style
            self.selected_style = C.negativ_selected_text_edit_style
            self.last_selected_style = C.last_negativ_selected_text_edit_style
        elif kind is T.observation:
            self.edited_style = C.observation_edited_text_edit_style
            self.normal_style = C.observation_normal_text_edit_style
            self.selected_style = C.observation_selected_text_edit_style
            self.last_selected_style = C.last_observation_selected_text_edit_style

        if self.is_selected:
            self.setStyleSheet(self.selected_style)
            if self.is_edited:
                self.setStyleSheet(self.edited_style)
        else:
            self.setStyleSheet(self.normal_style)

    def delete(self):
        if isinstance(self.node, MapNode):
            self.node.delete()
        self.selected_boxes.remove(self)
        self.setParent(None)
        self.deleteLater()

class ConnectionBox(MapNodeTextBox):

    def __init__(self, node: MapNode, con_node: MapNode, width: int,
                 selected_boxes: list, window: QMainWindow, kind: int = T.undefined):
        super().__init__(node=node, width=width, selected_boxes=selected_boxes, kind=kind, window=window)
        self.con_node = con_node

    def delete(self):
        if isinstance(self.node, MapNode):
            self.node.disconnect(self.con_node)
            self.con_node.disconnect(self.node)

            print(f"con-node: {self.con_node} \n parents: {self.con_node.parents} children: {self.con_node.children}")
            print(f"node: {self.node} \n parents: {self.node.parents} children: {self.node.children}")

        self.selected_boxes.remove(self)
        self.setParent(None)
        self.deleteLater()

    def renew_connect_nodes(self):
        pass