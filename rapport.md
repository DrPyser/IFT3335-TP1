---
author:
    - Charles Langlois
    - Yan Coutu
date: 17 mars 2017
title: Rapport: TP1 IFT3335
---

# Modélisation du problème
## État

Un état est ici une certaine configuration d'une grille de Sudoku 9 par 9.
Particulièrement, il s'agit d'une assignation d'un chiffre entre 0 et 9 (inclusif) pour chaque case
d'une matrice 9 par 9. 
Le chiffre 0 représente les cases "vide", soit dont une valeur n'a pas encore été assignée.
Pour les algorithmes de profondeur d'abord et de meilleur d'abord vorace, l'état peut effectivement contenir
des cases vides. Celles-ci se verront assignées une valeur valide(i.e. respectant les contraintes du jeu) au cours de la
recherche.
Pour les algorithmes de type "Hill Climbing" et de recuit simulé("Simulated Annealing"), 
les états seront toujours complètement remplis(i.e. aucune case vide, ayant une valeur de 0), 
mais certains états ainsi générés seront invalides(i.e. certaines cases ne respecteront pas les contraintes du jeu).
Ces états seront donc strictement intermédiaires et pourront servir de passage vers un état valide(i.e. une solution).
Concrètement, ce modèle d'état est implémenté dans le langage `Python` avec l'aide d'une classe([`Sudoku`](sudoku.py)) contenant
("enveloppant") une liste de liste(attribut d'instance `sudoku`), 
correspondant à une liste des lignes (chaque ligne contenant neuf chiffres entre 0 et 9)
de la grille du Sudoku. 
De plus, la classe contient une liste de pair d'entiers(attribut d'instance `fixed`) représentant la position dans la matrice d'une case
dont la valeur est fixe, c'est-à-dire inchangeable
(i.e. une pair `(i,j)` indique la case d'une instance de cette classe `sudoku_instance.sudoku[i][j]`).
Les méthodes appropriées sont implémentées pour permettre un accès facile à une ligne,
une colonne, une case ou un "bloc"(i.e. une sous-grille 3 par 3) de la grille. De plus, les méthodes appropriées pour vérifier
si la grille est remplie(aucune valeurs 0), pour générer les valeurs possibles(respectant les contraintes) pour une case,
pour générer un nouvelle état en modifiant la valeur d'une case et tout autre comportement utile dans l'implémentation utile des algorithmes
sont aussi présents dans cette classe.


## Problème
La formulation du problème, incluant la définition d'un état initial, d'un état but, des actions possibles dépend de 
l'algorithme utilisé.
En particulier, il existe deux formulations différentes du problème, une utilisée pour les algorithmes profondeur d'abord
et meilleur d'abord vorace(voir [SudokuProblem](problem1.py)), et l'autre utilisée pour 
les algorithmes de type "Hill Climbing" et recuit simulé(voir [`LewisSudokuProblem`](problem2.py)). 

Pour la première formulation, l'état initiale correspond à une grille de jeu(instance de la classe `Sudoku`) partiellement remplis
(i.e. avec certaines cases ayant la valeur 0). Les valeurs données initialement sont considérées comme fixe pour cet état et tous les états
subséquents.
Un état but correspond à une grille remplis, soit sans cases de valeur 0, et pour laquelle toutes les cases sont valides, 
c'est-à-dire qu'elles respectent toutes les contraintes du jeu, soit que la valeur d'une case soit unique pour la ligne, la colonne et le bloc.
La relation "successeur" associe à chaque état tous les états subséquents possibles(i.e. conservant la validité du jeu), 
soit chaque état produite par l'assignation à une case vide d'une valeur entre 1 et 9 pas déjà présente dans la même rangée, colonne ou bloc.
Pour cette formulation du problème, on fait l'hypothèse d'un coût uniforme constant de 1 pour tout changement d'état.
Pour implémenter cette formulation du problème, on défini les méthodes `actions`, `result` et `goal_test` dans la classe
[`SudokuProblem`](problem.py) sous-classant la classe [`Problem`](search.py) de la librarie `aima-python`.
La méthode `actions` d'une instance de la classe `SudokuProblem` appelée sur un état 
retourne un itérateur générant des triplets `(i,j,v)` représentant le changement d'état correspondant
à l'assignation d'une valeur `v` à la case `(i,j)` de la grille de jeu de l'état passée en paramètre. 
Seul les triplets représentant une assignation *valide*, c'est-à-dire respectant les contraintes du jeu par rapport à 
l'état considérée, seront générés.
La méthode `result` interprète une telle action en retournant l'état générée par l'application de l'action sur un état.
Il est assumé que l'action est effectivement une action valide pour cet état,
tel qu'elle serait générée par un appel de `actions` sur cet état.
La méthode `goal_test` vérifie si l'état en paramètre constitue un état final et une solution au Sudoku, c'est-à-dire
que la grille de jeu est remplis et que chaque case contient une valeur entre 1 et 9 unique dans sa ligne, colonne et bloc.
Finalement, la méthode `value` assigne une valeur à l'état, correspondant à la somme du nombre de chiffres manquants pour chaque colonne, 
rangée ou bloc de la grille.

Pour la deuxième formulation(inspirée de l'article de Lewis), l'état initiale est une configuration pleine(ou chaque case à une valeur entre 1 et 9)
tel que chaque bloc contient tous les chiffres de 1 à 9. Un sous-ensemble des cases sont considérée comme fixe et ne seront pas touchée lors de la recherche. Un état but correspond à une grille de jeu qui réponds aux contraintes d'une solution d'un sudoku, ou de manière équivalente, une grille de jeu ayant une valeur de 0 dans cette formulation.
La valeur d'un état est calculée en comptant le nombre de valeurs manquantes pour chaque ligne et colonne. Une action consiste en une paire de cases telle que les deux cases se trouvent dans le même carré et ne sont pas des cases fixes, c'est-à-dire des cases du problème.
La méthode `actions` d'une instance de la classe `SudokuProblem` appelé sur un état retourne une paire de paire représentant les deux paires à permuter.
La méthode `goal_test` vérifie si la valeur de la grille est à 0, c'est-à-dire si aucun chiffre ne se répète dans chaque ligne et dans chaque colonne (par construction, tous les chiffres dans chaque carré est différent).

# Heuristiques pour meilleur d'abord
Il y a trois heuristiques définies pour le meilleur d'abord: `h1`, `h2`, `h3`.
`h1` est la plus simple et regarde le nombre de possibilités pour la case associée à l'action ayant générée l'état.
Ainsi, les cases ayant peu de valeurs possibles vont être remplies en premier. 
Ici, "valeur possible" signifie une valeur entre 1 et 9 pour une case tel que

1. assigner cette valeur à cette case ne viole pas les contraintes du jeu(valeur unique pour la ligne, colonne et bloc).
2. si une valeur ne peut être placer dans aucunes des autres cases de la colonne, rangée ou bloc sans violer les contraintes,
   cette valeur est effectivement la seule valeur possible pour cette case.
   
L'heuristique `h2` est un peu plus intelligente puisqu'elle regarde aussi les autres cases de la grille de ce noeud pour trouver
des cases qui n'ont aucunes valeurs possibles. Ces états sont évidemment des cul-de-sac et n'ont aucune valeur. 
L'heuristique va donc retourner la valeur `None` pour indiquer à l'algorithme de recherche d'ignorer le sous-arbre correspondant à cet état.

# Fonctionnement du programme
Le programme à exécuter porte le nom de [`main.py`](main.py).
Le programme prend en argument un string correspondant à un algorithme de recherche à exécuter sur les 100 exemples du fichier [`100sudoku.txt`](100sudoky.txt).
Les choix possibles sont: 
* `"depth_first"`
* `"best_first_h1"` : algorithme meilleur d'abord *complet*(explorant toutes les solutions potentielles) avec l'heuristique `h1`.
* `"best_first_h2"` : algorithme meilleur d'abord *complet*(explorant toutes les solutions potentielles) avec l'heuristique `h2`.
* `"best_first_greedy_h1"` : algorithme meilleur d'abord *partiel*(explorant seulement le meilleur noeud à chaque étage, comme le *hill climbing*) avec l'heuristique `h1`.
* `"best_first_greedy_h2"` : algorithme meilleur d'abord *partiel*(explorant seulement le meilleur noeud à chaque étage, comme le *hill climbing*) avec l'heuristique `h2`.
* `"hill_climbing"` : algorithme de *hill climbing*.
* `"annealing"` : algorithme de recuit simulé.

Un exemple d'exécution d'une recherche:

`python3 main.py "depth_first"`

Le programme imprime sur la sortie standard des informations sur le résultat de chaque sudoku, en format `csv`, en commençant par le *header*:
`problem,searcher,explored,states,tests,solution,value`
"problem" est un numéro entre 0 et 99 indiquant le problème évalué. "searcher" est l'argument fourni au programme indiquant l'algorithme de recher utilisé. "explored" correspond au nombre d'états *explorés*, correspondant au nombre d'appel de la méthode `actions`. "states" correspond au nombre d'états générés(i.e. le nombre d'appel de la méthode `result`). "tests" correspond au nombre de d'appels de la méthode `goal_test`. "solution" est un booléen indiquant si une *vraie* solution a été trouvée("True"/"False"). Finalement, "value" correspond à la valeur donnée par la méthode `value` au résultat de la recherche.

# Analyse des algorithmes
L'algorithme de recherche par profondeur est très inefficace. Un seul sudoku prend plusieurs heures pour terminer. En contrepartie, nous savons qu'il arrive à une solution éventuellement. Il n'y a donc évidemment aucun résultat pour la recherche par profondeur.
L'algorithme best-first utilisé avec une heuristique priorisant les cases le moins de chiffres possibles en ne regardant que les cases remplies est aussi inefficace. Bien que le temps est, en théorie, meilleur, cela prend encore plusieurs heures pour arriver à une solution. Nous n'avons donc aucun résultat pour cet algorithme. Par contre, il aurait été possible d'améliorer l'heuristique en comptant le nombre de possibilités de manière plus exhaustive. Par exemple, en considérant les chiffres qui n'apparaissent qu'une fois dans une ligne, une colonne ou un carré, ou bien avec des techniques plus complexes : si l'union des chiffres possibles de n cases d'une ligne (ou d'une colonne ou d'un carré) est un ensemble de cardinal n, alors on peut éliminer ces possibilités dans les autres cases de la ligne (ou de la colonne ou du carré).

Le Hill Climbing réussit à réduire le cout, mais n'est pas capable de trouver une solution finale valide. En effet, sur les 100 sudokus, aucun sudoku n'a été résolu. Le cout moyen est de 13.54 et l'algorithme parcourait en moyenne 17.22 noeuds avant d'arriver à la solution

Pour le Recuit Simulé, la température suit une loi exponentielle, où la température initiale est de 80% et qui descend par un coefficient de 0.99 à chaque itération. Comme l'algorithme est très long, il a été décidé d'arrêter les itérations lorsque la température est descend en bas de 1%. Tout comme le Hill Climbing, il ne trouve pas de solution, mais donne de meilleures résultats, malgré un temps de calcul très long. En moyenne, le score s'approche de 10.58 et l'algorithme parcourt 437 noeuds. Notons que si on n'arrêtait pas l'algorithme prématurément, il est certain qu'il trouverait la solution, mais cela requiert beaucoup de temps de calcul.