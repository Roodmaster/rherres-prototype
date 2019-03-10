from collections import OrderedDict
from player import Player
import world
# import os
# import termios
# import tty
# import sys

# class color:
#    PURPLE = '\033[95m'
#    CYAN = '\033[96m'
#    DARKCYAN = '\033[36m'
#    BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
#    RED = '\033[91m'
#    UNDERLINE = '\033[4m'
   

BOLD = '\033[1m'
END = '\033[0m'


def play():
	print(BOLD + "\n CharlesBottens_ \n" + END)
	print("""
	This game is a prototype for generative storytelling. It's based on the concept "Charles Bottens_"
	(2019) by Raphael Herres. The game structure was created with the help of "Make Your Own Python
	Text Adventure" (2018) by Phillip Johnson.

	A unique world map is created when you start the game. It is a two-dimensional grid, with you
	starting in the top row, wanting to reach the bottom one. There will be enemies and traps in your way,
	but also traders to help you. By using general directions, North, East, South and West, you can move
	from one cell to the next. You might encounter road blocks or dead ends, that hinder your movement. So
	you better try to keep track of the path you have already taken!
	""")
	
	world.parse_world_dsl()
	player = Player()
	while player.is_alive() and not player.victory:
		room = world.tile_at(player.x, player.y)
		print(room.intro_text())
		room.modify_player(player)
		if player.is_alive() and not player.victory:
			choose_action(room, player)
		elif player.victory:
			print(" Done!")
		elif not player.is_alive():
			print(" You have failed in your attempt to flee from this god forsaken place! \n")


def choose_action(room, Player):
	action = None
	while not action:
		available_actions = get_available_actions(room, Player)
		action_input = input(BOLD + YELLOW + "\n > Action: " + END)
		action = available_actions.get(action_input)
		if action:
			action()
		else:
			print(BOLD + "\n Invalid action! \n" + END)


def get_available_actions(room, player):
	actions = OrderedDict()
	print(BOLD + " Choose an action: \n" + END)

	if player.inventory:
		action_adder(actions, 'i', player.print_inventory, "Inventory")

	if isinstance(room, world.npcTrader):
		action_adder(actions, 't', player.trade, "Trade")

	if isinstance(room, (world.EnemyTile, world.BossTile)) and room.enemy.is_alive():
		action_adder(actions, 'a', player.attack, "Attack")

	else:
		if world.tile_at(room.x, room.y - 1):
			action_adder(actions, 'n', player.move_north, "Go north")

		if world.tile_at(room.x, room.y + 1):
			action_adder(actions, 's', player.move_south, "Go south")

		if world.tile_at(room.x + 1, room.y):
			action_adder(actions, 'e', player.move_east, "Go east")

		if world.tile_at(room.x - 1, room.y):
			action_adder(actions, 'w', player.move_west, "Go west")

		if player.atStart:
	 		action_adder(actions, 'j', player.jump, "Jump... why would you jump in a Text-Adventure?")

		if player.atIDoku:
		 	action_adder(actions, 'c', player.crouch, "Crouch: Get back to the start of the game.")

	
	if player.hp < 100:
		action_adder(actions, 'h', player.heal, "Heal")

	return actions


def action_adder(action_dict, hotkey, action, name):
	action_dict[hotkey.lower()] = action
	action_dict[hotkey.upper()] = action
	print(BOLD + " {}:".format(hotkey) + END + " {}".format(name))


play()