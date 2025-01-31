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
    
    def inorder(self):
        if self.root:
            self._inorder(self.root)
    
    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(node.valor)
            self._inorder(node.right)
    
    def search(self, valor):
        if self.root:
            return self._search(valor, self.root)
        else:
            return False
    
    def _search(self, valor, node):
        if valor == node.valor:
            return True
        elif valor < node.valor and node.hasLeft():
            return self._search(valor, node.left)
        elif valor > node.valor and node.hasRight():
            return self._search(valor, node.right)
        else:
            return False