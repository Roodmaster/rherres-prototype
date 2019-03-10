import items
import world
import world_building

returnFromDoku = world_building.idoku

BOLD = '\033[1m'
END = '\033[0m'

class Player:
	def __init__(self):
		self.inventory = [items.Compass(), items.Apple(), items.Apple()]
		self.x = world.start_tile_location[0]
		self.y = world.start_tile_location[1]
		self.hp = 100
		self.gold = 5
		self.victory = False
		self.atStart = False
		self.atIDoku = False

	def is_alive(self):
		return self.hp > 0


	def print_inventory(self):
		print("\n" + BOLD + " Inventory:" + END)
		for item in self.inventory:
			print(' * ' + str(item))
		print(" * Gold: {}".format(self.gold))

	def heal(self):
		print(BOLD + "\n Current HP: {}".format(self.hp) + END)
		consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]
		if not consumables:
			print("\n You don't have any items to heal you!\n")
			return
		else:
			print("\n Input the number of the item you want to use or type 'Cancel' to cancel:\n")

		for i, item in enumerate(consumables, 1):
			print(" {}. {}".format(i, item))

		valid = False
		while not valid:
			choice = input("")
			if choice == "cancel" or "Cancel":
				valid = True
			try:
				to_eat = consumables[int(choice)-1]
				self.hp = min(100, self.hp + to_eat.healing_value)
				self.inventory.remove(to_eat)
				print(" Current HP: {}".format(self.hp))
				valid = True
			except (ValueError, IndexError):
				print(BOLD + "\n Invalid choice, try again!" + END)
			
 

	def most_powerful_weapon(self):
		max_damage = 0
		best_weapon = None
		for item in self.inventory:
			try:
				if item.damage > max_damage:
					best_weapon = item
					max_damage = item.damage
			except AttributeError:
				pass

		return best_weapon

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def jumpTo(self, dx, dy):
		self.x = 0
		self.y = 0

	def crouchTo(self, dx, dy):
		self.x = returnFromDoku
		self.y = 2

	def move_north(self):
		self.move(dx = 0, dy = -1)

	def move_south(self):
		self.move(dx = 0, dy = 1)

	def move_east(self):
		self.move(dx = 1, dy = 0)

	def move_west(self):
		self.move(dx = -1, dy = 0)

	def jump(self):
		self.jumpTo(dx = 0, dy = -2)

	def crouch(self):
		self.crouchTo(dx = 0, dy = + 2)

	def attack(self):
		best_weapon = self.most_powerful_weapon()
		room = world.tile_at(self.x, self.y)
		enemy = room.enemy
		print("\n You use {} against {}!".format(best_weapon.name, enemy.name))
		enemy.hp -= best_weapon.damage
		if not enemy.is_alive():
			print("\n You defeated {}.".format(enemy.name))
		else:
			print("\n {} has {} Healthpoints left.".format(enemy.name, enemy.hp))

	def trade(self):
		room = world.tile_at(self.x, self.y)
		room.check_if_trade(self)