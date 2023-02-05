import graphviz


h = graphviz.Graph('hello', format='svg')
h.edge('Hello', 'World')
h.render(directory="graphiz_data", view=True)
