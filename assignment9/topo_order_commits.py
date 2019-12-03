#!/usr/bin/python3

# Prithvi Kannan
# UID: 405110096
from collections import defaultdict
import os
import zlib

## NUMBER 1 ##


def find_root(test, dirs=(".git",), default=None):
    import os
    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.isdir(os.path.join(test, d)) for d in dirs):
            return test
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return default


top_level = find_root(os.getcwd())
# print('Top Level: ' + top_level)


## NUMBER 2 ##

# find .git/refs/heads/ -type f

# to get branches, go to /.git/refs/heads/
# each file name is the name of the branch
# the contents of the file contain the hash

branches = os.listdir(top_level + '/.git/refs/heads/')
# print(branches)


## NUMBER 3 ##

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

    def __str__(self):
        return 'Commit Hash: ' + self.commit_hash

def getParentsOf(hash):
    parent_hashes = []
    path = object_dir + hash[:2] + '/' + hash[2:]
    contents = zlib.decompress(open(path, 'rb').read())
    if (contents[:6] == b'commit'):
        contents = contents.decode().split('\n')
        for line in contents:
            if(line[:6] == 'parent'):
                parent_hash = line[7:]
                parent_hashes.append(parent_hash)
    return parent_hashes

# find .git/objects -type f


object_dir = top_level + '/.git/objects/'
prefixes = os.listdir(object_dir)
# print(prefixes)
commits = []
nodes = {}

for prefix in prefixes:
    folders = os.listdir(object_dir + prefix + '/')
    for hash in folders:
        file_name = object_dir + prefix + '/' + hash
        contents = zlib.decompress(open(file_name, 'rb').read())
        if (contents[:6] == b'commit'):
            hash = prefix + hash
            # print('hash ' + hash, end='')
            # print(getParentsOf(hash))
            stack = [hash]
            while(len(stack) != 0):
                curr = stack.pop()
                if curr not in nodes:
                    curr_node = CommitNode(curr)
                else:
                    curr_node = nodes[curr]
                parents = getParentsOf(curr)
                for parent in parents:
                    curr_node.parents.add(parent)
                    if parent not in nodes:
                        stack.append(parent)
                        parent_node = CommitNode(parent)
                    else:
                        parent_node = nodes[parent]

                    parent_node.children.add(curr)
                    nodes[parent] = parent_node
                nodes[curr] = curr_node

for hash in nodes:
    node = nodes[hash]
    print('node - ' + node.commit_hash)
    for children in node.children:
        print('child - ', end='')
        print(children)
    for parent in node.parents:
        print('parent - ', end='')
        print(parent)
    print()


## NUMBER 4 ##

# A Python program to print topological sorting of a graph
# using indegrees

# Class to represent a graph


class Graph:
    def __init__(self, vertices):
        # self.graph = defaultdict(CommitNode)  # dictionary containing adjacency List
        self.graph = defaultdict(list)  # dictionary containing adjacency List
        self.V = vertices  # No. of vertices

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # The function to do Topological Sort.

    def topologicalSort(self):

        # Create a vector to store indegrees of all
        # vertices. Initialize all indegrees as 0.
        in_degree = [0]*(self.V)

        # Traverse adjacency lists to fill indegrees of
        # vertices. This step takes O(V+E) time
        for i in self.graph:
            for j in self.graph[i]:
                in_degree[j] += 1
        # for i in self.graph:
        #     for j in self.graph[i]:
        #         in_degree[j] += 1

        # Create an queue and enqueue all vertices with
        # indegree 0
        queue = []
        for i in range(self.V):
            if in_degree[i] == 0:
                queue.append(i)

        # Initialize count of visited vertices
        cnt = 0

        # Create a vector to store result (A topological
        # ordering of the vertices)
        top_order = []

        # One by one dequeue vertices from queue and enqueue
        # adjacents if indegree of adjacent becomes 0
        while queue:

            # Extract front of queue (or perform dequeue)
            # and add it to topological order
            u = queue.pop(0)
            top_order.append(u)

            # Iterate through all neighbouring nodes
            # of dequeued node u and decrease their in-degree
            # by 1
            for i in self.graph[u]:
                in_degree[i] -= 1
                # If in-degree becomes zero, add it to queue
                if in_degree[i] == 0:
                    queue.append(i)

            cnt += 1

        # Check if there was a cycle
        if cnt != self.V:
            print ("There exists a cycle in the graph")
        else:
            # Print topological order
            print (top_order)


g = Graph(6)
g.addEdge(5, 2)
g.addEdge(5, 0)
g.addEdge(4, 0)
g.addEdge(4, 1)
g.addEdge(2, 3)
g.addEdge(3, 1)

# g.topologicalSort()

