# argent.py
argent = 100  # Montant initial d'argent

# Fonction pour obtenir la quantité d'argent actuelle
def get_argent():
    return argent

# Fonction pour ajouter de l'argent
def ajouter_argent(montant):
    global argent
    argent += montant
    print(f"Ajouté {montant}$, Argent actuel: {argent}$")  # Ajout d'un print pour le débogage

# Fonction pour retirer de l'argent
def retirer_argent(montant):
    global argent
    if argent >= montant:
        argent -= montant
        print(f"Retiré {montant}$, Argent actuel: {argent}$")  # Ajout d'un print pour le débogage
    else:
        print("Pas assez d'argent.")
