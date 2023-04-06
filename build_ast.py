from scanner import Tokenize
from afterscan import Afterscan
from dsl_token import *
from syntax import *
import dsl_info
import attributor
import attribute_evaluator

import graphviz
from argparse import ArgumentParser
import json
import pathlib
import os


def __RenderTokenStream(diagramName, tokenList, debugInfoDir):
    if debugInfoDir is None:
        return
    h = graphviz.Digraph(diagramName, format='svg')
    h.node('0', '', shape='point')
    i = 1
    for token in tokenList:
        if Token.Type.TERMINAL == token.type:
            h.node(str(i),
                   f"TERMINAL\ntype: {token.terminalType.name}\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""),
                   shape='diamond')
        elif Token.Type.KEY == token.type:
            h.node(str(i), f"KEY\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""), shape='oval')
        h.edge(str(i - 1), str(i))
        i += 1
    h.node(str(i), '', shape='point')
    h.edge(str(i - 1), str(i))
    h.render(directory=debugInfoDir, view=True)


def __RenderAst(diagramName, ast, debugInfoDir):
    if debugInfoDir is None:
        return
    h = graphviz.Digraph(diagramName, format='svg')
    i = 1
    nodes = [(ast, 0)]
    while len(nodes):
        node = nodes[0]
        if TreeNode.Type.NONTERMINAL == node[0].type:
            h.node(str(i),
                   f"NONTERMINAL\ntype: {node[0].nonterminalType}" + (f"\nattribute: {node[0].attribute}" if node[0].attribute else ""),
                   shape='box')
            if node[1] != 0:
                h.edge(str(node[1]), str(i))
            nodes += [(child, i) for child in node[0].childs]
        else:
            token = node[0].token
            if Token.Type.TERMINAL == token.type:
                h.node(str(i),
                       f"TERMINAL\ntype: {token.terminalType.name}\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""),
                       shape='diamond')
            elif Token.Type.KEY == token.type:
                h.node(str(i), f"KEY\nstring: {token.str}" + (f"\nattribute: {token.attribute}" if token.attribute else ""), shape='oval')
            h.edge(str(node[1]), str(i))
        nodes = nodes[1:]
        i += 1
    h.render(directory=debugInfoDir, view=True)


parser = ArgumentParser(prog="create_ast", description="Create AST")
parser.add_argument("-c", "--code", dest="codeFile", help="File with code", metavar="FILE", required=True)
parser.add_argument("-j", "--json", dest="jsonFile", help="Json file with settings", metavar="FILE", required=True)
args = parser.parse_args()

with open(args.jsonFile, 'r') as jsonFile:
    jsonData = json.loads(jsonFile.read())

syntaxInfo = GetSyntaxDesription(jsonData["syntax"])

if "debugInfoDir" in jsonData:
    debugInfoDir = pathlib.Path(jsonData["debugInfoDir"])
    if not debugInfoDir.exists():
        os.mkdir(debugInfoDir)
else:
    debugInfoDir = None

with open(args.codeFile, 'r') as codeFile:
    code = codeFile.read()

tokenList = Tokenize(code)
__RenderTokenStream('token_stream_after_scanner', tokenList, debugInfoDir)
tokenList = Afterscan(tokenList)
__RenderTokenStream('token_stream_after_afterscan', tokenList, debugInfoDir)

ast = BuildAst(syntaxInfo, dsl_info.axiom, tokenList)
__RenderAst('ast', ast, debugInfoDir)
attributor.SetAttributes(ast, attribute_evaluator.attributesMap)
__RenderAst('ast_attributed', ast, debugInfoDir)
