from scanner import Tokenize
from afterscan import Afterscan

from argparse import ArgumentParser


parser = ArgumentParser(
    prog="process_program",
    description="Process DSL program")
parser.add_argument("-d", "--dsl", dest="dslFile", help="File with DSL program", metavar="FILE", required=True)
parser.add_argument("-g", "--grammar", dest="grammarFile", help="File with DSL grammar", metavar="FILE", required=True)
args = parser.parse_args()

tokenList = Tokenize(args.dslFile)
tokenList = Afterscan(tokenList)
