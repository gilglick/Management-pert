from collections import defaultdict
import logging

# Authors:
# Jonathan Kartaq

logging.basicConfig(filename='hw2logger.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# The queue is used for the implementation of the topological sort
class Queue(object):
    def __init__(self):
        self.queue = []
        logging.info("New queue has been created, name: " + str(self.queue))

    def is_empty(self):
        return self.queue == []

    def insert(self, item):
        self.queue.insert(0, item)
        logging.info("New item insereted to queue: " + str(item))

    def delete(self):
        logging.info("Deleted item from queue: " + str(self.queue[0]))
        return self.queue.pop()

    def size(self):
        logging.info("Size of queue is = " + str(len(self.queue)))
        return len(self.queue)

    def __str__(self):
        logging.info("Queue's str func called for " + str(list(self.queue)))
        return "Queue list:" + str(list(self.queue))


# -------------------------------------------------------------------------------------------
class Node(object):
    def __init__(self, name):
        self.name = str(name)
        self.EE = 0
        self.LE = 0
        self.degree = 0
        logging.info("New node: " + repr(self) + " with name: " + name)

    def node_slack_time(self):
        logging.info("Node slack time called for node : " + self.name + " slack = " + str(self.LE - self.EE))
        return self.LE - self.EE

    def __str__(self):
        logging.info("Node's str method called for '" + repr(self))
        return "Node: " + self.name + " | EE/LE = " + str(self.EE) + "/" + str(self.LE)

    def __repr__(self):
        logging.info("Node's repr called for " + self.name)
        return self.name


# --------------------------------------------------------------------------------------------
class Activity(object):
    def __init__(self, name, duration):
        logging.info("New activity created, name: " + name + ", duration: " + str(duration))
        self.name = str(name)
        self.duration = duration

    def __str__(self):
        logging.info("Activity's str method called for: " + self.name + "' activity")
        return "Name: " + self.name + " | Duration = " + str(self.duration)

    def __repr__(self):
        logging.info("Activity's repr called for " + self.name)
        return self.name


# --------------------------------------------------------------------------------------------
class Pert(object):

    def __init__(self, graph_dict=None):
        logging.info("New pert: " + repr(self) + "' has been created, graph: " + str(graph_dict))
        if graph_dict is None:
            graph_dict = dict()
        self.__graph_dict = graph_dict
        self.topological_list = []

    def __str__(self):
        logging.info("str method called for: " + repr(self) + "' pert")
        string = "Adjacency list: \n"
        for vertex in self:
            string += repr(vertex) + " -> " + repr(list(self[vertex])) + "\n"
        return string

    def __getitem__(self, name):
        logging.info("__getitem__ method called for: " + repr(self) + "' pert")
        return self.__graph_dict[name]

    # iterator the iterate over the nodes
    def __iter__(self):
        logging.info("__iter__ method called for: " + repr(self) + "' pert")
        return iter(self.__graph_dict)

    def keys(self):
        logging.info("keys method called for: " + repr(self) + "' pert")
        return self.__graph_dict.keys()

    def items(self):
        logging.info("items method called for: " + repr(self) + "' pert")
        return self.__graph_dict.items()

    def values(self):
        logging.info("values method called for: " + repr(self) + "' pert")
        return self.__graph_dict.values()

    def find_node_degree(self):
        logging.info("find_node_degree method called for: " + repr(self) + "' pert")
        for node in self:
            for lst in self[node]:
                lst[0].degree = lst[0].degree + 1

    # Method to the critcal path: implemetation of topological sort
    def tp_sort(self, direction):
        logging.info("tp_sort method called for: " + repr(self) + "' pert with direction: " + str(direction))
        queue = Queue()
        self.topological_list.clear()
        self.find_node_degree()
        for node in self:
            if node.degree == 0:
                queue.insert(node)
                self.topological_list.append(node)
        while not queue.is_empty():
            node = queue.delete()
            for u in self[node]:  # for each node u in the adjacency list of u
                u[0].degree = u[0].degree - 1
                if direction == "FORWARD":
                    u[0].EE = max(u[0].EE, node.EE + u[1].duration)
                else:
                    u[0].LE = min(u[0].LE, node.LE - u[1].duration)
                if u[0].degree == 0:
                    queue.insert(u[0])
                    self.topological_list.append(u[0])
        return self.topological_list

    def reverse_graph(self, append):
        logging.info("reverse_graph method called for: " + repr(self) + "' pert with append: " + str(append))
        r = defaultdict(list)
        node1 = list(self.keys())[-1]
        for key, value in self.items():
            for node, act in value:
                if append:
                    node.LE = node1.EE
                r[node].append((key, act))
        for node in graph:
            if node not in r:
                r[node] = []
        self.__graph_dict = r

    def add_activity(self, node_from, act=None, node_to=None):
        logging.info("add_activity method called for: " + repr(self) + "' pert, Node from: " + str(
            node_from) + ", activity: " + str(activity) + ", Node to: " + str(node_to))
        if not node_to:
            self.__graph_dict[node_from] = []
        else:
            self.__graph_dict[node_from] = [[node_to, act]]

    def find_isolated(self):
        logging.info("find_isolated method called for: " + repr(self) + "' pert")
        """ returns a list of isolated vertices. """
        isolated = []
        self.find_node_degree()
        for i in self.keys():
            if i.degree == 0 and not self[i]:
                isolated.append(i)
        return isolated

    # Method for calculating the slack time
    def slack_time(self):
        logging.info("slack_time method called for: " + repr(self) + "' pert")
        slack_time = 0
        for s in self.keys():
            slack_time += (s.LE - s.EE)
        return slack_time

    def critical_path(self):
        logging.info("critical_path method called for: " + repr(self) + "' pert")
        self.tp_sort("FORWARD")
        self.reverse_graph(1)
        self.tp_sort("BACKWARD")
        self.reverse_graph(0)
        critical_path_lst = []
        for s in reversed(self.topological_list):
            if s.LE == s.EE:
                critical_path_lst.append(s)
        return critical_path_lst

    def shorten_critical_path(self):
        task_list = self.critical_path_activities()
        max_short_list = dict()

        for task in task_list:
            original_duration = task.duration
            while True:
                if task.duration == 0:
                    break
                task.duration = task.duration - 1
                temp = self.critical_path_activities()
                if task.duration <= 1:
                    max_short_list[task.name] = 1
                    task.duration = original_duration
                    break

                if task not in temp:
                    # print("duration = " + str(task.duration))
                    max_short_list[task.name] = original_duration - task.duration - 1
                    task.duration = original_duration
                    break
        return max_short_list

    def critical_path_activities(self):
        cpm = self.critical_path()
        cpm_copy = cpm[:]
        iterator = iter(cpm_copy)
        next(iterator)
        act_list = []
        cpm.pop()
        for node in cpm:
            item = next(iterator).name
            for node2 in self[node]:
                if item == node2[0].name:
                    act_list.append(node2[1])
        return act_list

    def desc_slack_time(self):
        sorted_lst = dict()
        for node in self:
            sorted_lst[node] = node.node_slack_time()
        sorted_lst = sorted(sorted_lst.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_lst


# --------------------------------------------------------------------------------------------


if __name__ == "__main__":
    a = Node("A")
    b = Node("B")
    c = Node("C")
    d = Node("D")
    e = Node("E")
    f = Node("F")
    g = Node("G")
    start = Node("Start")
    end = Node("End")

    graph = {start: [[a, Activity("Task1", 4)], [b, Activity("Task5", 6)], [c, Activity("Task9", 5)]],
             a: [[b, Activity("Task11", 0)]],
             b: [[d, Activity("Task2", 2)]],
             c: [[f, Activity("Task6", 4)]],
             d: [[e, Activity("Task8", 5)], [f, Activity("Task12", 0)], [g, Activity("Task3", 2)],
                 [end, Activity("Task10", 8)],
                 [c, Activity("Task13", 0)]],
             g: [[end, Activity("Task14", 0)]],
             f: [[end, Activity("Task7", 6)]],
             e: [[end, Activity("Task4", 5)], [f, Activity("Task15", 0)]],
             end: []}

    # Question 1: initialize graph
    graph = Pert(graph)
    cpm1 = graph.critical_path()

    # Question 4: slack time in descending order
    print("Slack time per activity: ")
    print(graph.desc_slack_time())

    # Question 5: sum of slack time
    print("\nSum of slack time is: " + str(graph.slack_time()) + "\n")

    # Question 7: iterate on the nodes with iterator
    print("Iterate over all the activities with iterator:")
    for activity in iter(graph):
        print(activity)

    # Question 8: find critical path
    print("\nCritical path:")
    for i in cpm1:
        print(str(i.name) + "->", end="")
    print("| \n")

    # Question 9: maximum shorting times
    print("Maximum shortening times:")
    print(graph.shorten_critical_path())

    # Question 3: find isolated activity
    graph.add_activity(Node("R"))
    lst_c_path = graph.find_isolated()
    print("\nThe isolated nodes are: " + str(lst_c_path) + "\n")

    # Question 2: add activity
    new_node = Node("Q")
    n_activity = Activity("Task16", 5)
    graph.add_activity(new_node)
    graph.add_activity(end, n_activity, new_node)
