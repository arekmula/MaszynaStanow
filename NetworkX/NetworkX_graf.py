import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

G = nx.Graph()
# NODE
G.add_node('Wjazd karoserii', pos=(50,300), node_color='Wjazd karoserii')
G.add_node('Karoseria w pozycji', pos=(50,200), node_color='Karoseria w pozycji')
G.add_node('Zadanie wykonane', pos=(50,100), node_color='Zadanie wykonane')
G.add_node('Stanowisko puste', pos=(50,2), node_color='Stanowisko puste')
G.add_node('Awaria', pos=(5,22), node_color='Awaria')
# EDGE
G.add_edge('Wjazd karoserii', 'Karoseria w pozycji', weight = 'm_0_1', edge_color='m_0_1')
G.add_edge( 'Karoseria w pozycji', 'Zadanie wykonane', weight = 'm_1_2', edge_color='m_1_2')
G.add_edge( 'Zadanie wykonane', 'Stanowisko puste' , weight = 'm_2_3', edge_color='m_2_3')
G.add_edge('Wjazd karoserii', 'Awaria', weight = 'm_1_4', edge_color='m_1_4')
G.add_edge( 'Karoseria w pozycji', 'Awaria', weight = 'm_2_4', edge_color='m_2_4')
G.add_edge( 'Zadanie wykonane', 'Awaria', weight = 'm_3_4' , edge_color='m_3_4')
G.add_edge( 'Zadanie wykonane', 'Wjazd karoserii' , weight = '', edge_color='m_3_0')

# NODE
A = nx.Graph()
A.add_node('Sygnalizacja bledu', pos=(150,300),node_color='Sygnalizacja bledu')
A.add_node('Potwierdzenie bledu', pos=(150,150),node_color='Potwierdzenie bledu')
A.add_node('Powrot do procesu', pos=(120,2),node_color='Powrot do procesu')
A.add_node('Wezwanie UR', pos=(180,2),node_color='Wezwanie UR')
# EDGE
A.add_edge('Sygnalizacja bledu', 'Potwierdzenie bledu', weight = 'a_0_1', edge_color='a_0_1')
A.add_edge('Potwierdzenie bledu', 'Powrot do procesu', weight = 'a_1_2', edge_color='a_1_2')
A.add_edge('Potwierdzenie bledu', 'Wezwanie UR', weight = 'a_1_3', edge_color='a_1_3')


weight = nx.get_edge_attributes(G, 'weight')
pos = nx.get_node_attributes(G, 'pos')
node_color = nx.get_node_attributes(G, 'node_color')
edge_color = nx.get_edge_attributes(G, 'edge_color')

node_colorA = nx.get_node_attributes(A, 'node_color')
edge_colorA = nx.get_edge_attributes(A, 'edge_color')
weightA = nx.get_edge_attributes(A, 'weight')
posA = nx.get_node_attributes(A, 'pos')

nodes_G = {'Wjazd karoserii': 'blue', 'Karoseria w pozycji': 'blue','Zadanie wykonane': 'blue' ,'Stanowisko puste': 'blue',  'Awaria': 'blue'}
edges_G = {'m_0_1': 'black','m_1_2': 'black','m_2_3': 'black','m_1_4': 'black','m_2_4': 'black','m_3_4': 'black','m_3_0': 'black'}
nodes_A = {'Sygnalizacja bledu': 'blue','Potwierdzenie bledu': 'blue',  'Powrot do procesu': 'blue', 'Wezwanie UR' : 'blue'}
edges_A = {'a_0_1': 'black','a_1_2': 'black','a_1_3': 'black','a_3_1': 'black'}

list_of_events = ['Wjazd karoserii','Karoseria w pozycji',  'Zadanie wykonane', 'Awaria' , 'Stanowisko puste']
list_of_events2 = ['Sygnalizacja bledu', 'Potwierdzenie bledu', 'Powrot do procesu', 'Wezwanie UR']
wykonanie_zadania = 0
while True:
    for event in list_of_events:

        if wykonanie_zadania == 1:
            nodes_G['Zadanie wykonane'] = 'red'
            nx.draw_networkx(G, pos, node_color=[nodes_G[x] for x in node_color.values()],
                         edge_color=[edges_G[x] for x in edge_color.values()])
            plt.pause(1)
            nodes_G['Zadanie wykonane'] = 'blue'
            nx.draw_networkx(G, pos, node_color=[nodes_G[x] for x in node_color.values()],
                         edge_color=[edges_G[x] for x in edge_color.values()])
            wykonanie_zadania = 0

        nodes_G[event] = 'red'

        nx.draw_networkx(G, pos, node_color = [nodes_G[x] for x in node_color.values()], edge_color = [edges_G[x] for x in edge_color.values()])
        nx.draw_networkx_edge_labels(G, pos, edge_labels = weight)

        if event == 'Awaria':
            for event2 in list_of_events2:
                nodes_A[event2] = 'red'
                nx.draw_networkx(A, posA, node_color=[nodes_A[x] for x in node_colorA.values()])
                nx.draw_networkx_edge_labels(A, posA, edge_labels=weightA)
                plt.pause(1)
                nodes_A[event2] = 'blue'
                nx.draw_networkx(A, posA, node_color=[nodes_A[x] for x in node_colorA.values()])
                if event2 == 'Powrot do procesu':
                    wykonanie_zadania = 1
                    break

        else:
            nx.draw_networkx(A, posA, node_color=[nodes_A[x] for x in node_colorA.values()])
            nx.draw_networkx_edge_labels(A, posA, edge_labels = weightA)

        plt.pause(1)
        nodes_G[event] = 'blue'
        nx.draw_networkx(G, pos, node_color = [nodes_G[x] for x in node_color.values()], edge_color = [edges_G[x] for x in edge_color.values()])


plt.show()
















