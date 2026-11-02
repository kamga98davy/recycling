import json

def telechargement(chemin_fichier):
    """
    Télécharge le contenu d'un fichier JSON et le retourne sous forme de dictionnaire.

    Args:
        chemin_fichier (str): Le chemin vers le fichier JSON à télécharger.

    Returns:
        dict: Le contenu du fichier JSON sous forme de dictionnaire.
    """
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = json.load(fichier)
    return contenu

data = telechargement('donnees.json')

def afficher_etat(joueur):
    print("==============================")
    print(f"{joueur['nom']} | Énergie : {joueur['energie']}")
    print("Ressources :")
    for ressource, quantite in joueur["ressources"].items():
        print(f"  - {ressource} : {quantite}")
    print("==============================")

def afficher_lieux(lieux):
    print("Lieux à explorer :")
    numero = 1
    for lieu in lieux:
        print(f"  {numero}. {lieu['nom']}")
        numero = numero + 1

def afficher_objectif(joueur,objectif):
    for ressource in joueur["ressources"].keys():
        print(f"{ressource} : {joueur['ressources'][ressource]} / {objectif[ressource]}")

def afficher_menu():
    print()
    print("Que veux-tu faire ?")
    print("  1. Explorer un lieu")
    print("  2. Voir mon état")
    print("  3. Quitter")

def jouer(donnees):
    joueur = donnees["joueur"]
    lieux = donnees["lieux"]

    print("Bienvenue dans les Cités Perdues !")
    afficher_etat(joueur)

    en_cours = True
    while en_cours:
        afficher_menu()
        choix = input("Ton choix : ")

        if choix == "1":
            afficher_lieux(lieux)
            print("(L'exploration arrive à l'étape 4.)")
        elif choix == "2":
            afficher_etat(joueur)
            afficher_objectif(joueur, donnees["objectif"])
        elif choix == "3":
            print("À bientôt, explorateur !")
            en_cours = False
        else:
            print("Choix invalide, tape 1, 2 ou 3.")

joueur = data["joueur"]
lieux = data["lieux"]
objectif = data["objectif"]


afficher_etat(joueur)
afficher_lieux(lieux)
afficher_objectif(joueur, objectif)
jouer(data)