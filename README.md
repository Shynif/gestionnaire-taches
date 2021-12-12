# Gestionnaire de tâches
NSI 2021 - gestionnaire de tâches

<br><br>

## ***Partie A*** : Nombre de collaborateurs
---
N°1 : Liste vers évènement
```py
def liste_evt(T) :
    e=[]
    for i,t in enumerate(T) :
        e.append((t[0],i,0)) # Ajoute le début de la tâche
        e.append((t[1],i,1)) # Ajoute la fin de la tâche
    return e # Trié en tri fusion sinon -> sorted(e,key=lambda x:x[0])
```

N°2 : Tri des évènements
```py
def trier_evt(T): # Stack-Reveret-Overflow
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
```

N°3 : Nombre de tâches en simultanées
```py
def nb_simultanees(E : list) -> int :
    maximum=0
    enCoursMaximum=0
    for element in E :
        enCoursMaximum=enCoursMaximum-1 if element[2] else enCoursMaximum+1
        maximum=max(enCoursMaximum,maximum)
    return maximum
```


<br><br>


## ***Partie B*** : Organisation des tâches
---
N°2 : Graph des tâches
```py
def graphe_tache(T) :
    g=Graph_as_list()
    [g.ajouter_sommet(f'T{i}') for i in range(len(T))]
    for i in range(len(T)) :
        for j in range(i,len(T)) :
            if (T[j][1]>T[i][0]>T[j][0]) or (T[i][1]>T[j][0]>T[i][0]) :
                g.ajouter_arete(f'T{i}',f'T{j}')
    return g
```

N°2 : Repartition des tâches
```py
def solve(g,enCours,role) -> dict : # 1 à 1
    n=0
    for i in range(len(g.voisins(enCours))) : # 2 pas mal, 1 marche pas
        for s in g.voisins(enCours) :
            if role[s] is not None and n==role[s] :
                n+=1
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
        # Calcul
        n=0
        for i in g.voisins(tache) : # On augmente de 1 en 1 donc on reactualise et augmente de 1 en 1
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
        # Calcul
        n=0
        for i in g.voisins(tache) : # On augmente de 1 en 1 donc on reactualise et augmente de 1 en 1
            for v in g.voisins(tache) :
                if role[v] is not None and n==role[v] :
                    n+=1
        role[tache]=n
    return role


def repartition(g, combinaisons : list) -> dict :
    role ={sommet:None for sommet in g.get_sommets()}
    roleb={sommet:None for sommet in g.get_sommets()}
    rolec={sommet:None for sommet in g.get_sommets()}
    for depart in combinaisons :
        role =  solve(g, depart,  role)
        roleb= solve2(g, depart, roleb)
        rolec= solve3(g, depart, rolec) # Notes : le désactiver donne le même résultat que dans le cour :)
    i=min({0:taille_repartition(role),1:taille_repartition(roleb),2:taille_repartition(rolec)})
    return [role,roleb,rolec][i]
```

N°3 : Taille de la répartition
```py
def taille_repartition(taches : dict) -> int :
    # Retourne la plus grande valeur du dictionnaire des tâches
    return max(taches.values())
```

N°4 : Optimisation de la répartiton des tâches selon toutes les combinaisons possibles
```py
def repartition_optimale(g) -> dict :
    sommet=g.get_sommets()
    maxi=float('inf')
    meilleurCalcul=None
    allSommet=[combinaison for combinaison in itertools.permutations(sommet, len(sommet))] # imaginer ne pas connaître itertools par coeur :^)        
    for combinaison in allSommet :
        resultat = repartition(g, combinaison)
        m=taille_repartition(resultat)
        if m<maxi :
            meilleurCalcul=resultat
            maxi=m
    return meilleurCalcul
```