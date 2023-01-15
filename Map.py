import datetime

import numpy as np
from PyPDF2 import PdfFileReader
import csv
from Data import Node, SourceNode, PageNode, MapNode, connect, DocNode, GodNode, future, past, now
from T import T
from dataclasses import dataclass, field
import re

@dataclass
class Map:
    title: str = field(default="NewMap")
    doc_nodes: [DocNode] = field(default_factory=list)
    nodes: dict[{str: Node}] = field(default_factory=dict)

    def __init__(self):
        super().__init__()
        self.future = GodNode(_id=T.wish, kind=T.wish)
        self.nodes[T.wish] = self.future
        self.now = GodNode(_id=T.undefined, kind=T.undefined)
        self.nodes[T.undefined] = self.now
        self.past = GodNode(_id=T.observation, kind=T.observation)
        self.nodes[T.observation] = self.past
        self.future.add(self.now, T.child)
        self.now.add(self.past, T.child)

    def __repr__(self):
        return f"{self.title}  docs: {self.doc_nodes}, number of nodes: {len(self.nodes)}"

    def add_doc(self, title: str = None, text: str = "Document Description", _id: str = None):
        _id = self.generate_id(_id=_id, p_node=title)
        if title is None:
            title = "New Document" + str(len(self.doc_nodes))
        new_node = DocNode(title=title, text=text, _id=_id)
        self.doc_nodes.append(new_node)
        self.nodes[_id] = new_node
        return new_node

    def add_page(self, text: str, doc: DocNode, _id: str = None):
        _id = self.generate_id(_id=_id, p_node=doc)
        new_node = PageNode(text=text, _id=_id, doc=doc)
        doc.add_page(new_node)
        self.nodes[_id] = new_node
        return new_node

    def add_source_node(self, text: str, page: PageNode, _id: str = None, org_text: str = None):
        _id = self.generate_id(_id=_id, p_node=page)
        new_node = SourceNode(text=text, _id=_id, page=page, original_text=org_text)
        page.add_source_node(new_node)
        self.nodes[_id] = new_node
        return new_node

    def add_map_node(self, text: str, source: SourceNode, _id: str = None, kind: int = T.undefined) -> MapNode:
        _id = self.generate_id(_id=_id, p_node=source)
        new_node = MapNode(text=text, _id=_id, source=source, kind=kind)
        source.add_map_node(new_node)
        self.nodes[_id] = new_node
        if kind == T.wish:
            new_node.add(self.future, T.parent)
            new_node.add(self.now, T.child)
        if kind == T.observation:
            new_node.add(self.future, T.parent)
            new_node.add(self.now, T.child)
        return new_node

    def remove_map_node(self, node: MapNode):
        for key, value in self.nodes:
            if value is node:
                del self.nodes[key]
                break
        node.delete()

    def generate_id(self, _id: str = None, p_node = None) -> str:
        # Generates an ID for Nodes like this with €€ is a number "DC€.€€.€€.€€"
        if _id is None:
            if isinstance(p_node, str):
                _id = re.sub(r'[^A-Z]',r'',p_node)
            if isinstance(p_node, DocNode):
                _id = p_node._id + "." + str(len(p_node.pages)+1)
            if isinstance(p_node, PageNode):
                _id = p_node._id + "." + str(len(p_node.source_parts)+1)
            if isinstance(p_node, SourceNode):
                _id = p_node._id + "." + str(len(p_node.map_nodes)+1)
        while _id in self.nodes:
            value_list = _id.split(".")
            if len(value_list) < 2:
                value_list.append("0")
            value_list[-1] = str(int(value_list[-1])+1)
            _id = ".".join(value_list)
        return _id

    def get_node_by_id(self, _id):
        return self.nodes[_id]

    def import_file(self, file_path: str, document_name: str):
        if file_path[-3:] == "pdf":
            self.import_pdf(file_path=file_path, document_name=document_name)
        elif file_path[-3:] == "csv":
            self.import_csv(file_path=file_path)

    def import_pdf(self, file_path: str, document_name: str):
        with open(file_path, "rb") as file:
            reader = PdfFileReader(file)
            new_doc = self.add_doc(title=document_name)
            for i, page in enumerate(reader.pages):
                new_page = self.add_page(text=(page.extractText()), doc=new_doc)
                for part in new_page.text.split(". "):
                    if part.strip():
                        self.add_source_node(text=(part.replace("-\n","").replace("\n"," ") + "."), page=new_page)

    def import_csv(self, file_path: str):
        # Import File
        with open(file_path, mode='r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #                   [0              1           2           3           4   ]
            # Node Row          [type,          _id,        text,       parent,     other: (title // org_text // kind))]
            # Connection Row    ["connection",  start: _id, ende: _id,  kind]
            for row in reader:
                if int(row[0]) == T.doc:
                    self.add_doc(title=row[4], text=row[2], _id=row[1])
                if int(row[0]) == T.page:
                    self.add_page(text=row[2], _id=row[1], doc=self.nodes[row[3]])
                if int(row[0]) == T.source:
                    self.add_source_node(text=row[2], _id=row[1], page=self.nodes[row[3]], org_text=row[4])
                if int(row[0]) == T.map_node:
                    self.add_map_node(text=row[2], _id=row[1], source=self.nodes[row[3]], kind=int(row[4]))
                if int(row[0]) == T.connection:
                    connect(start=self.nodes[row[1]], end=self.nodes[row[2]], kind=int(row[3]))

    def export_csv(self, file_path: str):
        # Export File
        with open(file_path, mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            map_nodes: [MapNode] = []

            for doc in self.doc_nodes:
                writer.writerow([T.doc, doc._id, doc.text, "", doc.title])
                for page in doc.pages:
                    writer.writerow([T.page, page._id, page.text, doc._id, "page"])
                    for source in page.source_parts:
                        writer.writerow([T.source, source._id, source.text, page._id, source.original_text])
                        for map_node in source.map_nodes:
                            writer.writerow([T.map_node, map_node._id, map_node.text, source._id, map_node.kind])
                            map_nodes.append(map_node)
            for map_node in map_nodes:
                for partner in map_node.parents:
                    writer.writerow([T.connection, map_node._id, partner._id, T.parent])
                for partner in map_node.children:
                    writer.writerow([T.connection, map_node._id, partner._id, T.child])
                for partner in map_node.equals:
                    writer.writerow([T.connection, map_node._id, partner._id, T.equal])
                for partner in map_node.opposites:
                    writer.writerow([T.connection, map_node._id, partner._id, T.opposed])
        file.close()

    def get_rows(self) -> [SourceNode]:
        result = []
        for doc in self.doc_nodes:
            for page in doc.pages:
                for part in page.source_parts:
                    result.append(part)
        return result

    def get_grafik_map(self) -> [int, int, [int, [int, int, MapNode]]]:
        result = []
        x = 0
        y = 0
        height = 0
        for doc in self.doc_nodes:
            for page in doc.pages:
                for part in page.source_parts:
                    for map_node in part.map_nodes:
                        if not bool(map_node.parents):
                            tree = map_node.get_tree_loc_and_size(x, y)
                            result.extend(tree)
                            x += map_node.size + T.offset
        for r in result:
            height = max(height, r[0])
        return [x, height, result]

    def get_np_grafik_map(self):
        return np.array(self.get_grafik_map())