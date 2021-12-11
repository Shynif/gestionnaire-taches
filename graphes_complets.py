import graphviz
from typing import Union
from pilesFiles import File
"""
Module implémentant les graphes

Pour rappel (source : https://en.wikipedia.org/wiki/Graph_(abstract_data_type))
The basic operations provided by a graph data structure G usually include:[1]

    * add_vertex(G, x): adds the vertex x, if it is not there;
    * add_edge(G, x, y): adds the edge from the vertex x to the vertex y, if it is not there;
    * adjacent(G, x, y): tests whether there is an edge from the vertex x to the vertex y;
    * neighbors(G, x): lists all vertices y such that there is an edge from the vertex x to the vertex y;
    * remove_vertex(G, x): removes the vertex x, if it is there;
    * remove_edge(G, x, y): removes the edge from the vertex x to the vertex y, if it is there;
    NON get_vertex_value(G, x): returns the value associated with the vertex x;
    NON set_vertex_value(G, x, v): sets the value associated with the vertex x to v.

Structures that associate values to the edges usually also provide:[1]

    get_edge_value(G, x, y): returns the value associated with the edge (x, y);
    set_edge_value(G, x, y, v): sets the value associated with the edge (x, y) to v.
"""


class Graph_as_list:
    """
    Classe implémentant un graphe non-orienté en tant que liste d'adjacence

    Le constructeur crée un graphe vide

    L'unique attibut est la liste d'adjacence codée sous forme d'un dictionnaire
    """

    def __init__(self):
        self.liste = {}

    def get_liste(self):
        """
        Renvoie la liste d'adjacence du graphe
        """
        return self.liste

    def get_sommets(self):
        """
        Renvoie la liste des noms des sommets
        """
        return list(self.liste.keys())

    def ajouter_sommet(self, nom: str) -> None:
        """
        Ajoute le sommet indiqué par son nom au graphe
        """
        assert isinstance(
            nom, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert nom not in self.liste, "Un sommet portant le même nom existe déjà"

        self.liste[nom] = [[],'black']

    def ajouter_arete(self, s1: str, s2: str) -> None:
        """
        Ajoute une arête entre les sommets de noms s1 et s2
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.liste, "Aucun sommet ne porte ce nom"
        assert s2 in self.liste, "Aucun sommet ne porte ce nom"

        self.liste[s1][0].append(s2)
        self.liste[s2][0].append(s1)

    def adjacent(self, s1: str, s2: str) -> bool:
        """
        Renvoie True si s2 est voisin avec s1
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.liste, "Aucun sommet ne porte ce nom"
        assert s2 in self.liste, "Aucun sommet ne porte ce nom"

        return s2 in self.liste[s1][0]

    def voisins(self, s: str) -> list:
        """
        Retourne la liste des voisins de s
        """
        assert isinstance(
            s, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s in self.liste, "Aucun sommet ne porte ce nom"

        return self.liste[s][0]

    def retirer_sommet(self, s: str) -> None:
        """
        Retire le sommet s du graphe ainsi que les arêtes associées
        """
        assert isinstance(
            s, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s in self.liste, "Aucun sommet ne porte ce nom"

        self.liste.pop(s)

        for sommet in self.liste:
            if s in self.liste[sommet][0]:
                self.liste[sommet][0].remove(s)

        return None

    def retirer_arete(self, s1: str, s2: str) -> None:
        """
        Retire l'arête s1-s2 du graphe
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.liste, "Aucun sommet ne porte ce nom"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s2 in self.liste, "Aucun sommet ne porte ce nom"
        assert s2 in self.liste[s1][0], "L'arête s1-s2 n'existe pas"

        self.liste[s1][0].remove(s2)
        self.liste[s2][0].remove(s1)

        return None

    def dessiner(self, nom='export_graphe.png'):
        """
        Représente le graphe à l'aide de graphviz
        """
        g = graphviz.Graph(format="png", strict=True)
        aretes = []

        for s in self.liste:
            g.node(s, color=self.liste[s][1], style='filled', fontcolor='white')
            for v in self.liste[s][0]:
                if (s, v) not in aretes:
                    g.edge(s, v)
                    aretes.append((v, s))

        g.render(nom, view=True)

        return None


class Graph_as_matrix:
    """
    Classe implémentant un graphe non-orienté en tant que matrice d'adjacence

    Le constructeur crée un graphe vide

    L'objet a deux attributs :
        * la liste des noms des sommets qui permet de faire le lien entre nom et indice 
            (l'indice d'un sommet dans la liste correspond à celui dans la matrice)
        * la matrice d'adjacence
    """

    def __init__(self):
        self.matrice = []
        self.noms = []

    def get_matrice(self):
        """
        Renvoie la matrice d'adjacence du graphe
        """
        return self.matrice

    def get_sommets(self):
        """
        Renvoie la liste des noms des sommets
        """
        return self.noms

    def ajouter_sommet(self, nom: str) -> None:
        """
        Ajoute le sommet indiqué par son nom au graphe
        """
        assert isinstance(
            nom, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert nom not in self.noms, "Un sommet portant le même nom existe déjà"

        taille = len(self.noms)

        for ligne in self.matrice:
            ligne += [0]

        self.matrice.append([0] * (taille + 1))

        self.noms.append(nom)

    def ajouter_arete(self, s1: str, s2: str, poids = 1) -> None:
        """
        Ajoute une arête entre les sommets de noms s1 et s2
        La valeur de l'arête est par défaut 1 dans les deux sens
        L'arête est ajoutée par défaut dans les deux directions
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.noms, "Aucun sommet ne porte ce nom"
        assert s2 in self.noms, "Aucun sommet ne porte ce nom"
        assert isinstance(poids, (int, float)
                          ), "Le poids doit être un nombre (int ou float)"

        i1 = self.noms.index(s1)
        i2 = self.noms.index(s2)

        self.matrice[i1][i2] = poids
        self.matrice[i2][i1] = poids

    def adjacent(self, s1: str, s2: str) -> bool:
        """
        Renvoie True si s2 est voisin avec s1
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.noms, "Aucun sommet ne porte ce nom"
        assert s2 in self.noms, "Aucun sommet ne porte ce nom"

        i1 = self.noms.index(s1)
        i2 = self.noms.index(s2)

        return self.matrice[i1][i2] != 0

    def voisins(self, s: str) -> list:
        """
        Retourne la liste des voisins de s
        """
        assert isinstance(
            s, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s in self.noms, "Aucun sommet ne porte ce nom"

        i = self.noms.index(s)

        voisins = []
        for j, v in enumerate(self.matrice[i]):
            if v != 0:
                voisins.append(self.noms[j])

        return voisins

    def retirer_sommet(self, s: str) -> None:
        """
        Retire le sommet s du graphe ainsi que les arêtes associées
        """
        assert isinstance(
            s, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s in self.noms, "Aucun sommet ne porte ce nom"

        i = self.noms.index(s)

        self.noms.remove(s)

        self.matrice.pop(i)

        for indice, ligne in enumerate(self.matrice):
            self.matrice[indice] = [v for k, v in enumerate(ligne) if k != i]

        return None

    def retirer_arete(self, s1: str, s2: str) -> None:
        """
        Retire l'arête s1-s2 du graphe
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.noms, "Aucun sommet ne porte ce nom"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s2 in self.noms, "Aucun sommet ne porte ce nom"

        i1 = self.noms.index(s1)
        i2 = self.noms.index(s2)

        assert self.matrice[i1][i2] != 0, "L'arête s1-s2 n'existe pas"

        self.matrice[i1][i2] = 0
        self.matrice[i2][i1] = 0

        return None

    def get_valeur_arete(self, s1: str, s2: str) -> Union[int, float]:
        """
        Retourne la valeur associée à l'arête s1-s2
        (qui peut être différente de celle associée à s2-s1 si on a utilisé set_valeur_arete)
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.noms, "Aucun sommet ne porte ce nom"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s2 in self.noms, "Aucun sommet ne porte ce nom"

        i1 = self.noms.index(s1)
        i2 = self.noms.index(s2)

        return self.matrice[i1][i2]

    def set_valeur_arete(self, s1: str, s2: str, valeur: Union[int, float]) -> None:
        """
        Affecte la valeur à l'arête s1-s2
        """
        assert isinstance(
            s1, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s1 in self.noms, "Aucun sommet ne porte ce nom"
        assert isinstance(
            s2, str), "Le nom du sommet doit être une chaîne de carcatères"
        assert s2 in self.noms, "Aucun sommet ne porte ce nom"
        assert isinstance(valeur, (int, float)
                          ), "La valeur doit être un nombre (int ou float)"

        i1 = self.noms.index(s1)
        i2 = self.noms.index(s2)

        self.matrice[i1][i2] = valeur

    def dessiner(self, nom='export_graphe.png', oriente: bool = False):
        """
        Représente le graphe à l'aide de graphviz
        Par défaut le graphe est non-orienté.
        Il est possible de changer cela avec la variable oriente

        oriente : Le graphe est-il orienté, False par défaut (bool)
        """
        
        g = None
        if not oriente:
            g = graphviz.Graph(format="png", strict=True)
        else:
            g = graphviz.Digraph(format="png", strict=True)

        aretes = []

        for s in self.noms:
            g.node(s)
            i = self.noms.index(s)
            for j, v in enumerate(self.matrice[i]):
                if v != 0:
                    if (i, j) not in aretes and not oriente :
                        g.edge(s, self.noms[j], label=str(v))
                        aretes.append(sorted([j, i]))
                    else:
                        g.edge(s, self.noms[j], label=str(v))
        g.render(nom, view=True)

        return None


def profondeur(G : Union[Graph_as_list, Graph_as_matrix], depart : str, visites = []) -> None:
    """Parcours en profondeur d'abord de G en partant de départ

    Args:
        G (Union[Graph_as_list, Graph_as_matrix]): un graphe donné sous forme d'une matrice ou d'une liste d'adjacence
        depart (str): Le nom du sommet de départ
    """
    assert depart in G.get_sommets(), "Le départ n'est pas dans la liste des sommets"

    visites.append(depart)
    print(depart)
    for voisin in G.voisins(depart) :
        if voisin not in visites :
            profondeur(G, voisin, visites)

def largeur(G : Union[Graph_as_list, Graph_as_matrix], depart : str) -> None :
    """Parcours en largeur d'abord de G en partant de départ

    Args:
        G (Union[Graph_as_list, Graph_as_matrix]): un graphe donné sous forme d'une matrice ou d'une liste d'adjacence
        depart (str): Le nom du sommet de départ
    """
    assert depart in G.get_sommets(), "Le départ n'est pas dans la liste des sommets"

    f = File()
    f.enfiler(depart)
    visites = [depart]
    while not f.est_vide() :
        s = f.defiler()
        print(s)
        for voisin in G.voisins(s) :
            if voisin not in visites:
                f.enfiler(voisin)
                visites.append(voisin)

if __name__ == "__main__":
    # Essai du graphe en tant que matrice
    g = Graph_as_matrix()
    g.ajouter_sommet("Essai")
    g.ajouter_sommet("Hello")
    g.ajouter_sommet("World")
    g.ajouter_sommet("Bonjour")
    g.ajouter_sommet("Le")
    g.ajouter_sommet("Monde")
    g.ajouter_arete("Hello", "World")
    g.ajouter_arete("Essai", "Hello")
    g.ajouter_arete("Essai", "Bonjour")
    g.ajouter_arete("Le", "Bonjour")
    g.ajouter_arete("Le", "Monde")
    g.ajouter_arete("Le", "World")
    print(g.get_sommets())
    g.retirer_arete('Le', "World")
    g.retirer_arete('Essai', "Hello")
    g.retirer_arete('Essai', "Bonjour")
    g.retirer_sommet("Essai")
    print(g.get_sommets())
    print(g.voisins("Le"))
    g.dessiner(oriente=False)
    profondeur(g, "Bonjour")
    
    """
    # Essai du graphe en tant que liste
    g = Graph_as_list()
    g.ajouter_sommet("Essai")
    g.ajouter_sommet("Hello")
    g.ajouter_sommet("World")
    g.ajouter_sommet("Bonjour")
    g.ajouter_sommet("Le")
    g.ajouter_sommet("Monde")
    g.ajouter_arete("Hello", "World")
    g.ajouter_arete("Essai", "Hello")
    g.ajouter_arete("Essai", "Bonjour")
    g.ajouter_arete("Le", "Bonjour")
    g.ajouter_arete("Le", "Monde")
    g.ajouter_arete("Le", "World")
    print(g.get_sommets())
    g.retirer_arete('Le', "World")
    g.retirer_arete('Essai', "Hello")
    g.retirer_arete('Essai', "Bonjour")
    g.retirer_sommet("Essai")
    print(g.get_sommets())
    print(g.voisins("Le"))
    g.dessiner()
    """
