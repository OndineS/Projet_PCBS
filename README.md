# Tâche de détection d'un stimulus visuel latéralisé et temps de réaction ipsi- et contro-latéral

## Introduction 

L'objectif de ce projet était de créer en Python, en utilisant le module expyriment, une expérience psychophysique permettant d'étudier le temps nécessaire à une information pour traverser les deux hémisphères cérébraux, en étudiant les temps de réaction des mains ipsi- et contro-latérale à un stimulus visuel latéralisé. 

Plus exactement, la tâche consiste en une succession d'essais (100 par bloc) durant lesquels un stimulus (carré gris clair) apparaît soit à droite, soit à gauche du champ visuel du sujet, de part ou d'autre de la croix de fixation centrale. Le sujet doit appuyer sur la touche "M" (située à droite du clavier) si le stimulus apparaît à droite, ou sur "Q" (située à gauche) si le stimulus apparaît à gauche.
L'expérience implique trois conditions: l'une où le sujet utilise la main ipsilatérale au stimulus (il appuie sur les touches gauche et droite respectivement avec les index gauche et droit); et deux où le sujet croise les bras pour utiliser la main controlatérale au stimulus (il appuie sur les touches gauche et droite respectivement avec les index droit et gauche), avec le bras droit au-dessus du gauche puis l'inverse.

Cette expérience est adaptée de l'article "Interhemispheric vs stimulus-response spatial compatibility effects in bimanual reaction times to lateralized visual stimuli" publié dans Frontiers in Psychology en 2013 par Pellicano&al. La différence principale est que, dans l'expérience codée ici, le sujet ne répond que d'une seule main au stimulus (comme précisé dans la description de projet proposée par M. Pallier) alors que dans l'expérience d'origine, il devait appuyer sur les deux touches simultanément, indépendament de la latéralisation du stimulus.

**Tables des Matières**
  * Tâche de détection d'un stimulus visuel latéralisé et temps de réaction ipsi- et contro-latéral
    * [Préparation des stimuli] (#stim)
    	* Croix de fixation (#fix)
        * Stimulus visuel (cible) (#vis)
    * [Design expérimental] (#exp)
    	* Création des trials (#tri)
        * Création des blocs d'expérimentation (#bloc)
        * Exportation des données (#data)
    * [Expérience] (#expt)
    * [Conclusion] (#ccl)

## Préparation des stimuli <a name="stim"></a>

### Croix de Fixation <a name="fix"></a>
La croix de fixation a été formatée et préchargée lors de la phase d'initialisation de l'expérience pour pouvoir être facilement modifiée et éviter d'éventuels temps de chargement lors de l'expérience. Elle a été crée en utilisant le module expyriment.

    fixcross = stimuli.FixCross(size=(20, 20), line_width = 3)
    fixcross.preload()

Par la suite, lors de la présentation de l'expérience, elle est affichée durant un temps aléatoire compris entre 1000 et 1800ms. 

    for trial in block.trials:
		     show_time = random.randint(1000,1800)
		     fixcross.present()
		     exp.clock.wait(show_time)


### Stimulus visuel (cible) <a name="vis"></a>

Le stimulus visuel utilisé est un carré gris, de 20 pixels de côté, apparaîssant à 200 pixels à droite ou à gauche de la croix de fixation centrale. Comme pour la croix, ses caractéristiques sont définies lors de l'initialisation de l'expérience pour pouvoir être facilement modifiées ou adaptées, et il est également préchargé.

	square_dist = 200
	square_size = [20, 20]
	left_square = stimuli.Rectangle(square_size, position=[-square_dist, 0])
	left_square.preload()
	right_square = stimuli.Rectangle(square_size, position=[square_dist, 0])
	right_square.preload()
	square_displaytime = 100

## Design expérimental <a name="exp"></a>

### Création des trials <a name="tri"></a>

Les deux types de trials (stimuli apparaissant au gauche ou à droite) ont également été initialisés en début d'expérience pour plus de fluidité.

	trial_left = ["left", key_q, left_square, 0]
	trial_right = ["right", key_m, right_square, 0]
	
De la même manière, les paramètres de réponse de l'utilisateur ont aussi été pré-programmées.

	key_m = 59
	key_q = 97
	response_keys = [key_m, key_q]
	
Les valeurs assignées à key_m et key_q sont propres à Python, et sont les seules valeurs permettant de conserver la mémoire de la touche appuyée par l'utilisateur dans le fichier d'exportation des données créé en fin d'expérience.

### Création des blocs d'expérimentation <a name="bloc"></a>

L'expérience est divisée en trois blocs similaires, dont la seule différence est la consigne donnée au sujet avant le début de l'expérience, concernant la manière dont il doit appuyer sur les touches en réponse aux stimuli.
Pour faciliter l'exportation des données, chaque bloc est identifié par un numéro de bloc. Par ailleurs, les paramètres principaux du bloc (nombre de trials, définition des stimuli, instructions à afficher) ont été programmés en amont afin qu'ils puissent être modifiés sans perturber le programme, et afin de faciliter la fluidité de la lecture des blocs et leur structuration. Par contre, si le nombre de trials est préprogrammé, le nombre de stimulus présentés à gauche / à droite est calculé à l'intérieur du bloc.

	for nblock in ["Bloc 1", "Bloc 2", "Bloc 3"]:
	b = design.Block()
	b.set_factor("Numéro du bloc", nblock)

	trial_left[3] = int(nb_trial/2)
	trial_right[3] = nb_trial - trial_left[3]

	for where in [trial_left, trial_right]:
			t = design.Trial()
			t.set_factor("Position", where[0])
			t.set_factor("Expected", where[1])
			t.add_stimulus(where[2])

			b.add_trial(t, copies=where[3])
	b.shuffle_trials()

	exp.add_block(b)

### Exportation des données <a name="data"></a>

Les noms des variables à enregistrer à chaque trial ont été définis lors de la création des blocs d'expérimentation.

	exp.data_variable_names = ["Bloc", "Position", "Expected", "Button", "RT"]
	
A chaque trials, les données de ces variables sont enregistrées, et à la fin de l'expérience, un fichier .xpd contenant toutes les valeurs de ces variables pour tous les trials est exporté dans un dossier "data" créé au même emplacement que celui du programme expérimental.

	exp.data.add([block.get_factor("Numéro du bloc"), trial.get_factor("Position"), trial.get_factor("Expected"), button, rt])
	
## Expérience <a name="expt"></a>

Le script pour faire fonctionner l'expérience utilise le module expyriment.

	import expyriment
	from expyriment import design, control, stimuli, io, misc
	import random

	############### INITIALISATION DE L'EXPERIENCE #################

	exp = design.Experiment("Projet PCBS: information crossing hemispheres")
	control.initialize(exp)
	screen_size = exp.screen.surface.get_size()
	user_device = exp.keyboard

	##################### INITIALISATION DES PARAMETRES #####################
	# (Permet de modifier facilement le design expérimental si nécessaire)

	key_m = 59
	key_q = 97
	response_keys = [key_m, key_q]

	nb_trial = 5
	fixcross = stimuli.FixCross(size=(20, 20), line_width = 3)
	fixcross.preload()
	Blankscreen = stimuli.BlankScreen()

	# Paramètres d'affichage du stimulus:
	square_dist = 200
	square_size = [20, 20]
	left_square = stimuli.Rectangle(square_size, position=[-square_dist, 0])
	left_square.preload()
	right_square = stimuli.Rectangle(square_size, position=[square_dist, 0])
	right_square.preload()
	square_displaytime = 100

	# Définition des stimuli et paramètres de réponse utilisateur
	trial_left = ["left", key_q, left_square, 0]
	trial_right = ["right", key_m, right_square, 0]

	wait_duration = 1000

	##################### INSTRUCTIONS #####################

	instructions = """Dans l'expérience suivante, un carré gris va apparaître dans la partie droite ou gauche de votre champ 		visuel,\n
	de part ou d'autre d'une croix centrale. \n
	Vous devez fixer la croix pendant toute la durée de l'essai.\n
	Appuyez sur la touche \"M\" si le carré apparaît à droite de la croix, et sur \"Q\" s'il apparaît à gauche.\n

	Appuyez sur n'importe quelle touche pour continuer."""

	instruction1 = "Veuillez positionner votre index droit sur la touche \"M\" et votre index gauche sur la touche \"Q\" \n Puis 		appuyez sur n'importe quelle touche pour commencer"
	instruction2 = "Veuillez positionner votre index gauche sur la touche \"M\" et votre index droit sur la touche \"Q\",
	Votre bras droit étant placé au-dessus de votre bras gauche, \n
	Puis appuyez sur n'importe quelle touche pour commencer"
	instruction3 = "Veuillez positionner votre index gauche sur la touche \"M\" et votre index droit sur la touche \"Q\", \n
	Votre bras gauche étant placé au-dessus de votre bras droit, \n
	Puis appuyez sur n'importe quelle touche pour commencer"
	instructions_total = [instruction1, instruction2, instruction3]

	##################### CREATION DES BLOCS D'EXPERIMENTATION #####################

	for nblock in ["Bloc 1", "Bloc 2", "Bloc 3"]:
		b = design.Block()
		b.set_factor("Numéro du bloc", nblock)

		trial_left[3] = int(nb_trial/2)
		trial_right[3] = nb_trial - trial_left[3]

		for where in [trial_left, trial_right]:
			t = design.Trial()
			t.set_factor("Position", where[0])
			t.set_factor("Expected", where[1])
			t.add_stimulus(where[2])

			b.add_trial(t, copies=where[3])
		b.shuffle_trials()

		exp.add_block(b)

	exp.data_variable_names = ["Bloc", "Position", "Expected", "Button", "RT"] # Variables à enregistrer à chaque essai

	##################### PRESENTATION DE L'EXPERIENCE #####################

	control.start()

	stimuli.TextScreen("Instructions", instructions).present()
	user_device.wait()

	block_index = 0
	for block in exp.blocks:
		stimuli.TextScreen("Instructions", instructions_total[block_index] ).present()
		block_index += 1
		user_device.wait()

		for trial in block.trials:
			show_time = random.randint(1000,1800)
			fixcross.present()
			exp.clock.wait(show_time)

			trial.stimuli[0].present()
			exp.clock.wait(square_displaytime)
			Blankscreen.present()

			button, rt = user_device.wait(keys = response_keys, duration = wait_duration)

			exp.data.add([block.get_factor("Numéro du bloc"), trial.get_factor("Position"), trial.get_factor("Expected"), 				button, rt]) # Exportation des données obtenues

	control.end()

## Conclusion <a name="ccl"></a>

Avant de commencer le cours, je n'avais pas la moindre connaissance en programmation informatique. Mon dernier contact avec la logique algorithmique remontait au lycée, au temps où nous écrivions des programmes de 10 lignes sur nos calculatrices Casio T35+ (une belle époque...). Il a donc fallu tout découvrir et tout assimiler, car pour moi, un python n'était rien d'autre qu'un nom vernaculaire désignant plusieurs espèces de serpents. Il est ainsi difficile de décrire en quelques lignes ce que j'ai appris durant cette UE: il me faudrait pour cela lister l'intégralité de ce que nous avons vu en cours, et tout ce que vous pouvez voir dans le contenu de ce projet.
De plus, le début du semestre a été un peu difficile, car je n'ai pas pu suivre l'intégralité des cours de mise à niveau du mois de rentrée à cause de problèmes personnels, j'ai donc perdu énormément de temps à essayer de rattraper les fondamentaux que je n'avais pas, d'où mon manque d'activité en cours. Qui plus est, je dois apprendre Matlab pour mon stage du second semestre, j'ai donc d'abord songé à rendre le projet d'AE en Matlab pour m'entraîner, et j'ai commencé à suivre des openclassrooms, mais je n'ai pas eu assez de temps pour atteindre un niveau suffisant pour réaliser un programme complet.

J'ai apprécié la structure des cours, et j'ai trouvé le système de slack très utile, mais pas optimisé, à plusieurs titres:
- beaucoup de choses dans le channel #général, et donc, finalement, pas une grande structuration de la plateforme pourtant très bien conçue à cet égard
- finalement assez peu d'utilisation de la part des étudiants MAIS cela s'explique par un grand problème du Cogmaster: l'interminable multiplication des plateformes de communication. Entre nos adresses mails, les intranets des différentes écoles / universités où nous prenons des cours, Schoology, les sites personnels de certains professeurs et/ou leurs dropbox, Slack... Tout est beaucoup trop dispersé pour que nous puissions tirer profit de toutes ces plateformes. Et cela finit par nuir à la bonne transmission des informations, car on ne sait plus trop où donner de la tête.

J'aurais aimé pouvoir coder l'analyse des résultats de l'expérience réalisée dans ce projet et de les ploter, mais hélas, je n'en ai pas eu le temps.
