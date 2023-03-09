import graphviz


h = graphviz.Digraph('SGI', format='svg')

h.node('start', 'SGI', shape='plaintext')
h.node('A', 'TERMINALS_BLOCK', shape='box')
h.node('B', 'KEYS_BLOCK', shape='box')
h.node('C', 'NONTERMINALS_BLOCK', shape='box')
h.node('D', 'AXIOM_BLOCK', shape='box')
h.node('F', 'ERROR_BLOCK', shape='box')
h.node('end', '', shape='point')

h.edge('start', 'A')
h.edge('A', 'B')
h.edge('B', 'C')
h.edge('C', 'D')
h.edge('D', 'F')
h.edge('D', 'end')
h.edge('F', 'end')

h.render(directory="_graphiz_data", view=True)
