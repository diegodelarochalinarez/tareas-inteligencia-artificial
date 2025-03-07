N = 3

mover_y = [0, 0, -1, 1]
mover_x = [-1, 1, 0, 0]

class Nodo:
    def __init__(self, padre, tablero, x, y, profundidad):
        self.padre = padre
        self.tablero = tablero
        self.x = x
        self.y = y
        self.profundidad = profundidad
        self.costo = float('inf')

def imprimir_tablero(tablero):
    for renglon in tablero:
        print(' '.join(map(str, renglon)))
    print("__________________")

def calcular_costo(inicial, final):
    cont = 0
    for i in range(3):
        for j in range(3):
            if inicial[i][j] != 0 and inicial[i][j] != final[i][j]:
                cont += 1
    return cont

def comprobar_posicion(x, y):
    return 0 <= x < N and 0 <= y < N

def imprimir_ruta(raiz):
    if raiz == None:
        return
    imprimir_ruta(raiz.padre)
    print(f'Profundidad alcanzada {raiz.profundidad}')
    imprimir_tablero(raiz.tablero)
    print()
        
def resolver(inicial, x, y, final):
    pq = []
    raiz = Nodo(None, inicial, x, y, 0)
    raiz.costo = calcular_costo(inicial, final)
    pq.append(raiz)
    
    while pq:
        min_nodo = min(pq, key=lambda n: n.costo + n.profundidad)
        pq.remove(min_nodo)

        imprimir_tablero(min_nodo.tablero)
                
        if min_nodo.costo == 0:
            imprimir_ruta(min_nodo)
            return
        
        for i in range(4):
            nueva_x, nueva_y = min_nodo.x + mover_x[i], min_nodo.y + mover_y[i]
            if comprobar_posicion(nueva_x, nueva_y):
                
                nuevo_tab = [renglon[:] for renglon in min_nodo.tablero]
                nuevo_tab[min_nodo.x][min_nodo.y], nuevo_tab[nueva_x][nueva_y] = nuevo_tab[nueva_x][nueva_y], nuevo_tab[min_nodo.x][min_nodo.y]
                
                if min_nodo.padre is not None and nuevo_tab == min_nodo.padre.tablero:
                    continue
                
                hijo = Nodo(min_nodo, nuevo_tab, nueva_x, nueva_y, min_nodo.profundidad + 1)
                hijo.costo = calcular_costo(hijo.tablero, final)
                pq.append(hijo)
        max_nodo = max(pq, key=lambda n: n.costo + n.profundidad)
        pq.remove(max_nodo)

if __name__ == '__main__':
    
    tablero = [[1,0,3],[4,8,7],[2,6,5]]
    solucion = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    x, y = 1, 0

    resolver(tablero, x, y, solucion)
        
    