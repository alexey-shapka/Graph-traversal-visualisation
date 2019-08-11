import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import time

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
class Graph:
    def __init__(self, speed=25):
        self.current_path = {}      #path on current turn to execute  
        self.node_coordinates = {}  #node coordinates
        self.ants = []              #list with ants (Ant class)
        self.graph = []             #logic graph edges
        self.turns = []             #paths to find end point    
        self.file = 'data.txt'      #read data to create
        self.figure = None
        self.animation = None
        self.ants_dots = None      
        self.speed = speed
        self.read_file()
        self.create_nodes()
        self.create_edges()

    def read_file(self):
        ants, start = 0, [0, 0]
        with open(self.file, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if '#' not in lines[i] and lines[i] != '\n':
                    if len(lines[i]) == 2:
                        ants = int(lines[i])
                    elif 'L' in lines[i]:
                        self.turns.append([list(map(int, j[1:].split('-'))) for j in lines[i].rstrip().split(' ')])
                    else:
                        if '-' in lines[i]:
                            self.graph.append(lines[i].replace('\n', '').split('-'))
                        else:
                            data = lines[i].split(' ')
                            self.node_coordinates[data[0]] = list(map(int, data[1:]))
                elif '##start' in lines[i]:
                    start = list(map(int, lines[i+1].split(' ')))[1:]

        for i in range(ants):
            self.ants.append(Ant(*start))

    def create_nodes(self):
        self.figure, self.ax = plt.subplots(figsize=(10,5))
        self.figure.canvas.set_window_title('HELP ANTS TO FIND THEIR HOME')
        keys, values = list(self.node_coordinates.keys()), list(self.node_coordinates.values())
        x, y = [i[0] for i in values], [i[1] for i in values]
        self.ax.scatter(x, y, color='red', s=70)
        for i in range(len(x)):
            self.ax.annotate(str(keys[i]), (x[i], y[i]), color='black', xytext=(x[i], y[i] + 0.3))
        plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
        plt.subplots_adjust(wspace=0.05, hspace=1, bottom=0.2, top=0.95, right=0.94, left=0.06)
        self.ants_dots, = plt.plot([], [], 'b8')

    def create_edges(self):
        for i in self.graph:
            x = [self.node_coordinates[i[0]][0], self.node_coordinates[i[1]][0]]
            y = [self.node_coordinates[i[0]][1], self.node_coordinates[i[1]][1]]
            plt.plot(x, y, color='#000000')

    def create_path(self, start_x, start_y, end_x, end_y, key):
        self.current_path[key] = [np.linspace(start_x, end_x, num=self.speed).tolist(),
                                  np.linspace(start_y, end_y, num=self.speed).tolist()]

    def show_ants_ways(self, interface):
        if len(self.current_path) == 0:
            if len(self.turns) != 0:
                turn = self.turns.pop(0)
                for i in turn:
                    ant = self.ants[i[0]-1]
                    self.create_path(ant.x, ant.y, *self.node_coordinates[str(i[1])], i[0]-1)
            else:
                self.animation.event_source.stop()
                plt.xlabel('\nEveryone at home!', fontsize=13, horizontalalignment='center')
        
        for i in self.current_path:
            if len(self.current_path[i][0]) != 0:
                self.ants[i].move(self.current_path[i][0].pop(0), self.current_path[i][1].pop(0))
            else:
                self.current_path.clear()
                break    

        return self.ants_dots.set_data([i.x for i in self.ants], [i.y for i in self.ants])
    
    def show(self):
        self.animation = animation.FuncAnimation(self.figure, self.show_ants_ways, frames=200, interval=20)
        plt.show()

g = Graph(speed=20)
g.show()