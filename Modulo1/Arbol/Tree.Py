from Node import Node

class Tree:
    
    def __init__(self, root = None):
        self.root = root
        self.size = 0
        
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return self.root.__iter__()
    
    def add(self, valor):
        if self.root:
            self._add(valor, self.root)
        else:
            self.root = Node(valor)
        self.size += 1
    def _add(self, valor, node):
        if valor < node.valor:
            if node.hasLeft():
                self._add(valor, node.left)
            else:
                node.left = Node(valor, parent = node)
        else:
            if node.hasRight():
                self._add(valor, node.right)
            else:
                node.right = Node(valor, parent = node)

    def find(self, valor):
        if self.root:
            return self._find(valor, self.root)
        else:
            return None
        
    def _find(self, valor, node):
        print(node.valor)
        if not node:
            return None
        elif node.valor == valor:
            return node
        elif valor < node.valor:
            return self._find(valor, node.left)
        else:
            return self._find(valor, node.right)
        
    def print(self):
        if self.root:
            self._print(self.root)
    
    def _print(self, node):
        if node:
            self._print(node.left)
            print(node.valor)
            self._print(node.right)
