#!/usr/bin/python

import random, pygame

MARIO_B_Idle = pygame.image.load("Images/Mario/B_Idle.png")
MARIO_R_Idle = pygame.image.load("Images/Mario/R_Idle.png")
MARIO_L_Idle = pygame.image.load("Images/Mario/L_Idle.png")
MARIO_F_Idle = pygame.image.load("Images/Mario/F_Idle.png")
MARIO_B_Walk1 = pygame.image.load("Images/Mario/B_Walk1.png")
MARIO_R_Walk1 = pygame.image.load("Images/Mario/R_Walk1.png")
MARIO_L_Walk1 = pygame.image.load("Images/Mario/L_Walk1.png")
MARIO_F_Walk1 = pygame.image.load("Images/Mario/F_Walk1.png")
MARIO_B_Walk2 = pygame.image.load("Images/Mario/B_Walk2.png")
MARIO_R_Walk2 = pygame.image.load("Images/Mario/R_Walk2.png")
MARIO_L_Walk2 = pygame.image.load("Images/Mario/L_Walk2.png")
MARIO_F_Walk2 = pygame.image.load("Images/Mario/F_Walk2.png")

# Base Class for all characters.
class Character():
	x = 0
	y = 0
	GOTOx = 0
	GOTOy = 0
	facing = "Down"
	speed = 100
	incrementMove = 20
	spriteWidth = 22
	spriteHeight = 37
	animateFrame = 0
	framerate = 15
	isMoving = False
	# animations = []
	# image = None
	def nextAction(self):
		pass

# The character controlled by the player. 
class Hero(Character):
	animations = [[MARIO_B_Idle, MARIO_B_Walk1, MARIO_B_Idle, MARIO_B_Walk2], 
				  [MARIO_R_Idle, MARIO_R_Walk1, MARIO_R_Idle, MARIO_R_Walk2], 
				  [MARIO_L_Idle, MARIO_L_Walk1, MARIO_L_Idle, MARIO_L_Walk2], 
				  [MARIO_F_Idle, MARIO_F_Walk1, MARIO_F_Idle, MARIO_F_Walk2]]
	image = MARIO_F_Idle
	x = 50
	y = 50
	GOTOx = 50
	GOTOy = 50
	def nextAction(self, keys):
		currentEvents = []
		if keys[pygame.K_w]:
			currentEvents.append("Up")
		if keys[pygame.K_a]:
			currentEvents.append("Left")
		if keys[pygame.K_d]:
			currentEvents.append("Right")
		if keys[pygame.K_s]:
			currentEvents.append("Down")
		return currentEvents

# An NPC that wanders around randomly within a box defined by the four border variables.
# TODO: Non-Mario Graphics (Maybe a Toad?)
class WanderNPC(Character):
	animations = [[MARIO_B_Idle, MARIO_B_Walk1, MARIO_B_Idle, MARIO_B_Walk2], 
				  [MARIO_R_Idle, MARIO_R_Walk1, MARIO_R_Idle, MARIO_R_Walk2], 
				  [MARIO_L_Idle, MARIO_L_Walk1, MARIO_L_Idle, MARIO_L_Walk2], 
				  [MARIO_F_Idle, MARIO_F_Walk1, MARIO_F_Idle, MARIO_F_Walk2]]
	image = MARIO_F_Idle
	topBorder = 0
	rightBorder = 0
	bottomBorder = 0
	leftBorder = 0
	def nextAction(self, keysPressed):
		events = []
		goIn = random.randint(1,4)
		if goIn == 1:
			events.append("Up")
		if goIn == 2:
			events.append("Right")
		if goIn == 3:
			events.append("Down")
		if goIn == 4:
			events.append("Left")
		return events