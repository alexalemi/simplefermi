
import tree_sitter
import tree_sitter_fermi as tsfermi

FERMI = tree_sitter.Language(tsfermi.language())

def parse(s: str):
    parser = tree_sitter.Parser()
    parser.set_language(FERMI)
    return parser.parse(bytes(s, 'utf-8')).root_node
    return parser.parse(bytes(s, 'utf-8')).root_node.sexp()



