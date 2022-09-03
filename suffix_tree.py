class Integer:

    def __init__(self, number):
        self.number = number

    def increment(self):
        self.number += 1

    def __str__(self):
        return f'{self.number}'

    def __int__(self):
        return self.number


class Node:
    counter = 1

    def __init__(self, name):
        self.name = name
        self.nodes = list()
        self.edges = list()
        self.suffix_link = None

    def add_node(self, _from, to):
        global string
        self.nodes.append(([_from, to], Node(f'node{Node.counter}')))
        self.edges.append(string[_from])
        Node.counter += 1

    def exists_edge(self, index, length):
        global string
        try:
            i = self.edges.index(string[index - length])
            return string[self.nodes[i][0][0] + length] == string[index]
        except ValueError:
            return False

    def split_edge(self, edge, length):
        global string, end
        temp = self.nodes[self.edges.index(edge)]
        temp[0][1] = temp[0][0] + length
        temp[1].add_node(temp[0][0] + length, end)
        return temp[1]

    def link_to(self, node):
        self.suffix_link = node

    def get_link(self):
        return self.suffix_link

    def check_end(self, edge, length):
        try:
            node = self.nodes[self.edges.index(edge)]
            if node[0][1] == node[0][0] + length:
                return node[1]
            return False
        except ValueError:
            return False

    def __str__(self):
        return self.name


def bfs(root):
    global string
    queue = list()
    queue.append(root)
    while queue:
        node = queue.pop(0)
        for edge, child in node.nodes:
            queue.append(child)
            print(f'{node.name} -> {child}: {string[edge[0]:int(edge[1])]}')


def dfs(root):
    for edge, child in root.nodes:
        print(f'{root.name} -> {child}: {string[edge[0]:int(edge[1])]}')
        dfs(child)


if __name__ == '__main__':
    # Initialization
    string = input('Enter a string without ending character: ') + '$'
    root = Node('root')
    remaining = 0
    active_node = root
    active_edge = '\0'
    active_length = 0
    end = Integer(0)

    for i in range(len(string)):
        remaining += 1
        end.increment()

        previous_new_node = None
        while remaining:
            if active_node.exists_edge(i, active_length):
                if active_length == 0:
                    active_edge = string[i]
                active_length += 1
                change_active_node = active_node.check_end(active_edge, active_length)
                if change_active_node:
                    active_node = change_active_node
                    active_edge = '\0'
                    active_length = 0
                break
            else:
                if active_length == 0:
                    active_node.add_node(i, end)
                    remaining -= 1
                elif active_length > 0:
                    new_node = active_node.split_edge(active_edge, active_length)
                    new_node.add_node(i, end)
                    remaining -= 1

                    if previous_new_node is None:  # rule 2
                        previous_new_node = new_node
                    else:
                        previous_new_node.link_to(new_node)
                        previous_new_node = new_node

                    if active_node is root:  # rule 1
                        active_edge = string[string.index(active_edge) + 1]
                        active_length -= 1
                    else:  # rule 3
                        node = active_node.get_link()
                        if node is None:
                            active_node = root
                        else:
                            active_node = node
    bfs(root)
