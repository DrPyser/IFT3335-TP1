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
Particulièrement, il s'agit d'une assignation d'un chiffre entre 0 et 9(inclusif) pour chaque case
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
[`SudokuProblem`](problem1.py) sous-classant la classe [`Problem`](search.py) de la librarie `aima-python`.
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

Pour la deuxième formulation(inspirée de l'article de Lewis), l'état initiale est une configuration pleine(ou chaque case à une valeur entre 1 et 9)
tel que chaque bloc contient tous les chiffres de 1 à 9. Un sous-ensemble des cases sont considérée comme fixe et ne seront pas touchée lors de la recherche. Un état but correspond à une grille de jeu qui réponds aux contraintes d'une solution d'un sudoku, ou de manière équivalente, une grille de jeu ayant une valeur de 0 dans cette formulation.
La valeur d'un état est calculée en comptant le nombre de valeurs manquantes pour chaque ligne et colonne.





