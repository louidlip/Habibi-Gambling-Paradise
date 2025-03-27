argent = 100  # Montant initial d'argent

# Fonction pour obtenir la quantité d'argent actuelle
def get_argent():
    return argent

# Fonction pour ajouter de l'argent
def ajouter_argent(montant):
    global argent
    argent += montant

# Fonction pour retirer de l'argent
def retirer_argent(montant):
    global argent
    if argent >= montant:
        argent -= montant
    else:
        print("Pas assez d'argent.")
