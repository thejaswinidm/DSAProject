import os
import math
import hashlib
import copy

class MerkleTree:
    class Node:
        def __init__(self, left, right, hash_val):
            self.left = left
            self.right = right
            if left == None:
                self._height = 0
            else:
                self._height = left.height + 1

            self.hash = hash_val
            self.parent = None
    
        @property
        def height(self):
            return self._height
    
        @height.setter
        def height(self,height):
            
            self._height = height

        def get_sibling(self, sibling_hash):
            if sibling_hash == self.left.hash:
                return self.right
            return self.left

    def __init__(self, items):
        
        self.is_built = False
        self.root_hash = None
        self.node_table = {}
        self.max_height = math.ceil(math.log(len(items), 2))
        self.leaves = list(map(self._leafify, map(self._md5sum, items)))

        if items and len(items) > 0:
            self.build_tree()

    def _leafify(self, data):
        leaf = self.Node(None, None, data)
        leaf.height = 0
        return leaf

    def _get_branch_by_hash(self, hash_):
        """ Returns an authentication path as a list in order from the top
            to the bottom of the tree (assumes preconditions have been checked).
        """
        path = []
        while hash_ != self.root_hash:
            node = self.node_table[hash_]
            parent = node.parent
            sibling = parent.get_sibling(hash_)
            path.append(sibling.hash)
            hash_ = parent.hash

        path.append(hash_)
        path.reverse()
        return path
    
    def _md5sum(self, data):
        """ Returns an md5 hash of data. 
            If data is a file it is expected to contain its full path.
        """
        data = str(data)
        m = hashlib.md5()
        m.update(data.encode('utf-8'))
        return m.hexdigest()

    

    def _handle_solo_node_case(self,):
        # The earlier method for building the tree will fail in a one node case
        if len(self.leaves) == 1:
            solo_node = self.leaves.pop()
            self.root_hash = solo_node.hash
            self.node_table[solo_node.hash] = solo_node

    def _get_leaf_hashes(self):
        return [node.hash for node in self.node_table.values() if node.mom == None]

    # TODO break into sub methods?
    def build_tree(self):
        """ Builds a merkle tree by adding leaves one at a time to a stack,
            and combining leaves in the stack when they are of the same height.
            Expected items to be an array of type Node.
            Also constructs node_table, a dict containing hashes that map to 
            individual nodes for auditing purposes.
        """
        stack = []
        self._handle_solo_node_case()
        while self.root_hash == None:
            if len(stack) >= 2 and stack[-1].height == stack[-2].height:
                left = stack.pop()
                right = stack.pop()
                parent_hash = self._md5sum(left.hash + right.hash)
                parent = self.Node(left, right, parent_hash)
                self.node_table[parent_hash] = parent
                left.parent = parent
                right.parent = parent

                if parent.height == self.max_height:
                    self.root_hash = parent.hash

                stack.append(parent)
            elif len(self.leaves) > 0:
                leaf = self.leaves.pop()
                self.node_table[leaf.hash] = leaf
                stack.append(leaf)
            # Handle case where last 2 nodes do not match in height by "graduating"
            # last node
            else:
                stack[-1].height += 1
        self.is_built = True

    
    
    def get_branch(self, item):
        """ Returns an authentication path for an item (not hashed) in 
            the Merkle tree as a list in order from the top of the tree
            to the bottom.
        """
        

        hash_ = self._md5sum(item)

        
        return self._get_branch_by_hash(hash_)




a=MerkleTree([2,3,4,5])
print(a.root_hash)
p=a.node_table[a.root_hash].right.right
print(p.hash)



















