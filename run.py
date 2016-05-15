#!/usr/bin/env python
# MAZEROBOT
# by Tim Heuett

import sys, os, time

import maze, robot

robotchars = (u"\u25b2",u"\u25b6",u"\u25bc",u"\u25c0")

delay = 0.1

def game(robotfile, mazefile):
	the_maze = maze.Maze(mazefile)
	the_robot = robot.Robot(robotfile, the_maze)

	robotpos = the_maze.exits[0]
	turn = 0

	while True:
		# draw the maze
		print "Turn: " + str(turn)
		for y in range(len(the_maze.graphic)):
			line = ""
			for x in range(len(the_maze.graphic[y])):
				if robotpos[0] == y and robotpos[1] == x:
					line += robotchars[the_robot.face_direction] + " "
				else:
					line += the_maze.graphic[y][x]
			print line

		# check to see if the robot made it
		if robotpos in the_maze.exits[1:]:
			print "Your robot completed the maze!"
			break

		# allow the robot to make its move
		message, robotpos = the_robot.makeMove(robotpos)
		print message

		# advance time
		time.sleep(delay)
		turn += 1

print "Welcome to MAZEROBOT, a game of slow-motion suspense\n"

# build a list of available mazes, and a list of available robots
mazes = ""
robots = ""
for item in os.listdir("./mazes"):
	if item[-4:].lower() == "maze":
		mazes += "  " + item[:-5]
for item in os.listdir("./robots"):
	if item[-3:].lower() == "rob":
		robots += "  " + item[:-4]

# make sure there are available mazes and robots
quit = False
print "Loading mazes..."
if len(mazes) < 1:
	print "Couldn't find any mazes. Make sure they are in the 'mazes' directory, and they end with '.maze'"
	quit = True
print "Loading robots..."
if len(robots) < 1:
	print "Couldn't find any robots. Make sure they are in the 'robots' directory, and they end with '.rob'"
	quit = True
if quit:
	print "Please check and try again"
	sys.exit()



# check for arguments
if len(sys.argv) == 3:
	mazefile = sys.argv[1]
	robotfile = sys.argv[2]
	if mazefile not in mazes:
		while True:
			print "That maze is not available. Try one of these?"
			print mazes
			mazefile = raw_input(": ")
			if mazefile in mazes:
				break
			print "Still no good. Try again\n"
	if robotfile not in robots:
		while True:
			print "That robot is not available. Try one of these?"
			print robots
			robotfile = raw_input(": ")
			if robotfile in robots:
				break
			print "Still no good. Try again\n"

	game(robotfile, mazefile)

	if raw_input("Would you like to play again?")[:1].lower() == 'n':
		print "\nThanks for playing!"
		sys.exit()
elif len(sys.argv) == 2 or len(sys.argv) > 3:
	print "ERROR: Invalid number of arguments"
	sys.exit()

while True:
	print
	while True:
		print "Pick a maze"
		print mazes
		mazefile = raw_input(": ")
		if mazefile in mazes:
			break
		print "That's not one of them. Try again\n"

	print
	while True:
		print "Pick a robot:"
		print robots
		robotfile = raw_input(": ")
		if robotfile in robots:
			break
		print "That's not one of them. Try again\n"

	game(robotfile,mazefile)

	if raw_input("Would you like to play again?")[:1].lower() == 'n':
		break

print "\nThanks for playing!"
sys.exit()
