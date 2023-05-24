# {name} automata object template
class {name}:
    # States
    class States(Enum):{states}


    # Constructor
    def __init__(self):{vars}
        self.state = {name}.States.{initialState}


    # REQUIRED:{required}


    # INNER
{inner}    # PROVIDED
{provided}    def run(self):
        while(True):{stateMachine}
