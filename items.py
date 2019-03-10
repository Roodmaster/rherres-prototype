# Script which defines mainclass Weapon as well as Consumable and different subclasses which can be initialized elsewhere

class Weapon:
	def __init__(self):
		raise NotImplementedError("Do not create raw Weapon objects.")

	def __str__(self):
		return self.name	


class Compass(Weapon):
	def __init__(self):
		self.name = "your Compass"
		self.description = "A fist-sized compass, suitable for bludgeoning someone and dealing a moderate amount of damage to their head."
		self.damage = 8
		self.value = 1
	

class Dagger(Weapon):
	def __init__(self):
		self.name = "Dagger"
		self.description = "A small, definitely better than a stupid rock."
		self.damage = 14
		self.value = 30


class Sword(Weapon):
	def __init__(self):
		self.name = "Rusty Sword"
		self.description = "Well, it's a bit rusty but can still kill stuff!"
		self.damage = 20
		self.value = 50


class Consumable:
	def __init__(self):
		raise NotImplementedError("Do not create raw Consumable objects!")

	def __str__(self):
		return "{} (+{} Healthpoints)".format(self.name, self.healing_value)


class Apple(Consumable):
	def __init__(self):
		self.name = "Apple"
		self.healing_value = 10
		self.value = 5


class Potion(Consumable):
	def __init__(self):
		self.name = "Healing Potion"
		self.healing_value = 40
		self.value = 15
		