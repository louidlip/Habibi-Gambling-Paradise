README.md

Membres du groupe :
Garotta Hugo (code et musique)
Kimpfler Jakob (code et auteur de l'histoire)
Kirsten Fynn (code et co auteur de l'histoire et co designer)
Lipuma Louis (code et designer)

Projet : Jeu de Casino avec différentes activités ( roulette, machine à sou, dés etc...)
Écran titre avec des onglet "start game", "settings" et "quit game".

Utilisation de pygame pour programmer le jeu

Lobby pour séléctionner les différents jeux et une option tutoriel et un shop avec des cosmétiques:
![image](https://github.com/user-attachments/assets/86159d56-1140-4f99-b8bd-22f68a9b1e46)






Differents minigames accecible du lobby:

![image](https://github.com/user-attachments/assets/53611c28-d83c-4e16-8e5c-5784f9f06323)
![image](https://github.com/user-attachments/assets/013a617f-8e52-4cfd-adb5-5759c973f132)
![image](https://github.com/user-attachments/assets/19413771-7c15-45ff-807b-0cc91769f5a1)
![image](https://github.com/user-attachments/assets/272cd0ce-3ff6-4fdc-b063-ab3fee4bc827)



# Cahier des Charges du Jeu de Casino

## Membres du groupe :
- **Garotta Hugo** : Code et musique
- **Kimpfler Jakob** : Code et auteur de l'histoire
- **Kirsten Fynn** : Code, co-auteur de l'histoire, et co-designer
- **Lipuma Louis** : Code et designer

## Projet : **Jeu de Casino avec différentes activités**

### 1. **Objectif du projet :**
Développer un jeu de casino comprenant plusieurs mini-jeux populaires : 
- Roulette
- Machine à sous
- Dés
- Black Jack

Le jeu sera conçu à l'aide de **Pygame**, une bibliothèque Python permettant de créer des jeux 2D interactifs.

### 2. **Fonctionnalités principales :**

#### a. **Écran titre** :
L'écran titre du jeu comportera les onglets suivants :
- **Start Game** : Démarre le jeu.
- **Settings** : Permet de modifier les paramètres du jeu, tels que le volume de la musique, les options graphiques et la difficulté.
- **Quit Game** : Quitte le jeu.

#### b. **Lobby principal** :
Une fois le jeu démarré, l'utilisateur accède à un lobby où il peut choisir parmi les différents jeux de casino proposés :
- Roulette
- Machine à sous
- Dés
- Black Jack

Le lobby comprendra également les options suivantes :
- **Tutoriel** : Explications et instructions sur les différents jeux disponibles.
- **Shop** : Un magasin où les joueurs peuvent acheter des cosmétiques pour personnaliser leur expérience de jeu (par exemple, skins, fonds d'écran, effets sonores).

#### c. **Jeux disponibles** :
1. **Roulette** : Jeu classique de casino où les joueurs parient sur la couleur, le numéro, ou le groupe de numéros sur lesquels la balle va atterrir.
2. **Machine à sous** : Un jeu de machine à sous avec des rouleaux et des symboles variés. Le but est d’aligner des symboles similaires pour remporter des gains.
3. **Dés** : Un jeu où les joueurs lancent des dés et parient sur le résultat.
4. **Black Jack** : Jeu de cartes où le but est d’avoir une main dont la somme des valeurs est la plus proche de 21 sans la dépasser.

#### d. **Menu et interface** :
- **Graphismes** : Des éléments graphiques simples et efficaces, adaptés à l’univers du casino.
- **Sons et musique** : Musique de fond adaptée à l'ambiance du casino, avec des effets sonores pour chaque action dans les jeux (exemple : bruit de la roulette, bruit des cartes, etc.).

#### e. **Éléments du Shop** :
Le shop proposera des cosmétiques tels que :
- **Skins pour les tables de jeux** (par exemple, table de roulette en bois ou en marbre).
- **Cartes personnalisées** pour le Black Jack.
- **Effets visuels** comme des animations supplémentaires lors des gains ou pertes.
- **Musique et effets sonores** supplémentaires à acheter.

#### f. **Tutoriel** :
Un tutoriel interactif guidera le joueur à travers les règles et les mécanismes de chaque jeu. Ce tutoriel sera disponible depuis le lobby, et le joueur pourra le consulter à tout moment.

### 3. **Technologies utilisées :**
- **Pygame** : Pour la création du jeu 2D et la gestion des interactions utilisateur (graphismes, sons, entrées).
- **Python** : Langage de programmation principal.
- **Bibliothèques supplémentaires** (si nécessaire) : Pour les sons, animations, gestion des fichiers de configuration, etc.

### 4. **Tâches et responsabilités :**

- **Garotta Hugo** : Développement du code pour la gestion de la musique et des sons, ainsi que le développement d'éléments liés à l'interface.
- **Kimpfler Jakob** : Création de l'histoire du jeu et du code de base pour les différentes mécaniques de jeux (roulette, blackjack, etc.).
- **Kirsten Fynn** : Co-auteur de l’histoire, co-designer des éléments visuels et programmation des interactions dans les jeux.
- **Lipuma Louis** : Design des éléments visuels et création des différentes interfaces et animations des jeux.

### 5. **Planification** :

| **Phase**                | **Description**                                               | **Durée estimée** |
|--------------------------|---------------------------------------------------------------|-------------------|
| **Phase de planification** | Définir le gameplay, les jeux à inclure, et les fonctionnalités | 1 semaine         |
| **Développement de base**  | Mise en place de l'interface, menu principal, et lobby        | 2 semaines        |
| **Création des jeux**     | Développement des mini-jeux (roulette, machine à sous, etc.)  | 3 semaines        |
| **Intégration du shop**   | Développement du magasin et des cosmétiques                   | 2 semaines        |
| **Test et ajustements**   | Test complet du jeu, ajustements des bugs et équilibrage      | 1 semaine         |
| **Finalisation et release** | Préparation pour la sortie et ajustements finaux             | 1 semaine         |

### 6. **Livrables** :
- Code source complet du jeu
- Fichiers graphiques et sonores utilisés dans le jeu
- Documentation du code et des mécanismes de jeu
- Version finale du jeu prête à être jouée

### 7. **Besoins en matériel et logiciels** :
- **Matériel** : Ordinateurs personnels pour chaque membre de l'équipe.
- **Logiciels** : Python 3.x, Pygame, un éditeur de texte (par exemple VSCode ou PyCharm), un logiciel de création graphique (comme GIMP ou Photoshop), un éditeur de musique (comme FL Studio ou Audacity).

### 8. **Évaluation** :
À la fin du projet, le jeu sera évalué sur les critères suivants :
- **Performance** : Le jeu doit fonctionner sans lag et être fluide sur des systèmes standards.
- **Jouabilité** : Les mécaniques de jeu doivent être équilibrées et divertissantes.
- **Design** : L’interface et les éléments visuels doivent être cohérents avec le thème du casino.
- **Innovation** : L’ajout de fonctionnalités originales, comme le shop de cosmétiques, sera pris en compte.

---

Ce cahier des charges définit les attentes et les responsabilités de chaque membre du groupe pour mener à bien ce projet de jeu de casino.
