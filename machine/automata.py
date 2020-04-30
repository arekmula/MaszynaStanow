from statemachine import StateMachine, State, Transition
from .generator import Generator
import re
from itertools import groupby
import robopy.base.model as robot
from commands.moves import move_j
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt


class Automata():
    options = []
    states = []
    from_to = []
    stateTransitions = {}
    paths = []
    joints = {}

    def __init__(self):
        self.options = []
        self.states = []
        self.from_to = []
        self.stateTransitions = {}
        self.paths = []
        self.joints = {}

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

    def getPathName(self):
        for transition in self.getTransitions():
            i = transition.find('_')
            return transition[:i]

    def getValuesFromString(self, string):
        i = string.find('_')
        string = string[i + 1:]
        i = string.find('_')
        end = string[i + 1:]
        start = string[:i]

        return start,end



    def getPath(self, state_in, state_out):

        transitions = self.getTransitions()
        states = self.getStatesObjects()

        #convert state names to numbers
        i = 0
        for state in states:
            if state.value == state_in:
                state_in = i
            if state.value == state_out:
                state_out = i
            i += 1

        #BFS algorithm
        dict = {}
        toVisit = [state_in]
        visited = set()
        isParent = [state_in]

        while len(toVisit)>0:
            isVisited = False


            # find next state
            while(not isVisited):
                if len(toVisit) == 0:
                    return []
                if(toVisit[0] in visited):
                    toVisit.pop(0)
                else:
                    consideredState = toVisit[0]
                    isVisited = True
            visited.add(consideredState)

            # if sought state is found, stop the loop
            if consideredState == state_out:
                break

            # find possible transitions
            for transition in transitions:
                start,end = self.getValuesFromString(transition)
                if int(start) == consideredState:
                    toVisit.append(int(end))
                    if int(end) not in isParent:
                        dict[int(end)] = int(start)
                        isParent.append(int(end))

        #get int path
        path = []
        path.append(state_out)

        flag = 0
        while flag == 0:
            state = dict.get(path[-1])

            path.append(state)
            if state == state_in:
                flag = 1

        #convert int path to string
        path_name = self.getPathName()
        transitions_out = []

        path.reverse()
        for i in range(len(path)-1):
            transitions_out.append(path_name+"_"+str(path[i])+"_"+str(path[i+1]))


        return transitions_out



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


    def addJointPositions(self, stateName, jointPositions):
        """
        add joint positions for given state
        :param stateName: state of automata where you add joint positions
        :param jointPositions: list of joint positions
        :return:
        """
        self.joints[stateName] = jointPositions

    def moveRobot(self, stateNames):
        model=robot.Puma560()  # defining robot as Puma 560
        jointStates = [self.joints[x] for x in stateNames]  # getting joints for each given state
        paths = []

        for i in range(0,len(jointStates)-1):
            path = move_j(model, jointStates[i], jointStates[i+1])
            paths.append(path)

        path = np.concatenate(paths, axis=0)
        print(path)

        model.animate(stances=path, unit='deg', frame_rate=30)





    def visualizeRobot(self, path):
        states = []
        for p in path:
            indexes = re.findall('\d+', p)  # finding indexes of states in path
            states.append(int(indexes[0]))
            states.append(int(indexes[1]))
        states = [i[0] for i in groupby(states)]  # deleting duplicate states that are neighbours

        stateNames = []

        for i in states:
            stateNames.append((self.options[i])["name"])  # getting stateNames corresponding to their indexes

        self.moveRobot(stateNames)

    def graf(self, path):
        states = []
        for p in path:

            indexes = re.findall('\d+', p)  # finding indexes of states in path
            states.append(int(indexes[0]))
            states.append(int(indexes[1]))
        states = [i[0] for i in groupby(states)]  # deleting duplicate states that are neighbours
        stateNames = []

        for i in states:
            stateNames.append((self.options[i])["name"])  # getting stateNames corresponding to their indexes

        self.graf_visu(stateNames, states)

    def graf_visu(self, stateNames, states):

        G = nx.Graph()
        nodes_G = {}
        # NODE
        position_y = 300
        for name in stateNames:
            G.add_node(name, pos=(50, position_y), node_color=name)
            position_y -= 100
            nodes_G[name]='blue'
        # EDGE
        i = 0
        for state in states:
            if i+1 < len(stateNames):
                G.add_edge(stateNames[i], stateNames[i+1], weight=state, edge_color=state)
                i += 1

        weight = nx.get_edge_attributes(G, 'weight')
        pos = nx.get_node_attributes(G, 'pos')
        node_color = nx.get_node_attributes(G, 'node_color')

        for event in stateNames:
            nodes_G[event] = 'red'
            nx.draw_networkx(G, pos, node_color=[nodes_G[x] for x in node_color.values()])
            plt.pause(1)
            nodes_G[event] = 'blue'
            nx.draw_networkx(G, pos, node_color=[nodes_G[x] for x in node_color.values()])
        plt.show()



