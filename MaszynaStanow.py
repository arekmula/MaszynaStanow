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
Awaria = automata.Automata()
Awaria.defineState("SygnalizacjaBledu", True, "SygnalizacjaBledu")
Awaria.defineState("PotwierdzenieBledu", False, "PotwierdzenieBledu")
Awaria.defineState("PowrotDoProcesu", False, "PowrotDoProcesu")
Awaria.defineState("WezwanieUR", False, "WezwanieUR")

alarm_states = Awaria.getStatesObjects()

Awaria.validTransitions(0, [1])
Awaria.validTransitions(1, [2, 3])
Awaria.validTransitions(3, [1])

Awaria.createTransitions("a")
alarm_transitions = Awaria.getTransitions()


# create a generator class


# create paths from transitions (exemplary)
# Sciezki glownego grafu
master.addPaths(["m_0_1", "m_1_2", "m_2_4"])
master.addPaths(["m_0_3", "m_3_0", "m_0_1", "m_1_2", "m_2_4"])
paths_master = master.getPaths()

# Sciezki grafu alarmu

Awaria.addPaths(["a_0_1", "a_1_2"])
Awaria.addPaths(["a_0_1", "a_1_3", "a_3_1", "a_1_2"])
paths_alarm = Awaria.getPaths()

automats = {
    "Master":master,
    "Awaria":Awaria
}

master.executePaths(automats)


print(master.getPath("WjazdKaroserii", "StanowiskoPuste"))
print(Awaria.getPath("SygnalizacjaBledu", "PowrotDoProcesu"))


