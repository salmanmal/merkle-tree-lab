import hashlib
from dataclasses import dataclass

class Node(object):
    def __init__(self, val=None, left=None, right=None):
        # Hash value of the node via hashlib.sha256(xxxxxx.encode()).hexdigest()
        self.val = val
        # Left node
        self.left = left
        # Right node
        self.right = right

    def __str__(self):
        return f':val={self.val},left={self.left},right={self.right}:'


class MerkleTrees(object):
    def __init__(self):
        self.root = None
        # txns dict: { hash_val -> 'file_path' } 
        self.txns = None
        
    def get_root_hash(self):
        return self.root.val if self.root else None

    def build(self, txns):
        """
        Construct a Merkle tree using the ordered txns from a given txns dictionary.
        """
        # save the original txns(files) dict while building a Merkle tree.
        self.txns = txns
        txns_list = list(txns.keys())
        if len(txns_list)%2 != 0:
            txns_list.append(txns_list[-1])
        intermediate_nodes=[]
        for index in range(0, len(txns_list)-1, 2):
            left = txns_list[index]
            right = txns_list[index+1]
            combine = left + right
            root = hashlib.sha256(combine.encode()).hexdigest()
            current_node = Node(root, Node(left), Node(right))
            intermediate_nodes.append(current_node)
        left=intermediate_nodes[0]
        right=intermediate_nodes[1]
        combine=left.val+right.val
        root=hashlib.sha256(combine.encode()).hexdigest()
        self.root = Node(root, left=left, right=right)


    def print_level_order(self):
        """
          1             1
         / \     -> --------------------    
        2   3       2 3
        """
        next_to_visit=[self.root]
        while len(next_to_visit)>0:
            node_to_visit=next_to_visit
            next_to_visit=[]
            row=""
            for curr_node in node_to_visit:
                row+=curr_node.val
                row+=" "
                if curr_node.left!=None:
                    next_to_visit.append(curr_node.left)
                if curr_node.right!=None:
                    next_to_visit.append(curr_node.right)
            print(row)
            print("--------------------")
        
        

    @staticmethod
    def compare(x, y):
        """
        Compare a given two merkle trees x and y.
        x: A Merkle Tree
        y: A Merkle Tree
        Pre-conditions: You can assume that number of nodes and heights of the given trees are equal.
        
        Return: A list of pairs as Python tuple type(xxxxx, yyyy) that hashes are not match.
        https://realpython.com/python-lists-tuples/#python-tuples
        """
        diff = []
        if x.get_root_hash() == y.get_root_hash():
            return diff
        
        nodes_x=[x.root]
        nodes_y=[y.root]

        while len(nodes_x)>0 and len(nodes_y)>0:
            iter_x=nodes_x
            iter_y=nodes_y

            nodes_x=[]
            nodes_y=[]
            for i in range(len(iter_x)):
                if iter_x[i].val!=iter_y[i].val:
                    diff.append((iter_x[i].val,iter_y[i].val))
                    if iter_x[i].left!=None:
                        nodes_x.append(iter_x[i].left)
                    if iter_x[i].right!=None:
                        nodes_x.append(iter_x[i].right)
                    if iter_y[i].left!=None:
                        nodes_y.append(iter_y[i].left)
                    if iter_y[i].right!=None:
                        nodes_y.append(iter_y[i].right)
        
        
        return diff
