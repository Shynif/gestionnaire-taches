from random import sample, shuffle, randint
from pilesFiles import Pile, File
from graphes_complets import Graph_as_list, Graph_as_matrix

import itertools # *menacing sound* :)
import concurrent.futures # Run I said

def n_taches(nb_taches : int) -> list :
    """Renvoie une liste de nb_taches tâches

    Args:
        nb_taches (int): le nombre de tâches souhaitées

    Returns:
        list: Une liste de  tâches au format (début, fin). Tous les instants sont différents
    """
    assert type(nb_taches) == int and nb_taches > 0, "nb_taches doit être un entier strictement positif"

    instants = [k for k in range(3*nb_taches)]
    instants = sample(instants, nb_taches*2)
    shuffle(instants)
    return [tuple(sorted([instants[k], instants[k+1]])) for k in range(0, len(instants), 2)]


def viz(T) :
    from matplotlib import pyplot as plt
    from matplotlib.patches import Rectangle
    for i,t in enumerate(T) :
        rect=Rectangle((t[0],i*3), t[1]-t[0],2)
        plt.gca().add_patch(rect)
    plt.ylim([0,len(T)*3])
    plt.xlim([0,max(T,key=lambda x:x[1])[1]])
    plt.show()

def liste_evt(T) :
    e=[]
    for i,t in enumerate(T) :
        e.append((t[0],i,0)) # Ajoute le début de la tâche
        e.append((t[1],i,1)) # Ajoute la fin de la tâche
    return e # Trié en tri fusion sinon -> sorted(e,key=lambda x:x[0])

def trier_evt(T): # Stack-Reveret-Overflow
    """
    trie la liste par la méthode de fusion 
    T (list)
    """
    longueur = len(T)
    if longueur == 1:
        return T
    else:
        debut = trier_evt(T[:longueur // 2])
        fin = trier_evt(T[longueur // 2:])

        retour = []

        while (debut and fin):
            if debut[0] < fin[0]:
                retour.append(debut.pop(0))
            else:
                retour.append(fin.pop(0))
        while debut:
            retour.append(debut.pop(0))
        while fin:
            retour.append(fin.pop(0))

    return retour

def nb_simultanees(E : list) -> int :
    maximum=0
    enCoursMaximum=0
    for element in E :
        enCoursMaximum=enCoursMaximum-1 if element[2] else enCoursMaximum+1
        maximum=max(enCoursMaximum,maximum)
    return maximum

def graphe_tache(T) :
    g=Graph_as_list()
    [g.ajouter_sommet(f'T{i}') for i in range(len(T))]
    for i in range(len(T)) :
        for j in range(i,len(T)) :
            if (T[j][1]>T[i][0]>T[j][0]) or (T[i][1]>T[j][0]>T[i][0]) :
                g.ajouter_arete(f'T{i}',f'T{j}')
    return g


def taille_repartition(taches : dict) -> int : # Retourne la plus grande valeur du dictionnaire des tâches
    return max(taches.values())


def repartitionThread() -> dict :
    global inProcess
    global allSommet
    global g
    while allSommet :
        role={sommet:None for sommet in g.get_sommets()}
        for enCours in allSommet.pop() :
            # SOLVE
            n=0
            for i in range(len(g.voisins(enCours))) : # 2 pas mal, 1 marche pas
                for s in g.voisins(enCours) :
                    if role[s] is not None and n==role[s] :
                        n+=1
            role[enCours]=n
        inProcess.append((role, taille_repartition(role)))


if __name__ == "__main__" :
    nb_taches = 8
    T = n_taches(nb_taches)
    #T = [(5, 12), (13, 15), (0, 2), (1, 4), (3, 7), (10, 14), (8, 11), (6, 9)]
    E = liste_evt(T)
    E = trier_evt(E)
    #print("T=", T)
    #print("E=", E)
    simul=nb_simultanees(E) # Partie A
    #print(simul)
    g=graphe_tache(T)
    [g.retirer_sommet(s) for s in g.get_sommets() if not g.voisins(s)] # Supprime les tâches sans voisins pouvant être effectués par l'ouvrier n°0


    maxi=float('inf')
    resultatFinal=None
    sommet = g.get_sommets()
    allSommet=[combinaison for combinaison in itertools.permutations(sommet, len(sommet))] # imaginer ne pas connaître itertools par coeur :^)
    inProcess=[]
    executor = concurrent.futures.ThreadPoolExecutor()
    executor.submit(repartitionThread)
    while inProcess or allSommet :
        #print(allSommet,inProcess)
        if inProcess :
            pr=inProcess.pop()
            if pr[1]<maxi :
                maxi=pr[1]
                resultatFinal=pr[0]


    # Coloration dugraph selon le résultat
    r = lambda: randint(0,255)
    colorsGraph=['#%02X%02X%02X' % (r(),r(),r()) for i in range(simul)]
    for s in g.get_sommets() :
        g.liste[s][1] = colorsGraph[resultatFinal[s]]
    
    # Dessin final et résultat
    g.dessiner()
    print(resultatFinal)

    # Visualisation des tâches
    viz(T)