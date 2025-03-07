from Tree import Tree


arbol = Tree()
arbol.add(5)
arbol.add(3)
arbol.add(8)
arbol.add(2)
arbol.add(4)
arbol.add(6)

arbol.inorder()

print(arbol.search(3))
print(arbol.search(10))