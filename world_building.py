import random
import numpy as np

cols = 6
rows = 12
rooms_vis = []
rooms_filled = []
s = np.random.choice(cols)
idoku = s


def worldlists():
	for y in range(rows):
		rooms_vis.append([])
		rooms_filled.append([])
		for x in range(cols):
			if y == 0:
				rooms_vis[y].append('i')
				rooms_filled[y].append(7)
			elif y == 1:
				rooms_vis[y].append('b')
				rooms_filled[y].append(0)
			else:	
				rooms_vis[y].append('x')
				rooms_filled[y].append(2)

worldlists()

# print(rooms_vis)
# print(rooms_filled)


def wayfinder():
	keepgoing = True
	y = 2
	x = s
	#idoku = s
	rooms_vis[y][x] = 's'
	d = np.random.choice(3)
	#print(x, d)

	while keepgoing:
		if d == 0:
			if x == 0:
				if y < rows-1:
					y = y + 1
					rooms_vis[y][x] = 'o' 
				else:
					rooms_vis[y][x] = 'z'
					keepgoing = False
				r = random.random()
				if r <= 0.5:
					d = 1
				else:
					d = 2
				#print(y, d)
			elif x in range(1,cols): 
				x = x - 1
				rooms_vis[y][x] = 'o'
				r = random.random()
				if r <= 0.5:
					d = 0
				else:
					d = 2
				#print(y, d)
		if d == 1:
			if x == cols-1:
				if y < rows-1:
					y = y + 1
					rooms_vis[y][x] = 'o'
				else:
					rooms_vis[y][x] = 'z'
					keepgoing = False
				r = random.random()
				if r <= 0.5:
					d = 0
				else:
					d = 2
				#print(y, d)
			elif x in range(cols-1):
				x = x + 1
				rooms_vis[y][x] = 'o'
				r = random.random()
				if r <= 0.5:
					d = 1
				else:
					d = 2
				#print(y, d)
		if d == 2:
			if  y < rows-1:
				y = y + 1
				rooms_vis[y][x] = 'o'
				d = np.random.choice(3)
				#print(y, d)
			else:
				rooms_vis[y][x] = 'z'
				keepgoing = False

wayfinder()

def worldfiller():
	for y in range(rows):
		for x in range(cols):
			#if rooms_vis[y][x] == 'i':
			if rooms_vis[y][x] == 'o':
				r = random.random()
				if r <= 0.35:
					rooms_filled[y][x] = 3
				elif r <= 0.5:
					rooms_filled[y][x] = 4
				elif r <= 0.65:
					rooms_filled[y][x] = 5
				else:
					rooms_filled[y][x] = 2
			elif rooms_vis[y][x] == 'x':
				r = random.random()
				if r <= 0.35:
					rooms_filled[y][x] = 3
				elif r <= 0.5:
					rooms_filled[y][x] = 4
				elif r <= 0.6:
					rooms_filled[y][x] = 5
				else:
					rooms_filled[y][x] = 0

worldfiller()

def set_start_end():
	for y in range(rows):
		for x in range(cols):
			if rooms_vis[y][x] == 's':
				rooms_filled[y][x] = 1
				rooms_filled[y+1][x] = 2
				if x in range(1,cols):
					rooms_filled[y][x-1] = 2
				if x in range(cols-1):
					rooms_filled[y][x+1] = 2
			elif rooms_vis[y][x] == 'z':
				rooms_filled[y][x] = 9
				rooms_filled[y-1][x] = 8
				if x in range(1,cols):
					rooms_filled[y][x-1] = 8
				if x in range(cols-1):
					rooms_filled[y][x+1] = 8


set_start_end()

	
	# 0 = '  ' (Dead Tile)
	# 1 = 'ST' (Start Tile)
	# 2 = 'BT' (Story Tile)
	# 3 = 'EN' (Enemy Tile)
	# 4 = 'TT' (Trap Tile)
	# 5 = 'NP' (NPC/Merchant)
	# 6 = 'PU' (Puzzle) unused
	# 7 = 'IN' (Interactive Docu)
	# 8 = 'BO' (Boss Enemy Tile)
	# 9 = 'VT' (Victory Tile)


def worldbuilder():
	mystring = ''
	for y in range(rows):
		for item in rooms_filled[y]:
		    if item == 0:
		        mystring = mystring + '|  '
		    elif item == 1:
		    	mystring = mystring + '|ST'
		    elif item == 2:
		    	mystring = mystring + '|BT'
		    elif item == 3:
		    	mystring = mystring + '|EN'
		    elif item == 4:
		    	mystring = mystring + '|TT'
		    elif item == 5:
		    	mystring = mystring + '|NP'
		    elif item == 6:
		    	mystring = mystring + '|PU'
		    elif item == 7:
		    	mystring = mystring + '|IN'
		    elif item == 8:
		    	mystring = mystring + '|BO'
		    elif item == 9:
		    	mystring = mystring + '|VT'

		mystring = mystring + '|' + '\n'

	return mystring