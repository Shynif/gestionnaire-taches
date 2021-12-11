from random import sample, shuffle, randint
from pilesFiles import Pile, File
from graphes_complets import Graph_as_list, Graph_as_matrix

import itertools # *menacing sound* :)

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
        e.append((t[0],i,0))
        e.append((t[1],i,1))
    return e #sorted(e,key=lambda x:x[0])

def fusion(T): # Stack-Reveret-Overflow
    """
    trie la liste par la méthode de fusion 
    T (list)
    """
    longueur = len(T)
    if longueur == 1:
        return T
    else:
        debut = fusion(T[:longueur // 2])
        fin = fusion(T[longueur // 2:])

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

def nb_simultanees(E) :
    mm=0
    m=0
    for e in E :
        m =m-1 if e[2] else m+1
        mm=max(m,mm)
    return mm

def graphe_tache(T) :
    g=Graph_as_list()
    [g.ajouter_sommet(f'T{i}') for i in range(len(T))]
    for i in range(len(T)) :
        for j in range(i,len(T)) :
            if (T[i][0]>T[j][0] and T[i][0]<T[j][1]) or (T[i][1]>T[j][0] and T[i][1]<T[j][1]) :
                g.ajouter_arete(f'T{i}',f'T{j}')
    return g

def solve(g,enCours,role) : # 1 à 1
    n=0
    for i in range(len(g.voisins(enCours))) : # 2 pas mal, 1 marche pas
        for s in g.voisins(enCours) :
            if role[s] is not None and n==role[s] :
                n+=1
    role[enCours]=n
    return role

def solve2(g,enCours,role) : # Largeur
    f=[enCours] # File (sans File car trop lent)
    visite=[enCours]
    while f :
        tache=f.pop(0) # Defile
        for voisin in g.voisins(tache) :
            if voisin not in visite :
                visite.append(voisin)
                f.append(voisin) # Enfile
        # Calcul
        n=0
        for i in g.voisins(tache) : # On augmente de 1 en 1 donc on reactualise et augmente de 1 en 1
            for v in g.voisins(tache) :
                if role[v] is not None and n==role[v] :
                    n+=1
        role[tache]=n
    return role

def solve3(g,enCours,role) : # Profondeur
    p=[enCours] # Pile (sans Pile car trop lent)
    visite=[enCours]
    while p :
        tache=p.pop() # Depile
        for voisin in g.voisins(tache) :
            if voisin not in visite :
                visite.append(voisin)
                p.append(voisin) # Enpile
        # Calcul
        n=0
        for i in g.voisins(tache) : # On augmente de 1 en 1 donc on reactualise et augmente de 1 en 1
            for v in g.voisins(tache) :
                if role[v] is not None and n==role[v] :
                    n+=1
        role[tache]=n
    return role

def taille_operation(taches) :
    '''maxi=0
    for v in taches.values() :
        maxi=max(maxi,v)
    return maxi'''
    return max(taches.values())

def cracker(g,combinaisons) :
    role={sommet:None for sommet in g.get_sommets()}
    roleb={sommet:None for sommet in g.get_sommets()}
    rolec={sommet:None for sommet in g.get_sommets()}    
    for depart in combinaisons :
        role=solve2(g,depart,role)
        roleb=solve(g,depart,roleb)
        rolec=solve(g,depart,rolec)
    i=min({0:taille_operation(role),1:taille_operation(roleb),2:taille_operation(rolec)})
    return [role,roleb,rolec][i]


def tacheComplet(g) :
    sommet=g.get_sommets()
    maxi=float('inf')
    meilleurCalcul=None
    allSommet=[combinaison for combinaison in itertools.permutations(sommet, len(sommet))] # imaginer ne pas connaître itertools par coeur :^)        
    for combinaison in allSommet :
        resultat = cracker(g, combinaison)
        m=taille_operation(resultat)
        if m<maxi :
            meilleurCalcul=resultat
            maxi=m
    return meilleurCalcul


if __name__ == "__main__":
    nb_taches = 8
    T = n_taches(nb_taches)
    # T = [(5, 12), (13, 15), (0, 2), (1, 4), (3, 7), (10, 14), (8, 11), (6, 9)]
    E = liste_evt(T)
    E = fusion(E)
    #print("T=", T)
    #print("E=", E)
    simul=nb_simultanees(E) # Partie A
    #print(simul)
    g=graphe_tache(T)
    [g.retirer_sommet(s) for s in g.get_sommets() if not g.voisins(s)] # Supprime les tâches sans voisins pouvant être effectués par l'ouvrier n°0


    resultatFinal=tacheComplet(g)


    # Coloration dugraph selon le résultat
    r = lambda: randint(0,255)
    colorsGraph=['#%02X%02X%02X' % (r(),r(),r()) for i in range(simul)]
    for s in g.get_sommets() :
        g.liste[s][1] = colorsGraph[resultatFinal[s]]
    
    # Dessin final et résultat
    g.dessiner()
    #print(resultatFinal)

    # Visualisation des tâches
    #viz(T)