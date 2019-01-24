# Tâche de détection d'un stimulus visuel latéralisé et temps de réaction ipsi- et contro-latéral

## Introduction 

L'objectif de ce projet était de créer en Python, une utilisant le module expyriment, une expérience psychophysique permettant d'étudier le temps nécessaire à une information pour traverser les deux hémisphères cérébraux, en étudiant les temps de réaction des mains ipsi- et contro-latérale à un stimulus visuel latéralisé. 

Plus exactement, la tâche consiste en une succession d'essais (100 par bloc) durant lesquels un stimulus (carré gris clair) apparaît soit à droite, soit à gauche du champ visuel du sujet, de part ou d'autre de la croix de fixation centrale. Le sujet doit appuyer sur la touche "M" (située à droite du clavier) si le stimulus apparaît à droite, ou sur "Q" (située à gauche) si le stimulus apparaît à gauche.
L'expérience implique trois conditions: l'une où le sujet utilise la main ipsilatérale au stimulus (il appuie sur les touches gauche et droite respectivement avec les index gauche et droit); et deux où le sujet croise les bras pour utiliser la main controlatérale au stimulus (il appuie sur les touches gauche et droite respectivement avec les index droit et gauche), avec le bras droit au-dessus du gauche puis l'inverse.

Cette expérience est adaptée de l'article "Interhemispheric vs stimulus-response spatial compatibility effects in bimanual reaction times to lateralized visual stimuli" publié dans Frontiers in Psychology en 2013 par Pellicano&al. La différence principale est que, dans l'expérience codée ici, le sujet ne répond que d'une seule main au stimulus (comme précisé dans la description de projet proposée par M. Pallier) alors que dans l'expérience d'origine, il devait appuyer sur les deux touches simultanément, indépendament de la latéralisation du stimulus.

**Tables des Matières**
  * #Tâche de détection d'un stimulus visuel latéralisé et temps de réaction ipsi- et contro-latéral
    * [Préparation des stimuli]
    * [Design expérimental]
    * [Expérience]
    * [Conclusion]

## Préparation des stimuli

 ### Croix de Fixation
La croix de fixation a été formatée et préchargée lors de la phase d'initialisation de l'expérience pour pouvoir être facilement modifiée et éviter d'éventuels temps de chargement lors de l'expérience. Elle a été crée en utilisant le module expyriment.

Par la suite, lors de l'expérience, elle est affichée durant un temps aléatoire compris entre 1000 et 1800ms. 


 ### Stimulus visuel (cible)

Le stimulus visuel utilisé est un carré gris, de 20 pixels de côté, apparaîssant à 200 pixels à droite ou à gauche de la croix de fixation centrale, paramétré grâce au module expyriment. Comme pour la croix, ses caractéristiques sont définies lors de l'initialisation de l'expérience pour pouvoir être facilement modifiées ou adaptées, et il est également préchargé.

## Design expérimental

 ### Création des blocs d'expérimentation

L'expérience est divisée en trois blocs similaires, dont la seule différence est la consigne donnée au sujet avant le début du bloc, concernant la manière dont il doit appuyer sur les touches en réponse aux stimuli.
