
solucion = [[1,2,3],[4,5,6],[7,8,0]]

N =3

mover_y = [0,0,-1,1]
mover_x = [-1,1,0,0]

class Estado:
    def __init__(self, tablero, x, y,profundidad):
        self.tablero = tablero
        self.x = x
        self.y = y
        self.profundidad = profundidad

def comprobar_resultado(tablero):
    return tablero == solucion
        
def comprobar_posicion_hueco(x, y):
    return 0<= x < N and 0<= y < N

def imprimir_tablero(tablero):
    for renglon in tablero:
        print(' '.join(map(str,renglon)))
    print("____________")
        
def solucionar_puzzle(inicio, x, y):
    lista = []
    visitados = set()
    lista.append(Estado(inicio,x,y, 0))
    visitados.add(tuple(map(tuple, inicio)))
    
    while lista:
        actual = lista.pop()
        print(f'Profundidad: {actual.profundidad}')
        imprimir_tablero(actual.tablero)
        
        if(comprobar_resultado(actual.tablero)):
            print(f'Estado encontrado en la profundidad {actual.profundidad}')
            return
        
        for i in range(4):
            nueva_x = actual.x + mover_x[i]
            nueva_y = actual.y +mover_y[i]
            
            if (comprobar_posicion_hueco(nueva_x,nueva_y)):
                nuevo_tablero = [renglon[:] for renglon in actual.tablero]
                
                nuevo_tablero[actual.x][actual.y], nuevo_tablero[nueva_x][nueva_y]=nuevo_tablero[nueva_x][nueva_y], nuevo_tablero[actual.x][actual.y]
                tupla_tablero = tuple(map(tuple, nuevo_tablero))
                if(tupla_tablero not in visitados):
                    visitados.add(tupla_tablero)
                    lista.append(Estado(nuevo_tablero, nueva_x, nueva_y, actual.profundidad + 1))
    print("No se encontró solución")       

if __name__ == '__main__':
    tablero = [[8,4,3],[2,0,1],[6,5,7]]
    x,y =1,1
    
    solucionar_puzzle(tablero, x, y)