import os
import math
from HashFunction import *
import copy
proof_to_user=[]
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
        # data = str(data)
        #data2=bytes(data,"utf-8")
        #return h
        # m = hashlib.md5()
        # m.update(data.encode('utf-8'))
        # return m.hexdigest()
        data = str(data)
        
        #m = hashlib.md5()
        if os.path.isfile(data):
            try:   
                f = open(data, 'rb')
            except:
                return 'ERROR: unable to open %s' % data
            temp1 = ''
            while True:
                d = f.read(8096)
                if not d:
                    break
                #d=str(d)
             #   print(d)
                temp=hash_fun_hex_str(hash_fun(d))
                temp1=hash_update(temp1,temp)
            f.close()
        # Otherwise it could be either 1) a directory 2) miscellaneous data (like json)
        else:
            data2=bytes(data,"utf-8")
            temp1=hash_fun_hex_str(hash_fun(data2))
        return temp1

    def _audit(self, questioned_hash, proof_hashes):
        """ Tests if questioned_hash is a member of the merkle tree by
            hashing it with its test until the root hash is reached. 
        """
        proof_hash = proof_hashes.pop()
	#	print(proof_hash) #Arpit the weirdo wated it      

        if not proof_hash in self.node_table.keys():#This fnxn is of no usefor the time being
            return False    #""

        test = self.node_table[proof_hash]
        parent = test.parent

        # Because the order in which the hashes are concatenated matters,
        # we must test to see if questioned_hash is the "mother" or "father"
        # of its child (the hash is always build as mother + father).
        if parent.left.hash == questioned_hash:
            actual_hash = self._md5sum(questioned_hash + test.hash)
            temp_str=questioned_hash+'   +   '+test.hash+'   =   '+actual_hash
            proof_to_user.append('2')
            proof_to_user.append(test.hash)
        elif parent.right.hash == questioned_hash:
            actual_hash = self._md5sum(test.hash + questioned_hash)
            temp_str=test.hash+'   +   '+questioned_hash+'   =   '+actual_hash
            proof_to_user.append('1')
            proof_to_user.append(test.hash)

        else:   #never executes
            return False    #""

        if actual_hash != parent.hash:  #never exexutes
            return False        #""
        if actual_hash == self.root_hash:
            return True

        return self._audit(actual_hash, proof_hashes)    #have to tackle the corner case of proof_hashes being empty and root has not matching

    def _handle_solo_node_case(self):
        # The earlier method for building the tree will fail in a one node case
        if len(self.leaves) == 1:
            solo_node = self.leaves.pop()
            self.root_hash = solo_node.hash
            self.node_table[solo_node.hash] = solo_node

    def _get_leaf_hashes(self):
        return [node.hash for node in self.node_table.values() if node.left == None]

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

    def audit(self, data, proof_hashes):
        """ Returns a boolean testing if a data (a file or object)
            is contained in the merkle tree. 
            proof_hashes are the nodes to hash the hash of data with 
            in order from the bottom of the tree to the second-to-last
            level. len(proof_hashes) is expected to be the height of the
            tree, ceil(log2(n)), as one node is needed for proof per layer.
            If the tree has not been built, returns False for any data.
        """
        if proof_hashes:
            if self.root_hash == None:
                return False

            hash_ = self._md5sum(data)

            # A one element tree does not make much sense, but if one exists
            # we simply need to check if the files hash is the correct root
            if self.max_height == 0 and hash_ == self.root_hash:
                return True
            if self.max_height == 0 and hash_ != self.root_hash:
                return False
            print('Proof Hashes', proof_hashes)
            proof_hashes_cp = copy.copy(proof_hashes)
            return self._audit(hash_, proof_hashes_cp)

        else:
            return False
    
    def get_branch(self, item):
        """ Returns an authentication path for an item (not hashed) in 
            the Merkle tree as a list in order from the top of the tree
            to the bottom.
        """
    
        hash_ = self._md5sum(item)

        if not hash_ in self._get_leaf_hashes():
            print("The requested item is not in the merkle tree.")
            return

        return self._get_branch_by_hash(hash_)

    def proof(self,root_h,l):
        m1=MerkleTree(l)
        if m1.root_hash == root_h:
            print("The files are authentic")
        else:
            print('Delete the files immediately, those are corrupted')

'''a=MerkleTree(['try.txt','try1.txt'])
print("root",a.root_hash)
p=a.node_table[a.root_hash].right
print("try",p.hash)
print(a.audit('try1.txt',a.get_branch('try1.txt')))
print(a.audit(17,a.get_branch(17)))
a.proof(a.root_hash,['try.txt','try2.txt'])
'''
a=MerkleTree(['testing_update.txt'])
print(a.root_hash)
# print(a.audit('try1.txt',a.get_branch('try1.txt')))
# f = open("proof_to_user1.txt","w")
# for i in range(len(proof_to_user)):
#     f.write(str(proof_to_user[i]+'\n')) 
# f.close()
