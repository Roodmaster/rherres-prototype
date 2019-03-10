# Script which defines mainclass NPC and different subclasses which can be initialized in world.py
# Itself initializes subclasses of Items

import items


class NonPlayableCharacter():
	def __init__(self):
		raise NotImplementedError("Do not create raw NPC objects!")

	def __str__(self):
		return self.name


class Trader(NonPlayableCharacter):
	def __init__(self):
		self.name = "Trader Joe"
		self.gold = 100
		self.inventory = [items.Apple(), items.Apple(), items.Potion(), items.Potion(), items.Dagger(), items.Sword()]