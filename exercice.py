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


joueur = data["joueur"]
lieux = data["lieux"]
objectif = data["objectif"]


afficher_etat(joueur)
afficher_lieux(lieux)
afficher_objectif(joueur, objectif)