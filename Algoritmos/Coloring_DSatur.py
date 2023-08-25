import networkx as nx
import time
'''
Coloring By DSatur

Dado G=(V,E) un grafo tal que V = (N1, N2, ... Nx) un conjunto de nodos y
E
'''

def Grado_saturacion(G, V):          #Función que extrae los colores de los vecinos del nodo
    ClrAdj=[]
    for Adj in G.neighbors(V):
        if G.nodes[Adj]['color'] != None:
            ClrAdj.append(G.nodes[Adj]['color'])
    Dg = list(set(ClrAdj))
    Dg_satur = len(Dg)
    return Dg_satur
    

def colores_vecinos(G, V):          #Función que extrae los colores de los vecinos del nodo
    ColorAdj=[]
    for Adj in G.neighbors(V):
        ColorAdj.append(G.nodes[Adj]['color'])
    return ColorAdj                 #Retorna la lista de los colores adyacentes


def min_disponible(disp, usados):   #Función compara la lista de colores adyacentes al nodo y los colores disponibles

    Clibres = set(disp) - set(usados)
    x = min(Clibres)
    return x                        #Retorna el mínimo color disponible


def Actualiza_GS(G):                    #Función que asigna el color a cada nodo del grafo

    for nodo in G.nodes():
        G.nodes[nodo]['DSatur'] = Grado_saturacion(G, nodo)
        #print ("GS", Grado_saturacion(G, nodo))


def DSatur(G):

    Satur={}
    Grado={}
    Actualiza_GS(G)
    
    for nodo in G.nodes(): 
        if G.nodes[nodo]['color'] == None:
            Satur [nodo] = G.nodes[nodo]['DSatur']
            
    SMayor = [key for key, value in Satur.items() if value == max(Satur.values())] 
    
    if len(SMayor) == 1:
        X= SMayor[0]
    else:
        for a in SMayor:
            Grado [a] = G.degree(a)            
        GMayor = [key for key, value in Grado.items() if value == max(Grado.values())]
        
        if len(GMayor) == 1:
            X = GMayor[0]
        else:
            X = sorted(GMayor)[0]

    return X


def coloring(X):
    Co = range(0, 50)
    Actualiza_GS(G)    
    color = min_disponible(Co, colores_vecinos(G, X))
    G.nodes[X]['color'] = color
    

def verifica(nodo):             #Funcion que verifica el coloreado del grafo
     
    for Adj in G.neighbors(nodo):
        if G.nodes[nodo]['color'] == G.nodes[Adj]['color']:
            return True
        else:
            return False
    
def colorUsado(G):
    ColorUsado=[]
    for nodo in G.nodes():
        ColorUsado.append(G.nodes[nodo]['color'])
    x = max(ColorUsado)
    return x

if __name__ == "__main__":
    start_time = time.time()

#Creación del grafo inicial
    
    #G = nx.fast_gnp_random_graph(n= 100, p=0.30, seed=None, directed=False)
    #G=nx.Graph()
    G=nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edges_from([(0, 1), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7), (5, 6), (6, 7)])


    #G=nx.read_gml("BC_Planars/obg 14.gml", destringizer=int)


#Creación de la propiedad "Color " a cada nodo
    
    for i in range(len(G.nodes)):
        G.nodes[i]['color'] = None
        G.nodes[i]['DSatur'] = None    
    
    
#Coloreado y verificación del coloreado
    
    coloreados=[]
    while len(coloreados)!= len(G.nodes()):
        coloreados.append(DSatur(G))

        coloring(DSatur(G))


    #Resultados del coloreado
    print("\n", "====== C O L O R E A D O ======","\n")
    for i in G.nodes:
        print("Nodo: ", i, "  color: ", G.nodes[i]['color']+1)
        
    print("El Numero de colores usados es:", colorUsado(G)+1)

    print("\n","--- %s s ---" % (time.time() - start_time),"\n")


#Verificación  
    error = 0 
    for nodo in G.nodes():
        if verifica(nodo) == True:
            print ("\n", "Incidencia en el coloreado", "\n")
            error +1
    if error == 0:
        print ("\n", "Coloreado correcto sin errores", "\n")