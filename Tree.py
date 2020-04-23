import numpy as np
from numpy.random import uniform
import graphviz as gv


class TreeNode(object):
    def __init__(self, val=None, id=None, left=None, right=None, minimum=None, maximum=None, depth=1):
        self.val = val
        self.id = id
        self.left = left
        self.right = right
        self.minimum = minimum
        self.maximum = maximum
        self.depth = depth
        
    def __repr__(self):
        return f"TreeNode(val={self.val}, id={self.id})"
        

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
        self._next_node_id = 0
        self.root = self._gen()
        
    @property
    def next_node_id(self):
        self._next_node_id += 1
        return self._next_node_id
        
    def _gen(self):
        if self.max_depth < self.min_depth:
            self.min_depth = self.max_depth
            
        root = TreeNode(
            val=int(uniform(self.tree_minimum_value, self.tree_maximum_value)),
            id=self.next_node_id
        )
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
                id=self.next_node_id,
                minimum=node.val, 
                maximum=node.maximum, 
                depth=node.depth + 1
            )
            
        if self._sparsity_test():
            node.left = TreeNode(
                val=self._gen_node_val(node, 'left'), 
                id=self.next_node_id,
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


def plot_tree(root, graph_attrs=None):
    def helper(graph, node):
        if not (node.left or node.right):
            return graph
        
        if node.left:
            graph.node(f'{node.left.id}', label=f'val: {node.left.val}\nnode_id: {node.left.id}')
            graph.edge(f'{node.id}', f'{node.left.id}')
            graph = helper(graph, node.left)
            
        if node.right:
            graph.node(f'{node.right.id}', label=f'val: {node.right.val}\nnode_id: {node.right.id}')
            graph.edge(f'{node.id}', f'{node.right.id}')
            graph = helper(graph, node.right)
            
        return graph
    
    graph_attrs = graph_attrs or {}
    graph = graphviz.Digraph()
    graph.node(f'{root.id}', label=f'val: {root.val}\nnode_id: {root.id}')
    graph = helper(graph, root)
    graph.attr(**graph_attrs)
    return graph


def lca(root, n1_id, n2_id):
    def helper(node):
        if not node:
            return False
        
        if node.id == n1_id or node.id == n2_id:
            return True
        
        return helper(node.left) or helper(node.right)
        
    if helper(root.right) and helper(root.left):
        return root

    if helper(root.right):
        return lca(root.right, n1_id, n2_id)
    
    return lca(root.left, n1_id, n2_id)