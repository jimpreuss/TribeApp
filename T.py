from PyQt5.QtGui import QColor
from colors import Colors as c


class T:
    # Other Node Types
    doc = 0
    page = 1
    source = 2
    map_node = 20
    # MapNode Types
    undefined = 3
    wish = 4
    observation = 5
    types = list(range(undefined, observation + 1))

    # Connection
    connection = 9

    # Relationship Types
    child = 10
    parent = 11
    equal = 12
    opposed = 13

    # Map values
    offset = 2
    standard_height = 10

    dictionary: {str: int} = {"Undefined Node": undefined, "Wish": wish, "Observation": observation,
                              "Child": child, "Parent": parent, "Equal": equal, "Opposed": opposed, "Source": source,
                              "Doc": doc, "Page": page}

    label = "Label"
    kind = "Type"
    description = "Description"
    start = "From"
    end = "To"

    page_number = "  p."
    document = "Document"
    source_node = "Source Node"
    original_text = "Original Text:\n"

    def mirror_relationship(self, kind: int) -> int:
        if kind is T.child:
            return T.parent
        elif kind is T.parent:
            return T.child
        elif kind is T.equal:
            return T.equal
        elif kind is T.opposed:
            return T.opposed

    def get_color(kind: int) -> QColor.rgb:
        if kind == T.wish:
            return QColor(c.pink3)
        elif kind == T.undefined:
            return QColor(c.green3)
        elif kind == T.observation:
            return QColor(c.yellow3)
        # elif kind == T.negativ:
        #     return QColor(c.red3)
        # elif kind == T.solution:
        #     return QColor(c.blue3)
        elif kind == T.source:
            return QColor(c.white2)
        else:
            return QColor(c.grey)


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