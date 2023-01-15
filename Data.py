from dataclasses import dataclass, field
from T import T
import datetime
import math

offset = 2


@dataclass
class Node:
    text: str
    _id : str
    created = f"{datetime.date} {datetime.time}"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{type(self)}: {self._id}"

future: Node
past: Node
now: Node

@dataclass
class DocNode(Node):
    title: str
    pages: list = field(init= False, default_factory=list)

    def add_page(self, page):
        if isinstance(page, PageNode):
            self.pages.append(page)
            return page

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{type(self)}: {self._id}"

@dataclass
class PageNode(Node):
    doc: DocNode
    source_parts: list = field(init= False, default_factory=list)

    def add_source_node(self, node):
        if isinstance(node, SourceNode):
            self.source_parts.append(node)
            return node

    def remove_source_node(self, node):
        self.source_parts.remove(node)

    def index(self):
        return self.doc.pages.index(self)

    def get_page_number(self):
        return self.index()+1


@dataclass
class SourceNode(Node):
    page: PageNode
    original_text: str = field(default=None)
    map_nodes: list = field(init= False, default_factory=list)

    def __post_init__(self):
        if self.original_text is None:
            self.original_text = self.text

    def restore_original(self):
        self.text = self.original_text

    def add_map_node(self, node):
        if isinstance(node, MapNode):
            self.map_nodes.append(node)
            return node

    def remove_map_node(self, node):
        self.map_nodes.remove(node)

    def index(self):
        return self.page.source_parts.index(self)

    def get_number_on_page(self):
        return self.index()+1

    def comes_before(self, node) -> True:
        if isinstance(node, SourceNode):
            if self.page == node.page and node.index() - self.index() == 1:
                return True
            elif self.page.doc == node.page.doc and node.index() == 0 and self.page.source_parts[-1] == self:
                    return True
        return False

    def combine(self, node):
        if isinstance(node, SourceNode):
            if self.comes_before(node):
                self.text += "\n" + node.text
                self.original_text += "\n" + node.original_text
                self.map_nodes += node.map_nodes
                for mapNode in node.map_nodes:
                    mapNode.source = self
                node.page.source_parts.remove(node)
            elif node.comes_before(self):
                node.combine(self)
            else:
                raise AssertionError("Nodes are not next next to each other.")
        else:
            raise TypeError("Cannot Combine SourceNode with another type of node.")


@dataclass
class MapNode(Node):
    source: SourceNode
    kind: int = field(default=T.undefined)
    size: int = field(init=False, default= T.standard_height)

    def __post_init__(self):
        if self.kind not in T.types:
            self.kind = T.undefined
        self.parents: set[Node] =set()
        self.children: set[Node] =set()
        self.equals: set[Node] =set()
        self.opposites: set[Node] =set()

    def index(self):
        self.source.map_nodes.index(self)

    def is_offspring_of(self, node):
        if isinstance(node, MapNode):
            if node in self.parents:
                return True
            return any([p.is_offspring_of(node) for p in self.parents])

    def is_ancestor_of(self, node):
        if isinstance(node, MapNode):
            if node in self.children:
                return True
            return any([c.is_ancestor_of(node) for c in self.children])

    def get_tree_loc_and_size(self,x: int, y: int) -> [[int, [int, int, Node]]]:
        floating_x = x
        result =[]
        for node in self.children:
            result.extend(node.get_tree_loc_and_size(floating_x+T.offset, int(y + T.standard_height*max(1, math.sqrt(len(self.children))) + T.offset)))
            floating_x += node.size+T.offset
        max_h = 0
        for i in result:
            max_h = max(max_h, i[0])
        result.extend([[int(max_h+T.offset+T.standard_height*max(1, math.sqrt(len(self.children)))), [x + T.offset, y + T.offset, self]]])
        return result

    def set_size_up_tree(self):
        self.size  = max(T.standard_height,sum([n.size for n in self.children])+ T.offset * (len(self.children)+1))
        for parent in self.parents:
            parent.set_size_up_tree()

    def set_size_down_tree(self):
        for child in self.children:
            child.set_size_down_tree()
        self.size  = max(T.standard_height,sum([n.size for n in self.children]) + T.offset * (len(self.children)+1))


    def add(self, node, kind: int):
        if isinstance(node, MapNode):
            # add Parent
            self.disconnect(node)
            if kind is T.parent:
                if self.is_ancestor_of(node):
                    print("Cannot add parent since parent is already offspring of node.")
                else:
                    self.parents.add(node)
                    node.children.add(self)
                    node.set_size_up_tree()

                    if future in self.parents:
                        self.disconnect(future)
                    if future in self.parents:
                        self.disconnect(now)
            # add Child
            if kind is T.child:
                if self.is_offspring_of(node):
                    print("Cannot add child since child is already ancestor of node.")
                else:
                    self.children.add(node)
                    node.parents.add(self)
                    self.set_size_up_tree()

                    if now in self.children:
                        self.disconnect(now)
                    if past in self.children:
                        self.disconnect(past)
            # add Equal
            if kind is T.equal:
                self.equals.add(node)
                node.equals.add(self)
            # add Parent
            if kind is T.opposed:
                self.opposites.add(node)
                node.opposites.add(self)

    def disconnect(self, node):
        if isinstance(node, MapNode):
            if node in self.parents:
                self.parents.remove(node)
                node.children.remove(self)
                node.set_size_up_tree()
                if not bool(self.parents):
                    if self.kind == T.wish:
                        self.parents.add(future)
                    elif self.kind == T.observation:
                        self.parents.add(now)
            elif node in self.children:
                self.children.remove(node)
                node.parents.remove(self)
                self.set_size_up_tree()
                if not bool(self.children):
                    if self.kind == T.wish:
                        self.children.add(now)
                    elif self.kind == T.observation:
                        self.children.add(past)
            elif node in self.equals:
                self.equals.remove(node)
                node.equals.remove(self)
            elif node in self.opposites:
                self.opposites.remove(node)
                node.opposites.remove(self)

    def disconnect_all(self):
        for node in self.parents.copy() and self.children.copy() and self.equals.copy() and self.opposites.copy():
            if isinstance(node, MapNode):
                node.disconnect(self)
                self.disconnect(node)

    def delete(self):
        self.disconnect_all()
        if future in self.parents:
            self.parents.remove(future)
        if now in self.parents:
            self.parents.remove(now)
        if past in self.children:
            self.children.remove(past)
        if now in self.children:
            self.disconnect(now)
        self.source.map_nodes.remove(self)
        del self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{type(self)}: {self._id}"

    def __hash__(self):
        return self._id.__hash__()


@dataclass()
class GodNode(MapNode):
    text: str = ""
    _id: str = None
    source: SourceNode = None
    kind: int = field(default=T.undefined)
    size: int = field(init=False, default=T.standard_height)

    def __post_init__(self):
        self._id = str(self.kind)
        self.parents: set[Node] = set()
        self.children: set[Node] = set()
        self.equals: set[Node] = set()
        self.opposites: set[Node] = set()


def connect(start: MapNode, end: MapNode, kind: int):
    start.add(end, kind)


future: GodNode = GodNode(_id=T.wish, kind=T.wish)
now: GodNode = GodNode(_id=T.undefined, kind=T.undefined)
past: GodNode = GodNode(_id=T.observation, kind=T.observation)
future.add(now, T.child)
now.add(past, T.child)
