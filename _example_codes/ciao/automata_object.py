from enum import Enum
import pathlib


class AutomataObject:
    class Transition:
        class Type(Enum):
            CODE = 0
            ELSE = 1
            UNCONDITIONAL = 2


        def __init__(self, source, destination, conditionType, conditionCode, actionCode):
            self.source = source
            self.destination = destination
            self.type = conditionType
            if conditionType == AutomataObject.Transition.Type.CODE:
                self.conditionCode = conditionCode
            self.actionCode = actionCode


    @staticmethod
    def __TransitionFromDictionary(transitionDictionary):
        conditionCode = transitionDictionary["cond"]
        if conditionCode is None:
            type = AutomataObject.Transition.Type.UNCONDITIONAL
        elif conditionCode == "else":
            type = AutomataObject.Transition.Type.ELSE
            conditionCode = None
        else:
            type = AutomataObject.Transition.Type.CODE
        return AutomataObject.Transition(
            transitionDictionary["src"],
            transitionDictionary["dst"],
            type,
            conditionCode,
            transitionDictionary["action"]
        )


    class Function:
        def __init__(self, name, args):
            self.name = name
            self.args = args


    def __init__(self, name):
        self.name = name
        self.vars = []
        self.inners = []
        self.provideds = []
        self.requireds = []
        self.states = set()
        self.initialState = None
        self.transitions = []


    def AddVars(self, vars):
        self.vars += vars


    def AddInner(self, funcName, argList):
        self.inners.append(AutomataObject.Function(funcName, argList))


    def AddProvided(self, funcName, argList):
        self.provideds.append(AutomataObject.Function(funcName, argList))


    def AddRequired(self, funcName, argList):
        self.requireds.append(AutomataObject.Function(funcName, argList))


    def AddTransition(self, transitionDictionary):
        transition = AutomataObject.__TransitionFromDictionary(transitionDictionary)
        if len(self.transitions) == 0:
            self.initialState = transition.source
        self.states.add(transition.source)
        self.states.add(transition.destination)

        alreadyAddedTransitionTypes = [trans.type for trans in self.transitions if trans.source == transition.source]
        if transition.type == AutomataObject.Transition.Type.UNCONDITIONAL and len(alreadyAddedTransitionTypes) != 0:
            raise RuntimeError("Attempt to add unconditinal transition where another transitions already added")
        else:
            if AutomataObject.Transition.Type.UNCONDITIONAL in alreadyAddedTransitionTypes:
                raise RuntimeError("Attempt to add transition where unconditinal transition already added")
            if transition.type == AutomataObject.Transition.Type.ELSE and AutomataObject.Transition.Type.ELSE in alreadyAddedTransitionTypes:
                raise RuntimeError("Attempt to add 'else' transition where 'else' transition already added")
        self.transitions.append(transition)


    def __SeparatedArray(array, sep = ', '):
        res = ""
        for el in array:
            res = res + sep + el
        return res


    def __str__(self):
        templateDirectory = pathlib.Path("_example_data/ciao")
        automataObjectTemplateName = "automata_object_template.py"
        methodTemplateName = "method_template.py"
        endStateTemplateName = "end_state_template.py"
        unconditionalTransitionTemplateName = "unconditional_transition_template.py"
        ifTransitionTemplateName = "if_transition_template.py"
        elifTransitionTemplateName = "elif_transition_template.py"
        elseTransitionTemplateName = "else_transition_template.py"
        shift = "    "

        statesStr = ""
        for state in self.states:
            statesStr =  statesStr + '\n' + shift * 2 + f"{state} = '{state}'"

        varsStr = ""
        for var in self.vars:
            varsStr = varsStr + '\n' + shift * 2 + f"self.{var[0]} = {repr(var[1])}"

        requiredStr = ""
        if len(self.requireds) == 0:
            requiredStr = "No"
        else:
            for required in self.requireds:
                requiredStr = requiredStr + '\n' + shift + f"# {required.name}"

        with open(templateDirectory / methodTemplateName, 'r') as templateFile:
            methodTemplate = templateFile.read()

        innerStr = ""
        for inner in self.inners:
            innerStr = innerStr + methodTemplate.format(
                name = "__" + inner.name,
                args=AutomataObject.__SeparatedArray(inner.args))

        providedStr = ""
        for provided in self.provideds:
            providedStr = providedStr + methodTemplate.format(
                name = provided.name,
                args=AutomataObject.__SeparatedArray(provided.args))

        with open(templateDirectory / endStateTemplateName, 'r') as templateFile:
            endStateTemplate = templateFile.read()

        with open(templateDirectory / unconditionalTransitionTemplateName, 'r') as templateFile:
            unconditionalTransitionTemplate = templateFile.read()

        with open(templateDirectory / ifTransitionTemplateName, 'r') as templateFile:
            ifTransitionTemplate = templateFile.read()

        with open(templateDirectory / elifTransitionTemplateName, 'r') as templateFile:
            elifTransitionTemplate = templateFile.read()

        with open(templateDirectory / elseTransitionTemplateName, 'r') as templateFile:
            elseTransitionTemplate = templateFile.read()

        stateMachineStr = ""
        for state in self.states:
            transitions = [trans for trans in self.transitions if trans.source == state]
            if len(transitions) == 0:
                stateMachineStr = stateMachineStr + endStateTemplate.format(automataObject=self.name, state=state)
                continue
            unconditionalTransitions = [trans for trans in transitions if AutomataObject.Transition.Type.UNCONDITIONAL == trans.type]
            if len(unconditionalTransitions) != 0:
                if unconditionalTransitions[0].actionCode is None:
                    commandCode = ""
                else:
                    commandCode = "\n" + shift * 4 + unconditionalTransitions[0].actionCode
                stateMachineStr = stateMachineStr + unconditionalTransitionTemplate.format(
                    automataObject = self.name,
                    currentState = state,
                    nextState = unconditionalTransitions[0].destination,
                    command = commandCode)
                continue
            codeTransitions = [trans for trans in transitions if AutomataObject.Transition.Type.CODE == trans.type]
            elseTransitions = [trans for trans in transitions if AutomataObject.Transition.Type.ELSE == trans.type]
            if len(codeTransitions) == 0:
                if elseTransitions[0].actionCode is None:
                    commandCode = ""
                else:
                    commandCode = "\n" + shift * 4 + elseTransitions[0].actionCode
                stateMachineStr = stateMachineStr + unconditionalTransitionTemplate.format(
                    automataObject = self.name,
                    currentState = state,
                    nextState = elseTransitions[0].destination,
                    command = commandCode)
                continue
            stateMachineStr = stateMachineStr + "\n" + shift * 3 + f"if {self.name}.State.{state} == self.state:"

            template = ifTransitionTemplate
            for transition in codeTransitions:
                if transition.actionCode is None:
                    commandCode = ""
                else:
                    commandCode = "\n" + shift * 5 + transition.actionCode
                stateMachineStr = stateMachineStr + template.format(
                    condition = transition.conditionCode,
                    automataObject = self.name,
                    nextState = transition.destination,
                    command = commandCode)
                template = elifTransitionTemplate

            if len(elseTransitions) == 0:
                continue
            if elseTransitions[0].actionCode is None:
                commandCode = ""
            else:
                commandCode = "\n" + shift * 5 + elseTransitions[0].actionCode
            stateMachineStr = stateMachineStr + elseTransitionTemplate.format(
                automataObject = self.name,
                nextState = elseTransitions[0].destination,
                command = commandCode)

        with open(templateDirectory / automataObjectTemplateName, 'r') as templateFile:
            automataObjectTemplate = templateFile.read()

        return automataObjectTemplate.format(
            name = self.name,
            states = statesStr,
            vars = varsStr,
            initialState = self.initialState,
            required = requiredStr,
            inner = innerStr,
            provided = providedStr,
            stateMachine = stateMachineStr
        )
