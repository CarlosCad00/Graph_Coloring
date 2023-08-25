import networkx as nx
import matplotlib.pyplot as plt
import time


def Diferent_Colored(V):          #Función que extrae los colores de los vecinos del nodo
    ClrAdj=[]
    for Adj in G.neighbors(V):
        if G.nodes[Adj]['color'] < 0:
            ClrAdj.append(G.nodes[Adj]['color'])
    Dg = set(ClrAdj)
    return Dg                 ###Devolver un entero


def Colored(i):             #Numero de vertices coloreados
    No_color =[]
    for nodo in G.neighbors(i):
        if G.nodes[nodo]['color'] < 0:
            No_color.append(nodo)
    return No_color            ###Devolver entero


def Uncolored(i):           #Numero de vertices NO coloreados 
    No_color =[]
    for nodo in G.neighbors(i):
        if G.nodes[nodo]['color'] == 0:
            No_color.append(nodo)
    return No_color            ###Devolver entero


def Pot_Diff(i):
    P_diff = len(Diferent_Colored(i))+ len(Uncolored(i))
    
    return P_diff


def AC_Pot_Diff_(Node):         #Recalcula Pot_Diff en los vecinos de un nodo
    
    for i in G.neighbors(Node) :
        G.nodes[i]['P_D'] = Pot_Diff(i)


def CC_dependent(i):

    if Pot_Diff(i)< Max_Color:
        CC=True
    else: 
        CC= False

    return CC


def P_D_Mayor():                 #Selecciona el nodo con el valor más alto de Pot_Dif(i) para colorear

    Potencial = {} 
    Grado = {}

    #for i in G.nodes() :
    #   G.nodes[i]['P_D'] = Pot_Diff(i)

    for nodo in G.nodes(): 
        if G.nodes[nodo]['color'] == 0 & G.nodes[nodo]['CC_D'] == False:            
            Potencial [nodo] = G.nodes[nodo]['P_D']
            
    SMayor = [key for key, value in Potencial.items() if value == max(Potencial.values())]
    #print(SMayor)
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


def min_disponible(disp, usados):   #Extrae el mínimo color disponible

    Clibres = set(disp) - set(usados)
    x = min(Clibres)
    return x


def colores_vecinos(V):          #Función que extrae los colores de los vecinos del nodo
    ColorAdj=[]
    for Adj in G.neighbors(V):
        ColorAdj.append(G.nodes[Adj]['color'])
    return ColorAdj                 #Retorna la lista de los colores adyacentes



def Coloreado():
    
    Co= range (1, Max_Color+1)

    for i in G.nodes():
        G.nodes[i]['P_D'] = Pot_Diff(i)         #Calcula Pot_Dif para  toos los nodos

    while any(G.nodes[i]['color'] == 0 for i in G.nodes()):          #>>>>REVISAR
        
        for i in G.nodes():
            G.nodes[i]['CC_D'] = CC_dependent(i)            #Calcula CC_Dependant par tos los nodos            
            print("CC_D", i, G.nodes[i]['CC_D'])
        color = min_disponible(Co, colores_vecinos(P_D_Mayor()))            #Selecciona el mínimo color disponible
        
        
        G.nodes[P_D_Mayor()]['color'] = color             #Colorea el nodo con mayor P_D con el menor color disponible
        
        AC_Pot_Diff_(P_D_Mayor())         #Actualia Pot_Dif para los vecinos de j que no estén en cc dependant

        for i in G.nodes():
            G.nodes[i]['CC_D'] = CC_dependent(i)            #Actualiza el CC_D a todos los nodos


        CC_no_color = 0
        for i in G.nodes:
            if G.nodes[i]['CC_D'] == False & G.nodes[i]['color'] == 0:
                CC_no_color + 1
            if CC_no_color > 0:
                return
            else:
                for nodo in G.nodes():
                    if G.nodes[i]['CC_D'] == True & G.nodes[nodo]['color'] == 0:
                        color = min_disponible(Co, colores_vecinos(nodo))
                        G.nodes[nodo]['color'] = color
        
        
def verifica(nodo):             #Funcion que verifica el coloreado del grafo
     
    for Adj in G.neighbors(nodo):
        if G.nodes[nodo]['color'] == G.nodes[Adj]['color']:
            return True
        else:
            return False


def colorUsado():               #Funcion que calcula el número de colores usados
        ColorUsado=[]
        for nodo in G.nodes():
            ColorUsado.append(G.nodes[nodo]['color'])
        x = max(ColorUsado)
        return x


if __name__ == "__main__":

    start_time = time.time()

#Grafo inicial
    G=nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 5), (3, 4), (5, 4), (1, 2), (2, 3)])

    #G = nx.read_gml("PlaneGraphs/80Nodes/Outerplanar80_5.gml", destringizer=int)
    #G=nx.read_gml("BC_Planars/obg 14.gml", destringizer=int)


#Limite de colores
    Max_Color = 4

#Propiedad color a todos los nodos
    for i in range(0, len(G.nodes)):
        G.nodes[i]['color'] = 0

#Coloreado
    Coloreado()

#Resultados
    print("\n", "====== C O L O R E A D O ======","\n")
    for i in G.nodes:
        print("Nodo:_", i, "  Color:_", G.nodes[i]['color'])

#tiempo de ejecución
    print("\n","--- %s s ---" % (time.time() - start_time),"\n")

#Verificación del coloreado
    error = 0 
    for nodo in G.nodes():
        if verifica(nodo) == True:
            print ("\n", "Incidencia en el coloreado", "\n")
            error +1
    if error == 0:
        print ("\n", "Coloreado correcto sin errores", "\n")

#Número de colores usados
    print("\n", "El Numero de colores usados es:", colorUsado(), "\n")

#Visualización del grafo
    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()