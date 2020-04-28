from statemachine import StateMachine, State, Transition
from .generator import Generator

class Automata():
    options = []
    states = []
    from_to = []
    stateTransitions = {}
    paths = []

    def __init__(self):
        self.options = []
        self.states = []
        self.from_to = []
        self.stateTransitions = {}
        self.paths = []

        super(Automata, self).__init__()



    def defineState(self, name, initial, value):
        """
        :param name: State name
        :param initial: is state Initial
        :param value: value
        :return: void
        """
        option = {"name":name, "initial":initial, "value":value}
        self.options.append(option)


    def getStatesObjects(self):
        self.states = [State(**opt) for opt in self.options]
        return self.states

    def validTransitions(self, parent, childs):
        """
        :param parent: start of current transition
        :param childs: available goals of transition as list
        :return:
        """
        transition = [parent, childs]
        self.from_to.append(transition)

    def createTransitions(self, opLetter):
        for indices in self.from_to:
            from_idx, to_idx_tuple = indices
            for to_idx in to_idx_tuple:
                op_identifier = "{}_{}_{}".format(opLetter, from_idx, to_idx)

                transition = Transition(self.states[from_idx], self.states[to_idx], identifier=op_identifier)
                self.stateTransitions[op_identifier] = transition

                self.states[from_idx].transitions.append(transition)

    def getTransitions(self):
        return self.stateTransitions

    def addPaths(self, newPaths):
        """
        :param newPath: paths given in "opLetter_fromID_toID" format as list
        :return:
        """
        self.paths.append(newPaths)

    def getPaths(self):
        return self.paths

    def getPath(self, state1, state2):

        for path in self.paths:
            if state1 in path and state2 in path:
                if path.index(state1) < path.index(state2):
                    return path[path.index(state1):path.index(state2)+1]
                else:
                    return path[path.index(state2):path.index(state1)+1]

        return []

    def executePaths(self, automats):
        for path in self.paths:
            supervisor = Generator.create_master(self.states, self.stateTransitions)
            print('\n'+str(supervisor))

            print("executing path: {}".format(path))
            for event in path:
                self.stateTransitions[event]._run(supervisor)
                print(supervisor.current_state)

                for key in automats:
                    if supervisor.current_state.value == key:
                        print("Executing {} automat".format(key))
                        automats[key].executePaths(automats)
