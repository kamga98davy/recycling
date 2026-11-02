import json


# ---------- Chargement des données ----------

def charger_donnees(chemin_fichier):
    """
    Lit un fichier JSON et renvoie son contenu sous forme de dictionnaire.

    Args:
        chemin_fichier (str): Le chemin vers le fichier JSON.

    Returns:
        dict: Le contenu du fichier JSON.
    """
    with open(chemin_fichier, "r", encoding="utf-8") as fichier:
        contenu = json.load(fichier)
    return contenu


# ---------- Affichage ----------

def afficher_etat(joueur):
    """Affiche le nom, l'énergie et les ressources du joueur."""
    print("==============================")
    print(f"{joueur['nom']} | Énergie : {joueur['energie']}")
    print("Ressources :")
    for ressource, quantite in joueur["ressources"].items():
        print(f"  - {ressource} : {quantite}")
    print("==============================")


def afficher_lieux(lieux):
    """Affiche les lieux numérotés, avec (fouillé) pour ceux qui sont vides."""
    print("Lieux à explorer :")
    numero = 1
    for lieu in lieux:
        if lieu["quantite"] == 0:
            print(f"  {numero}. {lieu['nom']} (fouillé)")
        else:
            print(f"  {numero}. {lieu['nom']}")
        numero = numero + 1


def afficher_objectif(joueur, objectif):
    """Affiche, pour chaque ressource, ce que le joueur possède et ce qu'il doit atteindre."""
    print("Objectif :")
    for ressource in objectif:
        print(f"  - {ressource} : {joueur['ressources'][ressource]} / {objectif[ressource]}")


def afficher_menu(tour):
    """Affiche le numéro du tour et les choix possibles."""
    print()
    print(f"--- Tour {tour} ---")
    print("Que veux-tu faire ?")
    print("  1. Explorer un lieu")
    print("  2. Voir mon état")
    print("  3. Quitter")


# ---------- Actions ----------

def choisir_lieu(lieux):
    """Demande un numéro de lieu et renvoie le lieu choisi, ou None si la saisie est invalide."""
    afficher_lieux(lieux)
    choix = input("Quel lieu ? (numéro) : ")

    if not choix.isdigit():
        print("Il faut taper un numéro.")
        return None

    numero = int(choix)
    if numero < 1 or numero > len(lieux):
        print("Ce lieu n'existe pas.")
        return None

    return lieux[numero - 1]


def rencontrer(joueur, nom, personnage):
    """Fait parler le personnage. Renvoie True si le joueur peut fouiller le lieu, False sinon."""
    if personnage["deja_rencontre"]:
        print(f"{nom} te salue de loin.")
        return True

    print(f"{nom} : « {personnage['dialogue']} »")

    if personnage["type"] == "allie":
        for ressource, quantite in personnage["cadeau"].items():
            joueur["ressources"][ressource] = joueur["ressources"][ressource] + quantite
            print(f"{nom} te donne {quantite} {ressource}.")
        personnage["deja_rencontre"] = True
        return True

    reponse = input(personnage["question"] + " ")
    if reponse.strip() == personnage["reponse"]:
        print(f"Bonne réponse ! {nom} te laisse passer.")
        personnage["deja_rencontre"] = True
        return True

    print(f"Mauvaise réponse ! {nom} te chasse. Tu perds 2 points d'énergie.")
    joueur["energie"] = joueur["energie"] - 2
    return False


def explorer(joueur, lieu, personnages):
    """Retire 1 d'énergie, affiche le lieu, fait parler son personnage, puis donne la ressource."""
    joueur["energie"] = joueur["energie"] - 1
    print(f"Tu arrives à {lieu['nom']}.")
    print(lieu["description"])

    if lieu["personnage"] is not None:
        nom = lieu["personnage"]
        passage = rencontrer(joueur, nom, personnages[nom])
        if not passage:
            print("Tu repars sans rien prendre.")
            return

    if lieu["quantite"] > 0:
        ressource = lieu["ressource"]
        joueur["ressources"][ressource] = joueur["ressources"][ressource] + lieu["quantite"]
        print(f"Tu trouves {lieu['quantite']} {ressource} !")
        lieu["quantite"] = 0
    else:
        print("Tu as déjà fouillé ce lieu, il n'y a plus rien.")


# ---------- Fin de partie ----------

def a_gagne(joueur, objectif):
    """Renvoie True si le joueur a au moins la quantité demandée pour chaque ressource."""
    for ressource in objectif:
        if joueur["ressources"][ressource] < objectif[ressource]:
            return False
    return True


def a_perdu(joueur):
    """Renvoie True si le joueur n'a plus d'énergie."""
    return joueur["energie"] <= 0


# ---------- Boucle de jeu ----------

def jouer(donnees):
    """Fait tourner le jeu jusqu'à ce que le joueur choisisse de quitter."""
    joueur = donnees["joueur"]
    lieux = donnees["lieux"]
    personnages = donnees["personnages"]

    print("Bienvenue dans les Cités Perdues !")
    afficher_etat(joueur)

    tour = 1
    en_cours = True
    while en_cours:
        afficher_menu(tour)
        choix = input("Ton choix : ")

        if choix == "1":
            lieu = choisir_lieu(lieux)
            if lieu is not None:
                explorer(joueur, lieu, personnages)
        elif choix == "2":
            afficher_etat(joueur)
            afficher_objectif(joueur, donnees["objectif"])
        elif choix == "3":
            print("À bientôt, explorateur !")
            en_cours = False
        else:
            print("Choix invalide, tape 1, 2 ou 3.")

        if a_gagne(joueur, donnees["objectif"]):
            print()
            print("Tu as réuni toutes les ressources : la cité reprend vie. Victoire !")
            afficher_etat(joueur)
            en_cours = False
        elif a_perdu(joueur):
            print()
            print("Tu n'as plus d'énergie. La cité restera perdue... Défaite.")
            en_cours = False

        tour = tour + 1


# ---------- Programme principal ----------

data = charger_donnees("donnees.json")
jouer(data)