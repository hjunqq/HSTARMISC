from gpro.helper import isint


class Group:
    index = 0
    elements = []

    def __init__(self, index=0):
        self.index = index
        self.elements = []

    def set_element(self, elements):
        self.elements = elements

    def add_elem(self, elem):
        self.elements.append(elem.index)


class Element:
    index = 0
    nodes = []
    group = 0

    def __init__(self, index, nodes):
        self.index = index
        self.nodes = nodes

    def set_group(self, group):
        self.group = group


class Node:
    index = 0
    coordinates = []

    def __init__(self, index, coordinates):
        self.index = index
        self.coordinates = coordinates


class Mesh:
    n_node = 0
    n_element = 0
    node = []
    element = []
    group = []

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        c_group = None
        with open(self.file_path, 'r') as f:
            for line in f:
                vals = line.split()
                if vals[0].lower() == "mesh":
                    dest = 0
                elif vals[0].lower() == "coordinates":
                    dest = 1
                elif vals[0].lower() == "elements":
                    dest = 2
                elif vals[0].lower() == "end":
                    dest = -1

                if dest == 0:
                    if c_group is None:
                        c_group = Group()
                    else:
                        self.group.append(c_group)
                        c_group = Group()


                if isint(vals[0]):
                    if dest == 1:
                        node = Node(int(vals[0]), list(map(float, vals[1:])))
                        self.n_node += 1
                        self.node.append(node)
                    elif dest == 2:
                        elem = Element(int(vals[0]), list(map(int, vals[1:-1])))
                        group_index = int(vals[-1])
                        elem.set_group(group_index)
                        c_group.add_elem(elem)
                        self.n_element += 1
                        self.element.append(elem)
            self.group.append(c_group)
        print(self.n_node, self.n_element)
