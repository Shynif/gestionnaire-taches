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


def viz(T) : # Visualisation des tâches T utilisant des rectangles de Matplotlib
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
        # Ajoute ou enlève 1 à au maximum en cour selon si une tâche démarre ou finit
        enCoursMaximum=enCoursMaximum-1 if element[2] else enCoursMaximum+1
        maximum=max(enCoursMaximum,maximum) # Ré-actualise le maximum
    return maximum

def graphe_tache(T) :
    # Crée une liste vide
    g=Graph_as_list()
    [g.ajouter_sommet(f'T{i}') for i in range(len(T))]
    # Itère à travers tout les éléments
    for i in range(len(T)) :
        for j in range(i,len(T)) :
            if (T[j][1]>T[i][0]>T[j][0]) or (T[i][1]>T[j][0]>T[i][0]) : # Si les tâches sont en même temps
                g.ajouter_arete(f'T{i}',f'T{j}')                        # Ajoute l'arrête
    return g

def solve(g,enCours,role) -> dict : # 1 à 1
    ###  Calcul classique pour obtenir le plus numéro de tâche possible
    n=0 # Numéro basique
    # Va à travers la liste de-nouveau pour réactualiser les valeurs et être sûr de ne pas avoir de nouvelle égalités
    # Autre façon de le comprendre : On augmente de 1 en 1 donc on reactualise et augmente de 1 en 1 en cas de nouvelle égalité
    for i in range(len(g.voisins(enCours))) :
        # Itère à travers tout les voisins pour regarder si ils sont égaux
        for s in g.voisins(enCours) :
            if role[s] is not None and n==role[s] : # Si un voisin à déjà le numéro
                n+=1                                # Prend le numéro supérieur
    role[enCours]=n
    return role

def solve2(g,enCours,role) -> dict : # Largeur
    f=[enCours] # File (sans File car trop lent) mais sans deque (car trop la flemme)
    visite=[enCours]
    while f :
        tache=f.pop(0) # Defile
        for voisin in g.voisins(tache) :
            if voisin not in visite :
                visite.append(voisin)
                f.append(voisin) # Enfile
        ###  Calcul classique de SOLVE()
        n=0
        for i in g.voisins(tache) :
            for v in g.voisins(tache) :
                if role[v] is not None and n==role[v] :
                    n+=1
        role[tache]=n
    return role

def solve3(g,enCours,role) -> dict : # Profondeur
    p=[enCours] # Pile (sans Pile car trop lent) mais sans deque (car trop la flemme)
    visite=[enCours]
    while p :
        tache=p.pop() # Depile
        for voisin in g.voisins(tache) :
            if voisin not in visite :
                visite.append(voisin)
                p.append(voisin) # Enpile
        ###  Calcul classique de SOLVE()
        n=0
        for i in g.voisins(tache) :
            for v in g.voisins(tache) :
                if role[v] is not None and n==role[v] :
                    n+=1
        role[tache]=n
    return role


def taille_repartition(taches : dict) -> int : # Retourne la plus grande valeur du dictionnaire des tâches
    return max(taches.values())


def repartition(g, combinaisons : list) -> dict :
    role ={sommet:None for sommet in g.get_sommets()}
    #roleb={sommet:None for sommet in g.get_sommets()}
    #rolec={sommet:None for sommet in g.get_sommets()}
    for depart in combinaisons :
        role =  solve(g, depart,  role)
        #roleb= solve2(g, depart, roleb)
        #rolec= solve3(g, depart, rolec) # Notes : le désactiver donne le même résultat que dans le cour pour l'exemple donné :)
    #i=min({0:taille_repartition(role),1:taille_repartition(roleb),2:taille_repartition(rolec)})
    #return [role,roleb,rolec][i]
    return role


def repartition_optimale(g) -> dict :
    sommet=g.get_sommets()
    maxi=float('inf')
    meilleurCalcul=None
    # Crée TOUTES les permutations possibles des sommets, TRES gourmand
    allSommet=[combinaison for combinaison in itertools.permutations(sommet, len(sommet))] # imaginer ne pas connaître itertools par coeur :^)        
    for combinaison in allSommet :
        resultat = repartition(g, combinaison)
        m=taille_repartition(resultat)
        if m<maxi :
            meilleurCalcul=resultat
            maxi=m
    '''
    # Version plus simple,  ne donne pas la meilleure solution à tout les coups
    allSommet = g.get_sommets()
    for i in range(len(allSommet)) :
        resultat = repartition(g, allSommet)
        m=taille_repartition(resultat)
        if m<maxi :
            meilleurCalcul=resultat
            maxi=m
        allSommet.append(allSommet.pop()) # Chenille :)
        #shuffle(allSommet) # Version aléatoire qui supprent souvent
    '''
    return meilleurCalcul


if __name__ == "__main__":
    nb_taches = 5
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


    resultatFinal=repartition_optimale(g)


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
