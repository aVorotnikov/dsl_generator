import pathlib
import pydot
from dsl_info import *
from syntax.core import *


def __GetType(shape):
    if shape[0] == '"':
        shape = shape[1:-1]
    if "plaintext" == shape:
        return NodeType.START
    if "point" == shape:
        return NodeType.END
    if "box" == shape:
        return NodeType.NONTERMINAL
    if "diamond" == shape:
        return NodeType.TERMINAL
    if "oval" == shape:
        return NodeType.KEY
    raise Exception(f"Insopported shape - {shape}")


def GetSyntaxDesription(diagramsDir, sgiFilePath):
    files = pathlib.Path(diagramsDir).glob('**/*.gv')
    res = dict()
    for file in files:
        print(f"Process {file.name}")
        source = pydot.graph_from_dot_file(file)
        diagram = source[0]
        a = diagram.get_type()
        if ("digraph" != diagram.get_type()):
            raise Exception("Virt diagram must be digraph")
        nodes = diagram.get_nodes()
        edges = diagram.get_edges()

        virtNodes = dict()
        startArray = []
        endArray = []
        for dotNode in nodes:
            attribs = dotNode.obj_dict["attributes"]
            str = "" if "label" not in attribs else attribs["label"]
            nodeType = __GetType("box" if "shape" not in attribs else attribs["shape"])
            if len(str) != 0 and str[0] == '"':
                str = str[1:-1]
            node = Node(nodeType, str)
            virtNodes[dotNode.get_name()] = node
            if NodeType.NONTERMINAL == nodeType:
                node.nonterminal = Nonterminal(str)
            elif NodeType.TERMINAL == nodeType:
                node.terminal = Terminal(str)
            elif NodeType.START == nodeType:
                startArray.append(node)
            elif NodeType.END == nodeType:
                endArray.append(node)
        if len(startArray) != 1:
            raise Exception(f"Incorrect number of starts")
        if len(endArray) != 1:
            raise Exception(f"Incorrect number of ends")
        for nodeName, node in virtNodes.items():
            outgoingEdges = [(edge.obj_dict["points"][1],
                              "" if "label" not in edge.obj_dict["attributes"] else edge.obj_dict["attributes"]["label"])
                             for edge in edges if edge.obj_dict["points"][0] == nodeName]
            for edge in outgoingEdges:
                if len(edge[1]) != 0 and edge[1][0] == '"':
                    code = edge[1][1:-1]
                else:
                    code = edge[1]
                node.nextNodes.append((virtNodes[edge[0]], code.replace('\\"', '"')))

        res[Nonterminal[diagram.get_name()]] = startArray[0]

    return res
