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

branchHash = {}
branches = os.listdir(top_level + '/.git/refs/heads/')
for b in sorted(branches):
    hash = open(top_level + '/.git/refs/heads/' + b, 'r').read().strip('\n')
    if hash not in branchHash: 
        temp = set()
    else:
        temp = branchHash[hash]
    temp.add(b)
    branchHash[hash] = temp

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
        for line in sorted(contents):
            if(line[:6] == 'parent'):
                parent_hash = line[7:]
                parent_hashes.append(parent_hash)
    return parent_hashes

object_dir = top_level + '/.git/objects/'
prefixes = os.listdir(object_dir)
# print(prefixes)
commits = []
nodes = {}

for prefix in sorted (prefixes):
    folders = os.listdir(object_dir + prefix + '/')
    for hash in sorted (folders):
        file_name = object_dir + prefix + '/' + hash
        contents = zlib.decompress(open(file_name, 'rb').read())
        if (contents[:6] == b'commit'):
            hash = prefix + hash
            stack = [hash]
            while(len(stack) != 0):
                curr = stack.pop()
                if curr not in nodes:
                    curr_node = CommitNode(curr)
                else:
                    curr_node = nodes[curr]
                parents = getParentsOf(curr)
                for parent in sorted(parents):
                    curr_node.parents.add(parent)
                    if parent not in nodes:
                        stack.append(parent)
                        parent_node = CommitNode(parent)
                    else:
                        parent_node = nodes[parent]

                    parent_node.children.add(curr)
                    nodes[parent] = parent_node
                nodes[curr] = curr_node

def printGraph(nodes):
    nodes
    for hash in sorted (nodes.keys()):
        node = nodes[hash]
        print('node - ' + node.commit_hash)
        for children in sorted (node.children):
            print('child - ', end='')
            print(children)
        for parent in sorted (node.parents):
            print('parent - ', end='')
            print(parent)
        print()

printGraph(nodes)

## NUMBER 4 ##

from collections import deque

def DFS_topo(nodes):
    order = []
    sources = []
    visited = set()
    for hash in sorted (nodes):
        if len(nodes[hash].parents) == 0:
            sources.append(hash)
    for s in sorted (sources):
        #DFS
        stack = [s]
        while len(stack)!=0:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                order.append(curr)
                children = nodes[curr].children
                for c in sorted (children):
                    stack.append(c)
    return order 

order = DFS_topo(nodes)


## NUMBER 5 ##

order = order[::-1]

i = 0
while i < len(order):
    print(order[i], end='')
    if order[i] in branchHash:
        for b in sorted (branchHash[order[i]]):
            print(' ' + b, end='')
    print()
    if (i < len(order)-1 and order[i+1] not in nodes[order[i]].parents):
        for n in nodes[order[i]].parents:
            print(n + '=')
            print()
    i += 1
