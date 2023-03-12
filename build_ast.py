from scanner import Tokenize
from afterscan import Afterscan
from dsl_token import *

from argparse import ArgumentParser
import json


parser = ArgumentParser(prog="create_ast", description="Create AST")
parser.add_argument("-c", "--code", dest="codeFile", help="File with code", metavar="FILE", required=True)
parser.add_argument("-j", "--json", dest="jsonFile", help="Json file with settings", metavar="FILE", required=True)
args = parser.parse_args()

with open(args.jsonFile, 'r') as jsonFile:
    jsonData = json.loads(jsonFile.read())

with open(args.codeFile, 'r') as codeFile:
    code = codeFile.read()

tokenList = Tokenize(code)
tokenList = Afterscan(tokenList)

print("tokens:")
for token in tokenList:
    if Token.Type.TERMINAL == token.type:
        print(f"TERMINAL, type: '{token.terminalType.name}', string: '{token.str}'.")
    elif Token.Type.KEY == token.type:
        print(f"KEY, string: '{token.str}'.")
