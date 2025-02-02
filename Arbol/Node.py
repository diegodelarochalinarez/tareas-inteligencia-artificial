class Node:
    
    def __init__(self, value, right = None, left = None, parent = None ):
        self.valor= value
        self.right = right
        self.left = left
        self.parent = parent
    
    def hasRight(self):
        return self.right
    
    def hasLeft(self):
        return self.left
    
    def isRoot(self):
        return not self.parent
    
    def isLeftSon(self):
        return self.parent and self.parent.left == self
    
    def isRightSon(self):
        return self.parent and self.parent.right == self
    
    def isLeaf(self):
        return not (self.right or self.left)
    
    def hasChild(self):
        return self.right or self.left
    
    def hasBothChildren(self):
        return self.right and self.left