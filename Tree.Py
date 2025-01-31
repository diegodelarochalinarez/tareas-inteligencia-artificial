from xml.dom import Node


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