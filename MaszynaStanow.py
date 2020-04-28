from statemachine import StateMachine, State, Transition

from machine import automata

# ******************* MASTER AUTOMATA **********************
master = automata.Automata()

master.defineState("WjazdKaroserii", True, "WjazdKaroserii")
master.defineState("KaroseriaWPozycji", False, "KaroseriaWPozycji")
master.defineState("ZadanieWykonane", False, "ZadanieWykonane")
master.defineState("Awaria", False, "Awaria")
master.defineState("StanowiskoPuste", False, "StanowiskoPuste")

master_states = master.getStatesObjects()

master.validTransitions(0, [1, 3])
master.validTransitions(1, [2, 3])
master.validTransitions(2, [3, 4])
master.validTransitions(3, [0, 1, 2])
master.validTransitions(4, [0])

master.createTransitions("m")
master_transitions = master.getTransitions()

# ******************** ALARM AUTOMATA ***********************
alarm = automata.Automata()
alarm.defineState("SygnalizacjaBledu", True, "SygnalizacjaBledu")
alarm.defineState("PotwierdzenieBledu", False, "PotwierdzenieBledu")
alarm.defineState("PowrotDoProcesu", False, "PowrotDoProcesu")
alarm.defineState("WezwanieUR", False, "WezwanieUR")

alarm_states = alarm.getStatesObjects()

alarm.validTransitions(0, [1])
alarm.validTransitions(1, [2, 3])
alarm.validTransitions(3, [1])

alarm.createTransitions("a")
alarm_transitions = alarm.getTransitions()


# create a generator class


# create paths from transitions (exemplary)
# Sciezki glownego grafu
master.addPaths(["m_0_1", "m_1_2", "m_2_4"])
master.addPaths(["m_0_3", "m_3_0", "m_0_1", "m_1_2", "m_2_4"])
paths_master = master.getPaths()

# Sciezki grafu alarmu

alarm.addPaths(["a_0_1", "a_1_2"])
alarm.addPaths(["a_0_1", "a_1_3", "a_3_1", "a_1_2"])
paths_alarm = alarm.getPaths()

master.executePaths()
alarm.executePaths()
