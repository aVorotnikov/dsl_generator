from scanner import Tokenize
from afterscan import Afterscan
from dsl_token import *
from syntax import *
import dsl_info
import attributor
import attribute_evaluator

from argparse import ArgumentParser
import json
import pathlib
import os
import shutil
import re


templateDirectory = pathlib.Path("_example_data/sgi")
dslInfoTemplateName = "dsl_info_template.py"
dslInfoFileName = "dsl_info.py"
dslAttrEvaluatorTemplateName = "attribute_evaluator_template.py"
dslAttrEvaluatorFileName = "attribute_evaluator.py"
aftescanTemplateName = "afterscan/afterscan_template.py"
aftescanFileName = "afterscan/afterscan.py"

parser = ArgumentParser(prog="create_ast", description="Create AST")
parser.add_argument("-c", "--code", dest="codeFile", help="File with code", metavar="FILE", required=True)
parser.add_argument("-j", "--json", dest="jsonFile", help="Json file with settings", metavar="FILE", required=False, default="_examples/rbnf/rbnf.json")
parser.add_argument("-d", "--dir", dest="directory", help="Directory to generate files", metavar="PATH", required=True)
args = parser.parse_args()

with open(args.jsonFile, 'r') as jsonFile:
    jsonData = json.loads(jsonFile.read())

syntaxInfo = GetSyntaxDesription(jsonData["syntax"])

with open(args.codeFile, 'r') as codeFile:
    code = codeFile.read()

tokenList = Tokenize(code)
tokenList = Afterscan(tokenList)
ast = BuildAst(syntaxInfo, dsl_info.axiom, tokenList)
attributor.SetAttributes(ast, attribute_evaluator.attributesMap)

for child in ast.childs:
    if TreeNode.Type.NONTERMINAL != child.type:
        raise Exception("Expected nonterminals only")
    elif dsl_info.Nonterminal.TERMINALS_BLOCK == child.nonterminalType:
        terminals = child.attribute
    elif dsl_info.Nonterminal.KEYS_BLOCK == child.nonterminalType:
        keys = child.attribute
    elif dsl_info.Nonterminal.NONTERMINALS_BLOCK == child.nonterminalType:
        nonterminals = child.attribute
    elif dsl_info.Nonterminal.AXIOM_BLOCK == child.nonterminalType:
        axiom = child.attribute
    elif dsl_info.Nonterminal.RULES_BLOCK == child.nonterminalType:
        rules = child

if axiom not in nonterminals:
    raise Exception("Axiom is not nonterminal")

rulesNonterminals = [rule.childs[0].attribute for rule in rules.childs if TreeNode.Type.NONTERMINAL == rule.type]
if len(rulesNonterminals) != len(set(rulesNonterminals)):
    raise Exception("Expect 1 rule for 1 nonterminal")
for nonterminal in rulesNonterminals:
    if nonterminal not in nonterminals:
        raise Exception(f"{nonterminal} not in terminal list")
for nonterminal in nonterminals:
    if nonterminal not in rulesNonterminals:
        raise Exception(f"{nonterminal} have no rule")

pathDirectory = pathlib.Path(args.directory)

os.makedirs(os.path.dirname(pathDirectory / aftescanFileName), exist_ok=True)
shutil.copy(templateDirectory / aftescanTemplateName, pathDirectory / aftescanFileName)

attributes = "\n"
attributeTemplate = "    # Nonterminal.{} : None,\n"
for nonterminal in nonterminals:
    attributes += attributeTemplate.format(nonterminal)
with open(templateDirectory / dslAttrEvaluatorTemplateName, 'r') as templateFile:
    templateText = templateFile.read()
dslAttrPath = pathDirectory / dslAttrEvaluatorFileName
os.makedirs(os.path.dirname(dslAttrPath), exist_ok=True)
with open(dslAttrPath, 'w') as file:
    file.write(templateText.format(attributes=attributes))

enumTemplate = '    {} = "{}"\n'
nonterminalsStr = "\n"
for nonterminal in nonterminals:
    nonterminalsStr += enumTemplate.format(nonterminal, nonterminal)
terminalsStr = "\n"
for terminal in terminals:
    terminalsStr += enumTemplate.format(terminal[0], terminal[0])
with open(templateDirectory / dslInfoTemplateName, 'r') as templateFile:
    templateText = templateFile.read()
terminalsRegularExpressionsTemplate = '    (Terminal.{}, r"{}"),\n'
terminalsRegularExpressions = "\n"
for terminal in terminals:
    terminalsRegularExpressions += terminalsRegularExpressionsTemplate.format(terminal[0], terminal[1].replace('"', '\\"'))

keysStr = "\n"
for key in keys:
    success = False
    for terminal in terminals:
        if re.match(terminal[1], key):
            keysStr += "    (\"{}\", Terminal.{}),\n".format(key, terminal[0])
            success = True
            break
    if not success:
        raise Exception(f"Failed to define terminal for '{key}' key")

dslInfoPath = pathDirectory / dslInfoFileName
os.makedirs(os.path.dirname(dslInfoPath), exist_ok=True)
with open(dslInfoPath, 'w') as file:
    file.write(templateText.format(
        terminals=terminalsStr,
        terminals_regex=terminalsRegularExpressions,
        keys=keysStr,
        nonterminals=nonterminalsStr,
        axiom=axiom))

class Node:
    def __init__(self, name, labels):
        self.name = name
        self.labels = labels

class Edge:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class Digraph:
    nodeName = "node{}"

    def __init__(self, name):
        self.nodes = []
        self.edges = []
        self.name = name
        self.counter = 0

    def AddNode(self, node):
        self.nodes.append(node)
        self.counter += 1

    def AddEdge(self, edge):
        self.edges.append(edge)

    def WriteToFile(self, fileName):
        with open(fileName, "w") as file:
            file.write(f"digraph {self.name} {{\n")
            for node in self.nodes:
                file.write(f"    {node.name}")
                if 0 != len(node.labels):
                    file.write(" [")
                    space = ""
                    for key, value in node.labels.items():
                        file.write(f"{space}{key}=\"{value}\"")
                        space = " "
                    file.write("]")
                file.write("\n")
            for edge in self.edges:
                file.write(f"    {edge.src.name} -> {edge.dst.name}\n")
            file.write("}\n")

dotDir = pathDirectory / "dot"
os.makedirs(dotDir, exist_ok=True)

def __SewNodes(digraph, starts, ends):
    for start in starts:
        for end in ends:
            digraph.AddEdge(Edge(start, end))

def __AnalyzeSequence(digraph, sequenceNonterminal):
    sequence = sequenceNonterminal.childs
    nodes = []
    for element in sequence:
        str = element.token.str
        if str in nonterminals:
            node = Node(digraph.nodeName.format(digraph.counter), {"label": str, "shape": "box"})
        elif str in [terminal[0] for terminal in terminals]:
            node = Node(digraph.nodeName.format(digraph.counter), {"label": str, "shape": "diamond"})
        else:
            node = Node(digraph.nodeName.format(digraph.counter), {"label": str, "shape": "oval"})
        digraph.AddNode(node)
        nodes.append(node)
    for i in range(len(nodes) - 1):
        digraph.AddEdge(nodes[i], nodes[i + 1])
    return [nodes[0]], [nodes[-1]], False

def __AnalyzeBrackets(digraph, bracketsNonterminal):
    rhss = [child for child in bracketsNonterminal.childs if TreeNode.Type.NONTERMINAL == child.type]
    starts = []
    ends = []
    sew = False
    for rhs in rhss:
        starts0, ends0, sew0 = __AnalyzeRhs(digraph, rhs)
        if sew0:
            sew = True
        starts += starts
        ends += ends0
    return starts, ends, sew

def __AnalyzeOptional(digraph, bracketsNonterminal):
    rhss = [child for child in bracketsNonterminal.childs if TreeNode.Type.NONTERMINAL == child.type]
    starts = []
    ends = []
    for rhs in rhss:
        starts0, ends0, sew0 = __AnalyzeRhs(digraph, rhs)
        starts += starts
        ends += ends0
    return starts, ends, True

def __AnalyzeTseitinIteration(digraph, tseitinNonterminal):
    if 2 == len(tseitinNonterminal.childs):
        return [], [], True
    if 3 == len(tseitinNonterminal.childs) and TreeNode.Type.NONTERMINAL != tseitinNonterminal.childs[1].type:
        return [], [], True
    if 3 == len(tseitinNonterminal.childs):
        return __AnalyzeRhs(digraph, tseitinNonterminal.childs[1])
    if 4 == len(tseitinNonterminal.childs):
        res = __AnalyzeRhs(digraph, tseitinNonterminal.childs[2])
        res[2] = True
        return res
    rhs1Res = __AnalyzeRhs(digraph, tseitinNonterminal.childs[1])
    rhs2Res = __AnalyzeRhs(digraph, tseitinNonterminal.childs[3])
    __SewNodes(digraph, rhs1Res[1], rhs2Res[0])
    __SewNodes(digraph, rhs2Res[1], rhs1Res[0])
    return rhs1Res[0], rhs1Res[1], rhs1Res[2]

def __AnalyzeRhs(digraph, rhsNonterminal):
    nodes = []
    for child in rhsNonterminal.childs:
        if dsl_info.Nonterminal.SEQUENCE == child.nonterminalType:
            nodes.append(__AnalyzeSequence(digraph, child))
        elif dsl_info.Nonterminal.BRACKETS == child.nonterminalType:
            node = __AnalyzeBrackets(digraph, child)
            nodes.append(node)
        elif dsl_info.Nonterminal.OPTIONAL == child.nonterminalType:
            node = __AnalyzeOptional(digraph, child)
            nodes.append(node)
        elif dsl_info.Nonterminal.TSEITIN_ITERATION == child.nonterminalType:
            node = __AnalyzeTseitinIteration(digraph, child)
            nodes.append(node)
    sew = True
    starts = []
    nodesToLink = []
    for i in range(len(nodes)):
        if sew:
            starts += nodes[i][0]
            sew = nodes[i][2]
        __SewNodes(digraph, nodesToLink, nodes[i][0])
        if not nodes[i][2]:
            nodesToLink = []
        nodesToLink += nodes[i][1]
    return starts, nodesToLink, sew

for rule in rules.childs:
    if TreeNode.Type.NONTERMINAL != rule.type:
        continue
    digraph = Digraph(rule.childs[0].attribute)
    start = Node(digraph.nodeName.format(digraph.counter), {"label": digraph.name, "shape": "plaintext"})
    digraph.AddNode(start)
    end = Node(digraph.nodeName.format(digraph.counter), {"label": "", "shape": "point"})
    digraph.AddNode(end)
    starts, ends, sew = __AnalyzeRhs(digraph, rule.childs[2])
    __SewNodes(digraph, [start], starts)
    __SewNodes(digraph, ends, [end])
    if sew:
        __SewNodes(digraph, [start], [end])
    digraph.WriteToFile(dotDir / f"{digraph.name.lower()}.gv")
