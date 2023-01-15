
node_types = ["undefined", "wish", "solution", "observation negativ", "observation"]

class Node:
    def __init__(self, text: str):
        self.text = text

class SourceNode(Node):
    def __init__(self, text: str, page_number: int, previous_node: Node, parent):
        super().__init__(text)
        self.previous_node = previous_node
        self.page_number: int = page_number
        self.original_text = text
        self.text_field = None
        self.parent = parent
        self.map_nodes : [MapNode] = []

    def get_number(self) -> int:
        return self.parent.get_node_position(self)

class SourceText:

    def __init__(self, title: str = "new SourceText"):
        self.title = title
        self.pages: [str] = []
        self.nodes_by_page: {int: [SourceNode]} = {}
        self.source_nodes: {str: SourceNode} = {}
        self.last_node_added: SourceNode = None
        self.map_nodes: {str: MapNode} = {}

    def get_node_position(self, node: SourceNode):
        return self.source_nodes.index(node)

    def num_nodes(self):
        return len(self.source_nodes)

    def import_page(self, page: str):
        self.pages.append(page)
        self.nodes_by_page[len(self.pages)-1] = []
        for part in page.split(". "):
            if part.strip():
                new_node = SourceNode(part + ".", len(self.pages)-1, self.last_node_added, self)
                self.source_nodes.append(new_node)
                self.nodes_by_page[len(self.pages)-1].append(new_node)
                self.last_node_added = new_node

    def get_page(self, page: int):
        return self.pages[page]

class MapNode(Node):

    def __init__(self, text: str, source_node: SourceNode = None, type: str = node_types[0]):
        super().__init__(text)
        self.type = type
        self.source_node: SourceNode = source_node
        self.parent_nodes: {MapNode} = {}
        self.child_nodes: {MapNode} = {}
        self.equal_nodes: {MapNode} = {}
        self.contradicting_nodes: {MapNode} = {}

    def add_parent(self, parents):
        self.parent_nodes.update(parents)
        for parent in parents:
            parent.child_nodes.add(self)

    def delete_parent(self, parents):
        for parent in parents:
            if parent in self.parent_nodes:
                self.parent_nodes.pop(parent)
                parent.child_nodes.pop(self)

    def add_child(self, children):
        for child in children:
            child.parent_nodes.update(self)
        self.child_nodes.update(children)

    def delete_child(self, children):
        if child in self.child_nodes:
            self.child_nodes.pop(child)
            child.parent_nodes.remove(self)

    def add_equal(self, equal):
        self.equal_nodes.append(equal)
        equal.equal_nodes.append(self)

    def delete_equal(self, equal):
        if equal in self.equal_nodes:
            self.equal_nodes.remove(equal)
            equal.equal_nodes.remove(self)

    def add_contra(self, contra):
        self.contradicting_nodes.append(contra)
        contra.contradicting_nodes.append(self)

    def delete_contra(self, contra):
        if contra in self.contradicting_nodes:
            self.contradicting_nodes.remove(contra)
            contra.contradicting_nodes.remove(self)

