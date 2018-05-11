#!/usr/bin/python

import random, pygame

Pete_B_Idle = pygame.image.load("Images/Pete/B_Idle.png")
Pete_R_Idle = pygame.image.load("Images/Pete/R_Idle.png")
Pete_L_Idle = pygame.image.load("Images/Pete/L_Idle.png")
Pete_F_Idle = pygame.image.load("Images/Pete/F_Idle.png")
Pete_B_Walk1 = pygame.image.load("Images/Pete/B_Walk1.png")
Pete_R_Walk1 = pygame.image.load("Images/Pete/R_Walk1.png")
Pete_L_Walk1 = pygame.image.load("Images/Pete/L_Walk1.png")
Pete_F_Walk1 = pygame.image.load("Images/Pete/F_Walk1.png")
Pete_B_Walk2 = pygame.image.load("Images/Pete/B_Walk2.png")
Pete_R_Walk2 = pygame.image.load("Images/Pete/R_Walk2.png")
Pete_L_Walk2 = pygame.image.load("Images/Pete/L_Walk2.png")
Pete_F_Walk2 = pygame.image.load("Images/Pete/F_Walk2.png")

Alec_B_Idle = pygame.image.load("Images/Alec/B_Idle.png")
Alec_R_Idle = pygame.image.load("Images/Alec/R_Idle.png")
Alec_L_Idle = pygame.image.load("Images/Alec/L_Idle.png")
Alec_F_Idle = pygame.image.load("Images/Alec/F_Idle.png")
Alec_B_Walk1 = pygame.image.load("Images/Alec/B_Walk1.png")
Alec_R_Walk1 = pygame.image.load("Images/Alec/R_Walk1.png")
Alec_L_Walk1 = pygame.image.load("Images/Alec/L_Walk1.png")
Alec_F_Walk1 = pygame.image.load("Images/Alec/F_Walk1.png")
Alec_B_Walk2 = pygame.image.load("Images/Alec/B_Walk2.png")
Alec_R_Walk2 = pygame.image.load("Images/Alec/R_Walk2.png")
Alec_L_Walk2 = pygame.image.load("Images/Alec/L_Walk2.png")
Alec_F_Walk2 = pygame.image.load("Images/Alec/F_Walk2.png")

# Base Class for all characters.
class Character():
	x = 0
	y = 0
	tag = None
	GOTOx = 0
	GOTOy = 0
	facing = "Down"
	speed = 100
	incrementMove = 20
	spriteWidth = 22
	spriteHeight = 37
	animateFrame = 0
	framerate = 12
	isMoving = False
	def nextAction(self):
		pass

# The character controlled by the player. 
class Hero(Character):
	animations = [[Pete_B_Idle, Pete_B_Walk1, Pete_B_Idle, Pete_B_Walk2], 
				  [Pete_R_Idle, Pete_R_Walk1, Pete_R_Idle, Pete_R_Walk2], 
				  [Pete_L_Idle, Pete_L_Walk1, Pete_L_Idle, Pete_L_Walk2], 
				  [Pete_F_Idle, Pete_F_Walk1, Pete_F_Idle, Pete_F_Walk2]]
	image = Pete_F_Idle
	tag = "Hero"
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

# An NPC that stands still.
class StandingNPC(Character):
	image = Alec_F_Idle
	tag = "StandingNPC"
	x = 50
	y = 320
	GOTOx = 50
	GOTOy = 320

# An NPC that wanders around randomly within a box defined by the four border variables.
class WanderNPC(Character):
	animations = [[Alec_B_Idle, Alec_B_Walk1, Alec_B_Idle, Alec_B_Walk2], 
				  [Alec_R_Idle, Alec_R_Walk1, Alec_R_Idle, Alec_R_Walk2], 
				  [Alec_L_Idle, Alec_L_Walk1, Alec_L_Idle, Alec_L_Walk2], 
				  [Alec_F_Idle, Alec_F_Walk1, Alec_F_Idle, Alec_F_Walk2]]
	image = Alec_F_Idle
	tag = "WanderNPC"
	topBorder = 250
	bottomBorder = 450
	leftBorder = 250
	rightBorder = 450
	wanderSpeed = 100
	x = 350
	y = 350
	GOTOx = 350
	GOTOy = 350
	def nextAction(self):
		events = []
		goIn = random.randint(1,self.wanderSpeed)
		if goIn == 1 and self.facing != "Down":
			events.append("Up")
		if goIn == 2 and self.facing != "Left":
			events.append("Right")
		if goIn == 3 and self.facing != "Up":
			events.append("Down")
		if goIn == 4 and self.facing != "Right":
			events.append("Left")
		return events