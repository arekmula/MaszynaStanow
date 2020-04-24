from statemachine import StateMachine, State, Transition

# define states for a master (way of passing args to class)
options = [
    {"name": "WjazdKaroserii", "initial": True, "value": "WjazdKaroserii"},  # 0
    {"name": "KaroseriaWPozycji", "initial": False, "value": "KaroseriaWPozycji"},  # 1
    {"name": "ZadanieWykonane", "initial": False, "value": "ZadanieWykonane"},  # 2
    {"name": "Awaria", "initial": False, "value": "Awaria"},  # 3
    {"name": "StanowiskoPuste", "initial": False, "value": "StanowiskoPuste"},  # 4
]

# create State objects for a master
master_states = [State(**opt) for opt in options]

# valid transitions for a master (indices of states from-to)
from_to = [
    [0, [1, 3]],
    [1, [2, 3]],
    [2, [3, 4]],
    [3, [0, 1, 2]],
    [4, [0]]
]

# create transitions for a master
master_transitions = {}
for indices in from_to:
    from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
    for to_idx in to_idx_tuple:  # iterate over destinations from a source state
        op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

        # create transition object and add it to the master_transitions dict
        transition = Transition(master_states[from_idx], master_states[to_idx], identifier=op_identifier)
        master_transitions[op_identifier] = transition

        # add transition to source state
        master_states[from_idx].transitions.append(transition)


# create a generator class
class Generator(StateMachine):
    states = []
    transitions = []
    states_map = {}
    current_state = None

    def __init__(self, states, transitions):

        # creating each new object needs clearing its variables
        self.states = []
        self.transitions = []
        self.states_map = {}
        self.current_state = states[0]

        # create fields of states and transitions using setattr()
        # create lists of states and transitions
        # create states map - needed by StateMachine to map states and its values
        for s in states:
            setattr(self,str(s.name).lower(), s)
            self.states.append(s)
            self.states_map[s.value] = str(s.name)

        for key in transitions:
            setattr(self, str(transitions[key].identifier).lower(), transitions[key])
            self.transitions.append(transitions[key])

        super(Generator, self).__init__()

    def __repr__(self):
        return "{}(model={!r}, state_field={!r}, current_state={!r})".format(type(self).__name__, self.model, self.state_field,
                                                                             self.current_state.identifier, )

    @classmethod
    def create_master(cls, states, transitions) -> 'Generator':
        return cls(states, transitions)

# create paths from transitions (exemplary)
path_1 = ["m_0_1", "m_1_2", "m_2_4"]
path_2 = ["m_0_3", "m_3_0", "m_0_1", "m_1_2", "m_2_4"]
paths = [path_1, path_2]

for path in paths:
    supervisor = Generator.create_master(master_states, master_transitions)
    print('\n'+str(supervisor))

    print("executing path: {}".format(path))
    for event in path:

        master_transitions[event]._run(supervisor)
        print(supervisor.current_state)

        # add slave
        if supervisor.current_state.value == "WjazdKaroserii":
            # TODO: automata 1 (for) slave1
            ...

        if supervisor.current_state.value == "KaroseriaWPozycji":
            # TODO: automata 2 (for) slave2
            ...

        if supervisor.current_state.value == "ZadanieWykonane":
            # TODO: automata 3 (for) slave3
            ...

        if supervisor.current_state.value == "StanowiskoPuste":
            # TODO: automata 4 (for) slave 4
            ...
        if supervisor.current_state.value == "Awaria":
            # TODO: automata 5 (for) slave 5
            print("Awaria!")