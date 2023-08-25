import networkx as nx
import matplotlib.pyplot as plt
import time

'''
Coloring by Tabu
'''

def Diferent_Colored(V):          #Función que extrae los colores de los vecinos del nodo
    ClrAdj=[]
    for Adj in G.neighbors(V):
        if G.nodes[Adj]['color'] != None and G.nodes[Adj]['color']!=0:
            ClrAdj.append(G.nodes[Adj]['color'])
    Dg = set(ClrAdj)
    #print("Conjunto:",len(Dg))
    return Dg                 ###Devolver un entero



def MAX_COLOR(G,isPlanar):                   #Funcion que calcula el maximo de colores
    Grados=[]                       
    if isPlanar:
        return 4
    for nodo in G.nodes():
        Grados.append(G.degree(nodo))
    return max(Grados) + 1              ###Debe ser delta +1

def Uncolored(i):           #Numero de vertices NO coloreados 
    No_color =[]
    for nodo in G.neighbors(i):
        if G.nodes[nodo]['color'] == None:
            No_color.append(nodo)
    return No_color            ###Devolver entero


def Colored(i):             #Numero de vertices coloreados
    No_color =[]
    for nodo in G.neighbors(i):
        if G.nodes[nodo]['color'] != None:
            No_color.append(nodo)
    return No_color            ###Devolver entero


def potential_difference(i):
    P_diff = len(Diferent_Colored(i))+ len(Uncolored(i))
    
    return P_diff


def CC_dependent(i):

    if potential_difference(i)< MAX_COLOR(G,True):
        CC=True
    else: 
        CC= False

    return CC

'''
def Share(node):  #Colores disponibles para este nodo y sus vecinos
    
    AUX = []
    for i in G.neighbors(node):
        if G.nodes[i]['color'] == None:
            for x in G.neighbors(i):
                AUX.append(G.nodes[x]['color'])       
    Shared = Avail(node).union(set(AUX)) 

    return Shared
'''
def Share(node):  #Colores disponibles para este nodo y sus vecinos
    AUX = []
    for i in G.neighbors(node):
        if G.nodes[i]['color'] == None:
            AUX = Avail(node).union (Avail(i))       
    return AUX 

def setShare(node):  #Colores disponibles para este nodo y sus vecinos
    AUX = []
    ColorDisp = list(range(1, MAX_COLOR(G,True)+1))
    #print(ColorDisp)
    for i in G.neighbors(node):
        if G.nodes[i]['color'] == None:
            AUX = setAvail(node).union(setAvail(i))
    myShare=set(ColorDisp)-set(AUX)      
    return myShare 

def setAvail(node):
    ColorAdj =[]
    ColorDisp = list(range(1, MAX_COLOR(G,True)+1))
    for i in G.neighbors(node):
        if G.nodes[i]['color']!=None:
            ColorAdj.append(G.nodes[i]['color'])
    myAvail=set(ColorDisp)-set(ColorAdj)
    return myAvail


def Avail(node):              #colores disponibles para el nodo i
    ColorAdj =[]
    ColorDisp = list(range(0, MAX_COLOR(G,True)+1))
    for i in G.neighbors(node):
        if G.nodes[i]['color']!=None:
            ColorAdj.append(G.nodes[i]['color'])
    SetAvail=set(ColorAdj)
    Available = set(ColorDisp) - set(ColorAdj)
    return Available                # Avail = max color menos los colores usados

def F(y):                        #Funcion F
    C=1.0
    K=1.0
    #print("Max_", y)
    F = C/((MAX_COLOR(G,True)-y)**K)

    return F

def computeDanger(i,K,Ku,Ka):          #Calcula el NODO DANGER
#First iteration K=1,Ku=1, Ka= 0
#Second iteration K=1,Ku=0.025, Ka= 0.33
    if Ka!=0:
        dng = F(len(Diferent_Colored(i))) + (Ku* len(Uncolored(i))) + (Ka* (len(setShare(i))/len(setAvail(i))))
    else:
        dng = len(Diferent_Colored(i)) + (Ku* len(Uncolored(i))) + (Ka* (len(setShare(i))/len(setAvail(i))))
    #print ("danger(",i,")=", dng)
    return dng


def Danger_node(i):          #Calcula el NODO DANGER
#Constantes

    K = 1.0
    Ku = 1#0.025
    Ka = 0#0.33
    V = None
    
    #dng = F(len(Diferent_Colored(i))) + (Ku* len(Uncolored(i))) + (Ka* (len(setShare(i))/len(setAvail(i))))
    dng = len(Diferent_Colored(i)) + (Ku* len(Uncolored(i))) + (Ka* (len(setShare(i))/len(setAvail(i))))
    #print ("danger(",i,")=", dng)
    return dng


def diff_neighbors(C):          #Maximo numero de diferentes nodos coloreados
    maximo = 0
    for x in G.nodes():
        if G.nodes[x]['color'] == None:
            for i in G.neighbors(x):
                if G.nodes[x]['color'] != C:
                    Gds = len (Diferent_Colored(G, x))
                    if Gds > maximo:
                        maximo = Gds
    return maximo  #devolver también el nodo


def num (C):                    #Revisa las veces que se ha usado el color "C"
    used = 0
    for i in G.nodes():
        if G.nodes[i]['color'] == C:
            used += 1
    return used


def Danger_color(C, Nc):            #Función de color danger
    K1=1.0
    K2=1.0
    K3=0.5
    K4=0.25

    Dgr_clr= K1/((len(MAX_COLOR(G,True))- len(diff_neighbors(C)))**K2)+(K3* len(Uncolored(Nc)))-(K4* num(C))

    return Dgr_clr

def colores_vecinos(V):          #Función que extrae los colores de los vecinos del nodo
    ColorAdj=[]
    for Adj in G.neighbors(V):
        ColorAdj.append(G.nodes[Adj]['color'])
    return ColorAdj                 #Retorna la lista de los colores adyacentes

def min_disponible(disp, usados):   #Extrae el mínimo color disponible

    Clibres = set(disp) - set(usados)
    x = min(Clibres)
    return x                        #Retorna el mínimo color disponible


def ActualizaDanger():                  #Función que actualiza el valor de danger en cada nodo

    for i in G.nodes() :              #Asigna DDANGER a cada nodo
        if G.nodes[i]['color'] != 0:
            G.nodes[i]['DNG'] = computeDanger(i,1,0.025, 0.33)
        else:
            G.nodes[i]['DNG'] = 0

def DangerMayor ():                 #Selecciona el nodo con el valor más alto de Danger para colorear
    Danger = {} 
    Grado = {}
    ActualizaDanger()

    for nodo in G.nodes(): 
        if G.nodes[nodo]['color'] == None:
            Danger [nodo] = G.nodes[nodo]['DNG']
            
    SMayor = [key for key, value in Danger.items() if value == max(Danger.values())]
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

def coloring(X):                    #Funcion que selecciona el minimo color disponible y colorea el nodo
    Co = range(1, MAX_COLOR(G,True)+1)
    ActualizaDanger()    
    color = min_disponible(Co, colores_vecinos(X))
    G.nodes[X]['color'] = color


def verifica(nodo):             #Funcion que verifica el coloreado del grafo
     
    for Adj in G.neighbors(nodo):
        if G.nodes[nodo]['color'] == G.nodes[Adj]['color']:
            return True
        else:
            return False
    
def areUncolored():
    for i in G.nodes():
            if G.nodes[i]['color'] == None: 
                return True
    return False

    
def actualizarCCDependant():
    for i in G.nodes():
        if G.nodes[i]['color'] == None: 
            if (computeDanger(i,1.0,1.0,0)<MAX_COLOR(G,True)):
                print("El nodo ",i," se guarda en CC_dependant")
                G.nodes[i]['color'] = 0

def colorUsado(G):
    ColorUsado=[]
    for nodo in G.nodes():
        ColorUsado.append(G.nodes[nodo]['color'])
    x = max(ColorUsado)
    return x


if __name__ =="__main__":
    start_time = time.time()
#Grafo de entrada

    #G = nx.fast_gnp_random_graph(n= 7, p=0.40, seed=None, directed=False)        #Genera grafos ALEATORIOS n=#nodos 
    #G = nx.read_gml("Instances/Outerplanar50.gml", destringizer=int)              #Genera grafos a partir de ARCHIVOS (.gml)
    
    
    G=nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edges_from([(0, 1), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7), (5, 6), (6, 7)])
    #G = nx.read_gml("PlaneGraphs/80Nodes/Outerplanar80_4.gml", destringizer=int)

    for i in G.nodes():
        G.nodes[i]['color'] = None

#DANGER INICIAL
    print("\n", "====== D A N G E R _____I N I C I A L ======","\n")
    for i in G.nodes():
        dangerAux=computeDanger(i,1.0,1.0,0)
        if (dangerAux<MAX_COLOR(G,True)):
            G.nodes[i]['color'] = 0 #These are cc_dependant
        print("Nodo: ", i, "  Danger: ",computeDanger(i,1.0,1.0,0) )


#Ciclo de coloreado
    coloreados = []
    uncolored=areUncolored()
    while len(coloreados)!= len(G.nodes()) and uncolored:
        coloreados.append(DangerMayor())
        coloring(DangerMayor())
        actualizarCCDependant()
        uncolored=areUncolored()

#Colorear los nodos en CC-Dependand
    CC_dependant=[]
    for i in G.nodes():
        if G.nodes[i]['color'] == 0:
            CC_dependant.append(i)

    for i in CC_dependant:
        coloring(i)
        

#Resultados del coloreado
    print("\n", "====== C O L O R E A D O ======","\n")
    for i in G.nodes():
        print("Nodo: ", i, "  color: ", G.nodes[i]['color'])
 
    print("\n","--- %s seconds ---" % (time.time() - start_time),"\n")

#Verificación  
    error = 0 
    for nodo in G.nodes():
        if verifica(nodo) == True:
            print ("\n", "Incidencia en el coloreado", "\n")
            error +1
    if error == 0:
        print ("\n", "Coloreado correcto sin errores", "\n")    

print("El Numero de colores usados es:", colorUsado(G))


#Visualización del grafo
    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()
    