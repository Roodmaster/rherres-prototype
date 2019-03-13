# Where most of the magic happens
# I updated a lot of Functions with \n in order to get some space between the lines
#!/usr/local/bin/python
# coding: latin-1
import os, sys
import random
import enemies
import npc
import world_building
from sample import sample

# Another dirty trick to modify the sample.py input (ref: Line 71)
chapter = 0

BOLD = '\033[1m'
END = '\033[0m'


class MapTile:
	"""World-building superclass"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def intro_text(self):
		raise NotImplementedError("Create a subclass instead!")

	def modify_player(self, player):
		pass


class StartTile(MapTile):
	"""Subclass of MapTile, used once at the start of the game"""
	def intro_text(self):
		return """

	The Beginning

	You wake up and immediately notice that something is different. You are shivering, your body is aching
	for a blanket and you are lying on the floor. This is not your room!
	You remember having a lovely evening dining with the lords and probably one too many drinks towards the
	end. That doesn't quite explain your current predicament, though. You decide to get up and find out what
	the hell happened to you and why you are not in your warm bed anymore!?

	Your foot hits something when you stand up. It's your trusty compass... You pick it up and remember the
	butler welcoming you at the 'South Gate' when you arrived at the mansion earlier.

		"""

	def modify_player(self, player):
		# Important to not have "j" displayed as possible action all the time, ref to game.py
		player.atStart = True
		player.atIDoku = False


class StoryTile(MapTile):
	"""Subclass of MapTile, used whenever there is a story to tell"""

	def __init__(self, x, y):
		self.visited = False
		self.intro = ''
		super().__init__(x, y)

	def modify_player(self, player):
		player.atStart = False

	def intro_text(self):
		# By adding this I was able to make rooms have a constant, generated intro-text 
		# as well as have the model input be Chapter 1, Chapter 2, Chapter 3 etc
		if not self.visited:
				global chapter
				chapter += 1
				self.visited = True
				model_input = 'Chapter ' + str(chapter)
				self.intro = sample(360, model_input, 1)		
		print("\n")
		print(self.intro)
		
		return ""
				

class EnemyTile(MapTile):
	def __init__(self, x, y):
		self.gold = random.randint(8, 15)
		self.gold_claimed = False
		r = random.random()
		if r <= 0.33:
			self.enemy = enemies.InsaneMob()
			self.intro = "\n Downstairs\n"
			self.alive_text = " One of the Groundskeepers has gone mad over whatever the hell happened here.\n"
			self.dead_text = " You've put a very irritated mind to rest.\n"
		elif r <= 0.66:
			self.enemy = enemies.GuardMob()
			self.intro = "\n One of the many Bedrooms\n"
			self.alive_text = " A Bloodthirsty Butler is trying to keep you from advancing.\n"
			self.dead_text = " His dead body is proof of your superior fighting skills.\n"
		else:
			self.enemy = enemies.Maid()
			self.intro = "\n Kitchenarea\n"
			self.alive_text = " One of the Kitchen Maids seems to have worked up an appetite... \n" + " That's about the only explanation you can come up with for why she is trying to take a bite out off you.\n"
			self.dead_text = " Unfortunately, her demise came at the price of your ear lobe.\n"

		super().__init__(x, y)

	def intro_text(self):
		print(BOLD + self.intro + END)
		text = self.alive_text if self.enemy.is_alive() else self.dead_text
		return text

	def modify_player(self, player):
		if self.enemy.is_alive():
			player.hp = player.hp - self.enemy.damage
			print(" Enemy does {} damage. You have {} Healthpoints remaining! \n".format(self.enemy.damage, player.hp))
		else:
			# Current HP shown at the end of the fight as well as looting some nice gold
			print(" Current Healthpoints: " + str(player.hp) + "\n")
			if not self.gold_claimed:
				self.gold_claimed = True
				player.gold = player.gold + self.gold
				print(" +{} gold found.\n".format(self.gold))


class BossTile(MapTile):
	def __init__(self, x, y):
		self.enemy = enemies.BossMonster()
		self.intro = "\n Master Study\n"
		self.alive_text = " You have disturbed one of the Lords in his study - bad idea!\n"
		self.dead_text = " The lord is lying dead on the floor and you sense that the exit is nearby.\n"

		super().__init__(x, y)

	def intro_text(self):
		print(BOLD + self.intro + END)
		text = self.alive_text if self.enemy.is_alive() else self.dead_text
		return text

	def modify_player(self, player):
		if self.enemy.is_alive():
			player.hp = player.hp - self.enemy.damage
			print(" Enemy does {} damage. You have {} Healthpoints remaining! \n".format(self.enemy.damage, player.hp))
		else:
			print(" Current Healthpoints: " + str(player.hp) + "\n")


class TrapTile(MapTile):
	# Traps can't be attacked, but have HP due to being a subclass of enemy. You aren't locked out of movement commands however
	def __init__(self, x, y):
		r = random.random()
		if r < 0.7:
			self.enemy = enemies.Beetles()
			self.intro = "\n Smelly Room\n"
			self.alive_text = " There is a swarm of beetles buzzing just above a corpse that's lying on\n" + " the floor! As you enter the room they started moving towards you.\n" + " You should probably just flee and shut the door behind you! \n"
			self.dead_text = "\n There is a pile of smushed beetles on the floor. \n"
		else:
			self.enemy = enemies.PoisonGas()
			self.intro = "\n Dizzy Room\n"
			self.alive_text = " The air is... green-ish in this room. You start coughing.\n" + " Perhaps you should just keep going and avoid breathing more of what seems to be poisonous gas! \n"
			self.dead_text = "\n"

		super().__init__(x, y)

	def intro_text(self):
		print(BOLD + self.intro + END)
		text = self.alive_text if self.enemy.is_alive() else self.dead_text
		return text

	def modify_player(self, player):
		if self.enemy.is_alive():
			player.hp = player.hp - self.enemy.damage
			print(" Trap deals {} damage. You have {} Healthpoints remaining. \n".format(self.enemy.damage, player.hp))


class Puzzle(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)


class InteractiveDoku(MapTile):
	# Very long subclass. Used in the first row of World DSL for an easter egg-level of sorts
	def __init__(self, x, y):
		super().__init__(x, y)

	def modify_player(self, player):
		player.atStart = False
		player.atIDoku = True
		x = self.x
		y = self.y
		# Room 1
		if x == 0 and y == 0 and player.x == 0 and player.y == 0:
			print("""
	Willkommen zur iDoku von CharlesBottens_

	In den folgenden Raeumen finden sich weitere Informationen zum Projekt von Raphael Herres.
	Man kann sich zwischen den Raeumen mit 'e' (nach rechts) und 'w' (nach links) bewegen. Sollte 
	eine der Optionen nicht zur Verfuegung stehen, hat man die Levelbeschraenkung erreicht. Im 
	vorletzten Raum kann man das Machine Learning-Modell des Prototyps mit einem eigenen Input
	ausprobieren. Im letzten Raum kann man sich Beispiele des von OpenAI veroeffentlichen Modells
	mit vorgefertigten Inputs anzeigen lassen (eventuell muss man hier etwas scrollen). 

	Folgende Raeume stehen zur Verfuegung:
	1. Intro
	2. Lessons Learned
	3. Das World-Building
	4. Feedback aus Usability-Tests
	5. Machine Learning-Modell von CharlesBottens_ selbst ausprobieren
	6. Beispiele von OpenAI lesen

	Zurueck zum eigentlichen Spiel gelangt man mit 'c'.
				""")
		# Room 2
		elif x == 1 and y == 0 and player.x == 1 and player.y == 0:
			print("""
	2. Lessons Learned:

	Dieses Bachelorprojekt war das erste grosse Projekt waehrend des Studiums, das ich
	komplett eigenstaendig durchgefuehrt habe. Es war spannend diese Aufgabe allein anzugehen.

	Waehrend den Projektphasen schwankt man immer irgendwo zwischen Gelassenheit und Panik.
	Dabei konnte ich diesmal auf Diskussionen verzichten und musste keine Missverstaendnisse aus
	dem Weg schaffen. Ausserdem war jede meiner Ideen 'super'.

	Doch Teammitglieder haben auch ihre Vorteile. Im Endeffekt habe ich aktiv nach Feedback und
	projektbezogenen Gespraechen gesucht, da mir das im Ein-Personen-Team gefehlt hat. Eine zweite
	Meinung, die selbst in das Projekt involviert ist und eine weitere Perspektive hat, hilft 
	ungemein. Vor allem um die vermeindlichen, 'super' Ideen einzufangen.

	Ich habe mich gefreut ein Thema bearbeiten zu koennen, das mich interessiert und mir am Herzen
	liegt. Aber in Zukunft bevorzuge ich wieder Teamarbeit über Soloarbeit!

				""")
		# Room 3
		elif x == 2 and y == 0 and player.x == 2 and player.y == 0:
			print("\n")
			print(world_dsl)
			print("""
	3. Das World-Building

	Die ausgegebene Tabelle ist eine Abbildung der aktuellen Spielwelt. Die Kuerzel in den Zellen
	stehen fuer die Raeume, die man auf seinem Weg zum Ende durchlaeuft. So steht z.B. "BT" fuer
	Story-Raeume, "EN" sind Gegner und "IN" steht fuer Interaktive Doku. Im dritten "IN"-Raum von
	links befindet sich die Spielfigur gerade!

	Startet man das Spiel neu, wird auch die Spielwelt neu generiert. Dafuer wird zuerst die
	Startposition ("ST") und ein Weg zum Ziel ("VT") festgelegt. Dieser Weg wird nie mit leeren
	Raeumen, wie sie z.B. zwischen Start und interaktiver Doku zu sehen sind, befuellt. Leere Raeume
	sind nicht betretbar, daher muss man auch zur iDoku "springen"!
	Diese Form der Levelbeschraenkung dient dazu, Sackgassen zu generieren und die Spieler in
	die Irre zu fuehren und die Herausforderung etwas zu steigern. 

	Durch die Wegfindung zu Beginn wird jedoch garantiert, dass mindestens ein begehbarer Weg zwischen
	Start und Ziel existiert. Die restlichen Zellen werden dann, mit unterschiedlicher Gewichtung,
	zufaellig befuellt.
	
				""")
		# Room 4
		elif x == 3 and y == 0 and player.x == 3 and player.y == 0:
			print("""
	4. Feedback aus Usability-Tests

	Ich habe meinen Prototyp von Kollegen, Freunden und Kommilitonen testen lassen und konnte so noch
	ein paar Dinge verbessern:

	- Man war urspruenglich in der "Heal"-Auswahl gefangen und musste einen heilenden Gegenstand
	  verbrauchen, um weiter spielen zu koennen. Mittlerweile kann man ueber den Begriff "Cancel" den
	  Vorgang abbrechen.
	- Die Kapitel zeigten nach der Generierung eine willkuerliche Nummerierung an und der Inhalt wurde bei
	  jedem Betreten eines Story-Raums neu generiert. Jetzt wird dem Modell als Prompt nicht nur "Chapter"
	  zugespielt, sondern auch eine linear hochzählende Nummerierung. Dadurch funktioniert die Kapitelanzeige
	  deutlich besser, denn diese wird auch vom Modell generiert und ist nicht vorherbestimmt.
	  Ausserdem behalten sich die Story-Raeume ihre Intro-Texte bei und helfen so sich besser zu orientieren.
	- Die Richtungsangaben "North", "East", "South", "West" sind traditioneller Text-Adventure nachempfunden,
	  ergeben fuer Menschen, die diese nie gespielt haben, aber nicht unbedingt sofort Sinn.
	  Daher wurde der Kompass als Startgegenstand und ein Hinweis auf die generelle Richtung eingebaut.
	- Healthpoints wurden urspruenglich mit "HP" abgekuerzt, was fuer unerfahrene Spieler keine gaengige
	  Abkuerzung darstellt. Ausserdem werden die aktuellen Lebenspunkte jetzt nochmal am Ende eines Kampfes
	  eingeblendet.
	- Durch die unterschiedliche Zeilenanzahl, die zwischen zwei "Actions" entstehen kann, mussten Tester
	  immer wieder mit den Augen hin und her springen, um zu verstehen welche Informationen gerade fuer sie
	  relevant sind. Formatierung ist im Terminal zwar limitiert, es wurden jedoch einige Python-Commands 
	  verwendet, um zum Einen den Text lesbarer zu machen, und zum anderen die "Actions" vom restlichen
	  Schriftbild farblich zu trennen.
				""")
		# Room 5
		elif x == 4 and y == 0 and player.x == 4 and player.y == 0:
			print("""
	5. Das Machine Learning-Modell von CharlesBottens_ selbst ausprobieren
			""")
			user_input = input(" Give any text prompt from which you want to generate a sample (in English): ")
			t = sample(400, user_input, 1)
			print("\n" + t + "\n")
		# Room 6
		elif x == 5 and y == 0 and player.x == 5 and player.y == 0:
			print(""" 
	6. Beispiele von OpenAI lesen

	Aus den folgenden Beispielen kann man waehlen: 
	1. 'Chapter One: The Journey Begins'
	2. 'The meaning of life is...'
	3. 'When I find myself in times of trouble...'
			""")
			user_input = input("Which sample would you like to read? ")
			if user_input == '1':
				with open("./chapters/chapterone.txt") as f:
					print(f.read() + "\n")
			elif user_input == '2':
				with open("./chapters/meaningoflife.txt") as f:
					print(f.read() + "\n")
			elif user_input == '3':
				with open("./chapters/beatles.txt") as f:
					print(f.read() + "\n")

	def intro_text(self):
		return "\n iDoku"
		

class npcTrader(MapTile):
	def __init__(self, x, y):
		self.trader = npc.Trader()
		self.intro = "\n Trader Joe\n"
		super().__init__(x, y)

	def check_if_trade(self, player):
		while True:
			print("\n Your gold: " + str(player.gold))
			print(" Would you like to (B)uy, (S)ell, or (Q)uit?")
			user_input = input()
			if user_input in ['Q', 'q']:
				return
			elif user_input in ['B', 'b']:
				print(" Here's whats available to buy: ")
				self.trade(buyer=player, seller=self.trader)
			elif user_input in ['S', 's']:
				print(" Here's whats available to sell: ")
				self.trade(buyer=self.trader, seller=player)
			else:
				print(BOLD + " Invalid choice!" + END)

	def trade(self, buyer, seller):
		for i, item in enumerate(seller.inventory, 1):
			print(" {}. {} - {} Gold".format(i, item.name, item.value))
		while True:
			user_input = input(" Choose an item or press Q to exit: ")
			if user_input in ['Q', 'q']:
				return
			else:
				try:
					choice = int(user_input)
					to_swap = seller.inventory[choice - 1]
					self.swap(seller, buyer, to_swap)
				except ValueError:
					print(BOLD + " Invalid choice!" + END)

	def swap(self, seller, buyer, item):
		if item.value > buyer.gold:
			print(BOLD + " That's too expensive" + END)
			return
		seller.inventory.remove(item)
		buyer.inventory.append(item)
		seller.gold = seller.gold + item.value
		buyer.gold = buyer.gold - item.value
		print(BOLD + " Trade complete!" + END)


	def intro_text(self):
		print(BOLD + self.intro + END)
		return " A frail not-quite-human, not-quite-creature squats in the corner\n" + " clinking his gold coins together. He looks willing to trade.\n"
		
class VictoryTile(MapTile):
	def modify_player(self, player):
		player.victory = True

	def intro_text(self):
		return """\n As you open the door you breath fresh air and realize that you finally made it out of this god forsaken place!"""

# Where it gets the built world from world_building.py
dsl_string = world_building.worldbuilder()

world_dsl = """{}""".format(dsl_string)

# Check if world_dsl has a Start and at least one victory, and wether all rows are equally long, in order to have a grid
def is_dsl_valid(dsl):
	if dsl.count("|ST|") != 1:
		return False
	if dsl.count("|VT|") == 0:
		return False
	lines = dsl.splitlines()
	lines = [l for l in lines if l]
	pipe_counts = [line.count("|") for line in lines]
	for count in pipe_counts:
		if count != pipe_counts[0]:
			return False
	return True

#Dict for all the room-types
tile_type_dict = {"VT": VictoryTile, "EN": EnemyTile, "ST": StartTile, "TT": TrapTile, "BT": StoryTile, "NP": npcTrader, "PU": Puzzle, "IN": InteractiveDoku, "BO": BossTile, "  ": None}

world_map = []

start_tile_location = None

# Worldmap is parsed for game.py to use
def parse_world_dsl():
	if not is_dsl_valid(world_dsl):
		raise SyntaxError("DSL is invalid!")

	dsl_lines = world_dsl.splitlines()
	dsl_lines = [x for x in dsl_lines if x]

	for y, dsl_row in enumerate(dsl_lines):
		row = []
		dsl_cells = dsl_row.split("|")
		dsl_cells = [c for c in dsl_cells if c]
		for x, dsl_cell in enumerate(dsl_cells):
			tile_type = tile_type_dict[dsl_cell]
			if tile_type == StartTile:
				global start_tile_location
				start_tile_location = x, y
			row.append(tile_type(x, y) if tile_type else None)

		world_map.append(row)
		
def tile_at(x, y):
	if x < 0 or y < 0:
		return None
	try:
		return world_map[y][x]
	except IndexError:
		return None

