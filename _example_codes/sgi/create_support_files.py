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
parser.add_argument("-j", "--json", dest="jsonFile", help="Json file with settings", metavar="FILE", required=False, default="_examples/sgi/sgi.json")
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

if axiom not in nonterminals:
    raise Exception("Axiom is not nonterminal")

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
