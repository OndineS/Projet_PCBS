import expyriment
from expyriment import design, control, stimuli, io, misc
import random

############### INITIALISATION DE L'EXPERIENCE #################

exp = design.Experiment("Projet PCBS: information crossing hemispheres")
control.initialize(exp)
screen_size = exp.screen.surface.get_size()
user_device = exp.keyboard

##################### INITIALISATION DES PARAMETRES #####################

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

instructions = """Dans l'expérience suivante, un carré gris va apparaître dans la partie droite ou gauche de votre champ visuel, \n
de part ou d'autre d'une croix centrale. \n
Vous devez fixer la croix pendant toute la durée de l'essai.\n
Appuyez sur la touche \"M\" si le carré apparaît à droite de la croix, et sur \"Q\" s'il apparaît à gauche.\n

Appuyez sur n'importe quelle touche pour continuer."""

instruction1 = "Veuillez positionner votre index droit sur la touche \"M\" et votre index gauche sur la touche \"Q\" \n Puis appuyez sur n'importe quelle touche pour commencer"
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

		exp.data.add([block.get_factor("Numéro du bloc"), trial.get_factor("Position"), trial.get_factor("Expected"), button, rt]) # Exportation des données obtenues

control.end()
