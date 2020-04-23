import numpy as np
from numpy.random import uniform
import graphviz as gv


class TreeNode(object):
    def __init__(self, val=None, left=None, right=None, minimum=None, maximum=None, depth=1):
        self.val = val
        self.left = left
        self.right = right
        self.minimum = minimum
        self.maximum = maximum
        self.depth = depth
        

class Tree(object):
    def __init__(
        self, 
        sparsity=0, 
        max_depth=5, 
        min_depth=5, 
        tree_minimum_value=0,
        tree_maximum_value=1000,
        balanced=False
    ):
        self.sparsity = sparsity
        self.max_depth = max_depth
        self.min_depth = min_depth
        self.tree_minimum_value = tree_minimum_value
        self.tree_maximum_value = tree_maximum_value
        self.balanced = balanced
        self.min = False
        self.root = self._gen()
        
    def _gen(self):
        if self.max_depth < self.min_depth:
            self.min_depth = self.max_depth
            
        root = TreeNode(int(uniform(self.tree_minimum_value, self.tree_maximum_value)))
        stack = [root]
        while stack:
            node = stack.pop()
            node = self._gen_node_children(node)
                
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
                
            # if no children, but min_depth not met, force recalculate 
            if (
                not (node.left or node.right) 
                and node.depth < self.min_depth 
                and not self.min
            ):
                stack.append(node)
                continue 
    
        return root   
    
    def _gen_node_children(self, node):
        # Flag if the min_depth has been reached
        if not self.min and node.depth >= self.min_depth:
            self.min = True
            
        if node.depth >= self.max_depth:
            return node
        
        if self._sparsity_test():      
            node.right = TreeNode(
                val=self._gen_node_val(node, 'right'), 
                minimum=node.val, 
                maximum=node.maximum, 
                depth=node.depth + 1
            )
            
        if self._sparsity_test():
            node.left = TreeNode(
                val=self._gen_node_val(node, 'left'), 
                maximum=node.val, 
                minimum=node.minimum, 
                depth=node.depth + 1
            )
            
        return node
        
    def _gen_node_val(self, node, side):
        if self.balanced:
            if side == 'right':
                return int(uniform(node.val, node.maximum or self.tree_maximum_value))
            return int(uniform(node.minimum or self.tree_minimum_value, node.val))
        
        return int(uniform(self.tree_minimum_value, self.tree_maximum_value))
        
    def _sparsity_test(self):
        return uniform() >= self.sparsity


def plot_tree(root):
    def helper(graph, node, root_id):
        if not (node.left or node.right):
            return graph, root_id
        
        id = root_id
        if node.left:
            d.node(f'{id + 1}', label=f'{node.left.val}')
            d.edge(f'{root_id}', f'{id + 1}')
            graph, id = helper(graph, node.left, id + 1)
            
        if node.right:
            d.node(f'{id + 1}', label=f'{node.right.val}')
            d.edge(f'{root_id}', f'{id + 1}')
            graph, id = helper(graph, node.right, id + 1)
            
        return graph, id
    
    d = graphviz.Digraph()
    root_id = 0
    d.node(f'{root_id}', label=f'{root.val}')
    graph, _ = helper(d, root, root_id)
    return graph