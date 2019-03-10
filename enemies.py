# Script which defines mainclass Enemy and different subclasses which can be initialized in world.py

class Enemy:
	def __init__(self):
		raise NotImplementedError("Do not create raw Enemy objects!")

	def __str__(self):
		return self.name

	def is_alive(self):
		return self.hp > 0

class Beetles(Enemy):
	def __init__(self):
		self.name = "Swarm of Beetles"
		self.hp = 40
		self.damage = 2

class PoisonGas(Enemy):
	def __init__(self):
		self.name = "Poisonous Cloud"
		self.hp = 40
		self.damage = 3

class GuardMob(Enemy):
	def __init__(self):
		self.name = "Murderous Butler"
		self.hp = 16
		self.damage = 8

class InsaneMob(Enemy):
	def __init__(self):
		self.name = "Insane Groundskeeper" 
		self.hp = 29
		self.damage = 5

class Maid(Enemy):
	def __init__(self):
		self.name = "Hungry Kitchen Maid" 
		self.hp = 24
		self.damage = 6

class BossMonster(Enemy):
	def __init__(self):
		self.name = "Lord Attenborough"
		self.hp = 100
		self.damage = 12