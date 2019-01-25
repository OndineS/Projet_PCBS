import expyriment
from expyriment import design, control, stimuli, io, misc
import random

############### INITIALISATION DE L'EXPERIENCE #################

exp = design.Experiment("Projet PCBS: information crossing hemispheres - bimanual")
control.initialize(exp)
screen_size = exp.screen.surface.get_size()
user_device = exp.keyboard

##################### INITIALISATION DES PARAMETRES #####################

key_m = 59
key_q = 97
response_keys = [key_m, key_q]

nb_trial = 100
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

instructions = """Dans l'expérience suivante, un carré gris va apparaître dans la partie droite ou gauche de votre champ visuel, \n\
de part ou d'autre d'une croix centrale. \n\
Vous devez fixer la croix pendant toute la durée de l'essai.\n\
Appuyez simultanément sur les touches \"M\" et \"Q\" du clavier dès que vous voyez le stimulus, quelle que soit sa localisation. \n\

Appuyez sur n'importe quelle touche pour continuer."""

instruction1 = "Veuillez positionner votre index droit sur la touche \"M\" et votre index gauche sur la touche \"Q\" \n\
Puis appuyez sur n'importe quelle touche pour commencer"
instruction2 = "Veuillez positionner votre index gauche sur la touche \"M\" et votre index droit sur la touche \"Q\" \n\
Votre bras droit étant placé au-dessus de votre bras gauche, \n\
Puis appuyez sur n'importe quelle touche pour commencer"
instruction3 = "Veuillez positionner votre index gauche sur la touche \"M\" et votre index droit sur la touche \"Q\", \n\
Votre bras gauche étant placé au-dessus de votre bras droit, \n\
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

exp.data_variable_names = ["Bloc", "Position", "Bouton 1", "RT1", "Bouton 2", "RT2"] # Variables à enregistrer à chaque essai

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

		fixcross.present()
		trial.stimuli[0].present(clear = False)
		exp.clock.wait(square_displaytime)
		Blankscreen.present()

		user_device.clear()
		button1, rt1 = user_device.wait(keys=response_keys,duration=wait_duration)
		if not ( button1 is None ):
			button2, rt2 = user_device.wait(keys=response_keys, duration=(wait_duration-rt1))
# On stocke les paramètres de l'essai après avoir normalisé les données
		if not (button2 is None):
			if button2 == button1:	# l'utilisateur a appuyé deux fois sur la même touche => on supprime la 2ème mesure
				button2 = None
				rt2 = None
		if not ( rt2 is None ):		# il y a eu 2 frappes de touche donc le délai de la 2ème frappe est celle de la 1ère + le délai entre les 2 frappes
			rt2 += rt1
# On trie les réponses en fonction du code caractère pour avoir toujours le caractère "M" en 1ère colonne
		if not (button1 is None ) and ( button1 == key_q ) :
			exp.data.add([block.get_factor("Numéro du bloc"), show_time, trial.get_factor("Position"), button2, rt2, button1, rt1])
		else:
			exp.data.add([block.get_factor("Numéro du bloc"), show_time, trial.get_factor("Position"), button1, rt1, button2, rt2])
# On réinitialise les variables pour la boucle suivante
		button1 = None
		rt1 = None
		button2 = None
		rt2 = None

control.end()
