import expyriment
from expyriment import design, control, stimuli, io, misc
import random

############### INITIALISATION DE L'EXPERIENCE #################
exp = design.Experiment("Projet PCBS: information crossing hemispheres")
control.initialize(exp)
user_device = exp.keyboard # Créer la classe du périphérique de saisie

##################### INITIALISATION DES PARAMETRES #####################
# (Permet de modifier facilement le design expérimental si nécessaire)

key_m = 59
key_q = 97
response_keys = [key_m, key_q]

n_trial = 5 # Nombre de trials par bloc
fixcross = stimuli.FixCross(size=(20, 20), line_width = 3) #Croix de fixation
fixcross.preload()
Blackscreen = stimuli.BlankScreen()

# Paramètres d'affichage du stimulus:
square_dist = 200
square_size = [20, 20]

# Paramètre de réponses: appuyer sur "M" si stimulus à droite / "Q" si stimulus à gauche
trial_left = ["left", key_q, -square_dist, 0]
trial_right = ["right", key_m, square_dist, 0]

square_wait = 100 # Durée d'affichage du stimulus
wait_duration = 1000 # Durée d'attente post-stimulus pour saisie utilisateur

##################### INSTRUCTIONS #####################

instructions = """Dans l'expérience suivante, un carré gris va apparaître dans la partie droite ou gauche de votre champ visuel,
de part et d'autre d'une croix centrale.
Vous devez fixer la croix pendant toute la durée de l'essai.
Appuyez sur la touche "M" si le carré apparaît à droite de la croix, et sur "Q" s'il apparaît à gauche.

Appuyez sur n'importe quelle touche pour continuer."""

instruction1 = "Veuillez positionner votre index droit sur la touche \"m\" et votre index gauche sur la touche \"q\" puis taper sur n'importe quelle touche pour commencer"
instruction2 = "Veuillez positionner votre index gauche sur la touche \"m\" et votre index droit sur la touche \"q\", votre bras droit étant placé au-dessus de votre bras gauche, puis taper sur n'importe quelle touche pour commencer"
instruction3 = "Veuillez positionner votre index gauche sur la touche \"m\" et votre index droit sur la touche \"q\", votre bras gauche étant placé au-dessus de votre bras droit puis taper sur n'importe quelle touche pour commencer"
instructions_total = [instruction1, instruction2, instruction3]

##################### CREATION DES BLOCS D'EXPERIMENTATION #####################

for nblock in ["Bloc 1", "Bloc 2", "Bloc 3"]:
	b = design.Block()
	b.set_factor("Numéro du bloc", nblock)

# Définition du nombre de tirages par côté (au moins 1 de chaque côté)
	trial_left[3] = int(n_trial/2)
	trial_right[3] = n_trial - trial_left[3]

# Création des stimuli carrés "gauche" et "droite"
	for where in [trial_left, trial_right]:
			t = design.Trial()
			t.set_factor("Position", where[0])
			t.set_factor("Expected", where[1])
			s = stimuli.Rectangle(square_size, position=[where[2], 0])
			t.add_stimulus(s)

			b.add_trial(t, copies=where[3])
	b.shuffle_trials()

	exp.add_block(b) # Ajout du bloc à l'expérience

# Variables d’expérimentation à conserver: numéro de bloc, position du stimulus, saisie clavier attendue,saisie de l’utilisateur, temps de réaction
exp.data_variable_names = ["Bloc", "Position", "Expected", "Button", "RT"]

##################### DEBUT DE L'EXPERIENCE #####################

control.start()

stimuli.TextScreen("Instructions", instructions).present() # instructions générales
user_device.wait()
# Enchaînement des trois blocs
j = 0
for block in exp.blocks:
	stimuli.TextScreen("Instructions", instructions_total[j] ).present() # instructions spécifiques
	j += 1
	user_device.wait()

	for trial in block.trials:
		show_time = random.randint(1000, 1800) # temps d'affichage de la croix de fixation avant présentation du stimulus
		fixcross.present()
		exp.clock.wait(show_time)

		trial.stimuli[0].present() #affichage du stimulus
		exp.clock.wait(square_wait)
		Blackscreen.present()

		button, rt = user_device.wait(keys = response_keys, duration = wait_duration)

# Enregistrement des données obtenues:
		exp.data.add([block.get_factor("Numéro du bloc"), show_time, trial.get_factor("Position"), trial.get_factor("Expected"), button, rt])

control.end()
