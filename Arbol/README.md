# Árbol de búsqueda binaria

En esta tarea implementamos una estructura tipo arbol que consta de un nodo raíz, que puede tener como máximo 2 nodos hijos y un nodo padre (exceptuando el nodo raíz). La característica principal de esta estructura es que mantiene el orden poniendo los nodos con valor menor a la izquierda y los nodos con valor mayor a la derecha.

Implementamos los cuatro métodos especificados: <br/>
1.- El constructor es el método que inicializa el árbol.
2.- El método add() si el árbol ya tiene raíz llama al metodo recursivo \_add() que busca colocar el valor en una nueva hoja del árbol recorriendo el sub árbol derecho si es que el valor a insertar es mayor al nodo actual o el sub árbol izquierdo en caso contrario.
3.- El método find() llama a su vez al método recursivo \_find() que sigue a su vez sigue la misma lógica que la inserción.
4.- Para imprimir el árbol lo hacemos siguiendo el recorrido en órden primero por el sub árbol izquierdo, luego el nodo actual y posterior el sub árbol derecho.

El método de añadir y buscar logran una complejidad en tiempo de O(log n) al mantener en todo momento el orden en la búsqueda.
