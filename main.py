#!/usr/bin/python

import pygame, sys, json
from basecharacters import Hero
from basecharacters import WanderNPC
from basecharacters import StandingNPC

# DAMAGE FORMULA: int((ATTACKBASE*USERATTACK)-(TARGETDEF/2))

pygame.init()
screenWidth = 640
screenHeight = 480

# Creates Caches for Images and Rooms
imageCache = {}
roomCache = {}

def loadImagesFromCache(tiles):
	global imageCache
	for tile in tiles:
		# Replace the image pathways referenced in our room file with Pygame Surfaces.
		if tile['image'] in imageCache.keys():
			tile['image'] = imageCache[tile['image']]
		else:
			typeTemplate = "string"
			if type(tile['image']) == type(typeTemplate):
				imageToBeAdded = pygame.image.load(tile['image'])
			else:
				imageToBeAdded = tile['image']
			imageCache[tile['image']] = imageToBeAdded
			tile['image'] = imageToBeAdded

# Forces the passed in dictionary to use ASCII strings, not Unicode
def ascii_encode_dict(data):
	ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x
	return dict(map(ascii_encode, pair) for pair in data.items())

# Opens up the Test Room (JSON File)
# Converts JSON file to python dictionary
levelFile = open('Rooms/testRoom.json')
testRoom = json.load(levelFile, object_hook = ascii_encode_dict)

# Random Tiles for Collision Detection
TileWall = pygame.image.load("Images/Tiles/Wall.png")
TileTest = pygame.image.load("Images/Tiles/Test.png")

def loadRoomFromCache(path):
	global roomCache
	if path in roomCache.keys():
		room = roomCache[path]
	else:
		openRoom = open(path)
		roomToBeAdded = json.load(openRoom, object_hook = ascii_encode_dict)
		roomCache[path] = roomToBeAdded
		room = roomToBeAdded
	return room

# Initialize Game Clock and Screen
clock = pygame.time.Clock()
screen = pygame.display.set_mode([screenWidth,screenHeight])

# Creates an array of Test Tiles to fill screen
def testCreateTiles():
	global TileTest
	global screenWidth
	global screenHeight
	tiles = []
	x = 0
	y = 0
	while True:
		newTile = {'x':x,'y':y, 'image':TileTest, 'passable':True}
		tiles.append(newTile)
		if x == (screenWidth - 40):
			x = 0
			if y == (screenHeight - 40):
				return tiles
			else:
				y += 40
		else:
			x += 40

# Turns a passed in room into a list of tiles to be used in updateScreen()
# Room is a dictionary, returns array of tiles
def tilesFromRoom(room):
	tiles = room['tiles']
	loadImagesFromCache(tiles)
	return tiles

hero = Hero()
wanderer = WanderNPC()
stander = StandingNPC()
objects = [wanderer, stander]
tiles = []

def matchTilesToRoom(room):
	global tiles
	tiles = tilesFromRoom(room)

matchTilesToRoom(testRoom)

# Debugging Position
def logPosition(state):
	print "(" + str(state.x) + ", " + str(state.y) + ") -> (" + str(state.GOTOx) + ", " + str(state.GOTOy) + "), Facing " + state.facing

# Update The Screen
def updateScreen(hero, objects, tiles):
	screen.fill([255, 255, 255])
	for state in tiles:
		screen.blit(state['image'], [state['x'], state['y']])
	screen.blit(hero.image, [hero.x, hero.y])
	for state in objects:
		screen.blit(state.image, [state.x, state.y])
	pygame.display.flip()

# Check For Input
def checkForInput():
	quitgame = False
	currentEvents = []
	for event in pygame.event.get():
	 	if event.type == pygame.QUIT:
	 		quitgame = True
	keys = pygame.key.get_pressed()  #checking pressed keys
	currentEvents = hero.nextAction(keys)
	pygame.event.pump()
	return currentEvents, quitgame

def checkForCollision(state, objects):
	touching = []
	for object in objects:
		if object['passable'] == False:
			if (state.GOTOx >= object['x'] and state.GOTOx <= (object['x'] + (object['spriteWidth'] - 1)) and 
			    state.GOTOy >= object['y'] and state.GOTOy <= (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
			elif ((state.GOTOx + (state.spriteWidth - 1)) >= object['x'] and (state.GOTOx + (state.spriteWidth - 1)) <= 
			      (object['x'] + (object['spriteWidth'] - 1)) and state.GOTOy >= object['y'] and state.GOTOy <= 
			      (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
			elif (state.GOTOx >= object['x'] and state.GOTOx <= (object['x'] + (object['spriteWidth'] - 1)) and 
			     (state.GOTOy + (state.spriteHeight - 1)) >= object['y'] and (state.GOTOy + (state.spriteHeight - 1)) <=
			     (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
			elif ((state.GOTOx + (state.spriteWidth - 1)) >= object['x'] and (state.GOTOx + (state.spriteWidth - 1)) <=
			      (object['x'] + (object['spriteWidth'] - 1)) and (state.GOTOy + (state.spriteHeight - 1)) >= object['y'] and 
			      (state.GOTOy + (state.spriteHeight - 1)) <= (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
		if object['door'] == True:
			if (state.GOTOx >= object['x'] and state.GOTOx <= (object['x'] + (object['spriteWidth'] - 1)) and 
			    state.GOTOy >= object['y'] and state.GOTOy <= (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
			elif ((state.GOTOx + (state.spriteWidth - 1)) >= object['x'] and (state.GOTOx + (state.spriteWidth - 1)) <= 
			      (object['x'] + (object['spriteWidth'] - 1)) and state.GOTOy >= object['y'] and state.GOTOy <= 
			      (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
			elif (state.GOTOx >= object['x'] and state.GOTOx <= (object['x'] + (object['spriteWidth'] - 1)) and 
			     (state.GOTOy + (state.spriteHeight - 1)) >= object['y'] and (state.GOTOy + (state.spriteHeight - 1)) <=
			     (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
			elif ((state.GOTOx + (state.spriteWidth - 1)) >= object['x'] and (state.GOTOx + (state.spriteWidth - 1)) <=
			      (object['x'] + (object['spriteWidth'] - 1)) and (state.GOTOy + (state.spriteHeight - 1)) >= object['y'] and 
			      (state.GOTOy + (state.spriteHeight - 1)) <= (object['y'] + (object['spriteHeight'] - 1))):
				touching.append(object)
	return touching

# Is Animation Done?
def isAnimationDone(state):
	if state.x == state.GOTOx and state.y == state.GOTOy:
		return True
	else:
		return False

# Change to Idle Frame
def changeToIdleFrame(state):
	state.animateFrame = 0
	directionIndex = 0
	if state.facing == "Up":
		directionIndex = 0
	if state.facing == "Right":
		directionIndex = 1
	if state.facing == "Left":
		directionIndex = 2
	if state.facing == "Down":
		directionIndex = 3
	state.image = state.animations[directionIndex][state.animateFrame]
	return state

# Next Animation Frame
def nextanimateFrame(state, ticks):
	framesThisCycle = []
	framesThisCycle.append(state.animateFrame)
	state.animateFrame += 1
	if state.animateFrame == 4:
		state.animateFrame = 0
	directionIndex = 0
	if state.facing == "Up":
		directionIndex = 0
	if state.facing == "Right":
		directionIndex = 1
	if state.facing == "Left":
		directionIndex = 2
	if state.facing == "Down":
		directionIndex = 3
	state.image = state.animations[directionIndex][state.animateFrame]
	#print "Direction: " + str(directionIndex)
	#print "Frame: " + str(state.animateFrame) + ", Ticks: " + str(ticks)
	return state

# Updates State
def updateState(state, events, elapsedTicks, ticksToAnimate):
	global tiles
	frameDuration = (1000.0 / float(state.framerate))
	if isAnimationDone(state):
		# Detect if Character is Idle
		# If Character is idle, accept new input
		if events == []:
			state = changeToIdleFrame(state)
			state.isMoving = False
		else:
			# Set movement according to keys pressed
			state.isMoving = True
			if "Down" in events:
				state.facing = "Down"
				state.GOTOy += state.incrementMove
			elif "Up" in events:
				state.facing = "Up"
				state.GOTOy -= state.incrementMove
			elif "Right" in events:
				state.facing = "Right"
				state.GOTOx += state.incrementMove
			elif "Left" in events:
				state.facing = "Left"
				state.GOTOx -= state.incrementMove
			# Make Sure Mario Doesn't Walk Off of the Screen
			if state.GOTOx < 0:
				state.GOTOx = 0
			if state.GOTOx > (screenWidth - state.spriteWidth):
				state.GOTOx = (screenWidth - state.spriteWidth)
			if state.GOTOy < 0:
				state.GOTOy = 0
			if state.GOTOy > (screenHeight - state.spriteHeight):
				state.GOTOy = (screenHeight - state.spriteHeight)
			# Do the extra stuff with WanderNPC's borders
			if state.tag == "WanderNPC":
				if state.GOTOx < state.leftBorder:
					state.GOTOx = state.leftBorder
				if state.GOTOx > (state.rightBorder - state.spriteWidth):
					state.GOTOx = (state.rightBorder - state.spriteWidth)
				if state.GOTOy < state.topBorder:
					state.GOTOy = state.topBorder
				if state.GOTOy > (state.bottomBorder - state.spriteHeight):
					state.GOTOy = (state.bottomBorder - state.spriteHeight)
			# Collision Detection with Objects
			collidedWith = checkForCollision(state, tiles)
			for collidingState in collidedWith:
				if 'door' in collidingState.keys() and collidingState['door'] == True and state.tag == "Hero":
					roomToUse = loadRoomFromCache(collidingState['tpRoom'])
					matchTilesToRoom(roomToUse)
					state.x = collidingState['tpX']
					state.GOTOx = collidingState['tpX']
					state.y = collidingState['tpY']
					state.GOTOy = collidingState['tpY']
					state = changeToIdleFrame(state)
					state.isMoving = False
				else:
					if state.facing == "Left":
						state.GOTOx = (collidingState['x'] + collidingState['spriteWidth'])
					elif state.facing == "Right":
						state.GOTOx = (collidingState['x'] - state.spriteWidth)
					elif state.facing == "Up":
						state.GOTOy = (collidingState['y'] + collidingState['spriteHeight'])
					elif state.facing == "Down":
						state.GOTOy = (collidingState['y'] - state.spriteHeight)
	else:
		# Animation Is Not Done Yet, So Move Next Distance Increment
		distance = int(state.speed * (float(elapsedTicks) / 1000.0))
		if state.facing == "Up":
			state.y -= distance
			if abs(state.GOTOy - state.y) < distance:
				state.y = state.GOTOy
		if state.facing == "Down":
			state.y += distance
			if abs(state.GOTOy - state.y) < distance:
				state.y = state.GOTOy
		if state.facing == "Left":
			state.x -= distance
			if abs(state.GOTOx - state.x) < distance:
				state.x = state.GOTOx
		if state.facing == "Right":
			state.x += distance
			if abs(state.GOTOx - state.x) < distance:
				state.x = state.GOTOx
		# Animate Motion
		if ticksToAnimate >= frameDuration:
			ticksToAnimate -= frameDuration
			state = nextanimateFrame(state, ticksToAnimate)
	# if state.tag == "WanderNPC":
	# 	logPosition(state)
	return state, ticksToAnimate

currentTicks = pygame.time.get_ticks()
elapsedTicks = 0
ticksToAnimate = 0

quitgame = False

while quitgame == False:
	updateScreen(hero, objects, tiles)
	keysPressed, quitgame = checkForInput()
	hero, ticksToAnimate = updateState(hero, keysPressed, elapsedTicks, ticksToAnimate)
	for object in objects:
		objectEvents = object.nextAction()
		object, ticksToAnimate = updateState(object, objectEvents, elapsedTicks, ticksToAnimate)
	elapsedTicks = pygame.time.get_ticks() - currentTicks
	currentTicks = pygame.time.get_ticks()
	if hero.isMoving == True:
		ticksToAnimate += elapsedTicks

sys.exit()