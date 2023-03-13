from scanner import Tokenize
from afterscan import Afterscan
from dsl_token import *

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
            h.node(str(i), f"TERMINAL\ntype: {token.terminalType.name}\nstring: {token.str}", shape='box', color='red')
        elif Token.Type.KEY == token.type:
            h.node(str(i), f"KEY\nstring: {token.str}", shape='box', color='blue')
        h.edge(str(i - 1), str(i))
        i += 1
    h.node(str(i), '', shape='point')
    h.edge(str(i - 1), str(i))
    h.render(directory=debugInfoDir, view=True)


parser = ArgumentParser(prog="create_ast", description="Create AST")
parser.add_argument("-c", "--code", dest="codeFile", help="File with code", metavar="FILE", required=True)
parser.add_argument("-j", "--json", dest="jsonFile", help="Json file with settings", metavar="FILE", required=True)
args = parser.parse_args()

with open(args.jsonFile, 'r') as jsonFile:
    jsonData = json.loads(jsonFile.read())

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
