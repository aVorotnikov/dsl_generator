from syntax.core import *
import syntax.virt
from syntax.build_ast import *


def GetSyntaxDesription(syntaxParameters):
    if SyntaxDescriptionType.VIRT_DIAGRAMS.value == syntaxParameters["type"]:
        return syntax.virt.GetSyntaxDesription(syntaxParameters["info"]["diagrams"], syntaxParameters["info"]["supportInfo"])
    if SyntaxDescriptionType.RBNF.value == syntaxParameters["type"]:
        raise Exception("RBNF not supported yet")
    raise Exception("Unsupported syntax description type")
