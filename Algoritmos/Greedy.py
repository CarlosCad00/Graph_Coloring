import networkx as nx
import time 
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
Coloreado de un grafo con el mínimo de colores posibles
1.- 
'''

def colores_vecinos(G, V):          #Función que extrae los colores de los vecinos del nodo
    ColorAdj=[]
    for Adj in G.neighbors(V):
        ColorAdj.append(G.nodes[Adj]['color'])
    return ColorAdj                 #Retorna la lista de los colores adyacentes


def min_disponible(disp, usados):   #Función compara la lista de colores adyacentes al nodo y los colores disponibles

    Clibres = set(disp) - set(usados)
    x = min(Clibres)
    return x                        #Retorna el mínimo color disponible


def coloring(G):                    #Función que asigna el color a cada nodo del grafo
    
    Co = range(0, 50)
    for nodo in G.nodes():
        
        if G.nodes[nodo]['color'] == None:
            color = min_disponible(Co, colores_vecinos(G, nodo))
            G.nodes[nodo]['color'] = color


def verifica(nodo):             #Funcion que verifica el coloreado del grafo
     
    for Adj in G.neighbors(nodo):
        if G.nodes[nodo]['color'] == G.nodes[Adj]['color']:
            return True
        else:
            return False

def colorUsado():
    ColorUsado=[]
    for nodo in G.nodes():
        ColorUsado.append(G.nodes[nodo]['color'])
    x = max(ColorUsado)
    return x
    
def draw_graph():
    pos = nx.spring_layout(G)  # Cambia el diseño si lo deseas
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()

def show_results():
    result_text.delete("1.0", tk.END)  # Limpia el texto anterior
    result_text.insert(tk.END, "====== C O L O R E A D O ======\n")
    
    for i in G.nodes:
        result_text.insert(tk.END, f"Nodo: {i}, color: {G.nodes[i]['color']+1}\n")
    
    result_text.insert(tk.END, f"Tiempo: {tiempo_total} s\n")
    
    error = 0 
    for nodo in G.nodes():
        if verifica(nodo) == True:
            result_text.insert(tk.END, "Incidencia en el coloreado\n")
            error += 1
    if error == 0:
        result_text.insert(tk.END, "Coloreado correcto sin errores\n")
    
    result_text.insert(tk.END, f"Numero de colores usados: {colorUsado()+1}\n")
    
    draw_button = tk.Button(main_window, text="Dibujar Grafo", command=draw_graph)
    draw_button.pack()

if __name__ == "__main__":
    


#Creación del grafo inicial
    #G = nx.fast_gnp_random_graph(n= 100, p=0.30, seed=None, directed=False)

    #G=nx.read_gml("BC_Planars/obg 14.gml", destringizer=int)
        
    G=nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
    G.add_edges_from([(0, 1), (0, 3), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7), (5, 6), (6, 7)])


#Creando la propiedad "Color " a cada nodo

    for i in range(0, len(G.nodes)):
        G.nodes[i]['color'] = None
    start_time = time.time()
    coloring(G)


#Resultados del coloreado
    print("\n", "====== C O L O R E A D O ======","\n")
    for i in G.nodes:
        print("Nodo: ", i, "  color: ", G.nodes[i]['color']+1 )

    tiempo_total=time.time() - start_time
#Verificación del tiempo
    print("\n","--- %s s ---" % tiempo_total,"\n")


#Verificación  
    error = 0 
    for nodo in G.nodes():
        if verifica(nodo) == True:
            print ("Incidencia en el coloreado", "\n")
            error +1
    if error == 0:
        print ("Coloreado correcto sin errores", "\n")
    
    
    print("El Numero de colores usados es:", colorUsado()+1, "\n")
    
    #Dibujado del grafo
    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()

    main_window = tk.Tk()
    main_window.title("Coloreado de Grafo")

    result_text = tk.Text(main_window)
    result_text.pack()

    show_button = tk.Button(main_window, text="Mostrar Resultados", command=show_results)
    show_button.pack()

    main_window.mainloop()