import sys

rel_directions = ('f', 'r', 'b', 'l')
abs_directions = ('n', 'e', 's', 'w')
dir_short = { 'f': 'forward', 'b': 'backward', 'l': 'left', 'r': 'right' }

class Robot:
	def __init__(self, robotfile, the_maze):
		self.__maze = the_maze

		self.__name = robotfile
		self.rawrobot = self.loadRobot(robotfile)
		self.commands, self.curCom = self.parseCommands(self.rawrobot)
		self.face_direction = 2


	def makeMove(self, position):
		command = self.commands[self.curCom]

		# MOVE
		if command[0] == "move":
			mvdir = 0
			if command[1] == "b":
				mvdir = 2

			newPos = self.updatePos(position, mvdir)
			if self.canMove(position, mvdir):
				self.curCom += 1
				return self.__name + " moves to " + str(newPos), newPos
			else:
				self.curCom += 1
				return self.__name + " attempts to move to " + str(newPos), position

		# TURN
		elif command[0] == "turn":
			self.face_direction = (self.face_direction + rel_directions.index(command[1])) % 4
			self.curCom += 1
			return self.__name + " turns " + dir_short[command[1]], position

		# SENSE
		elif command[0] == "sense":
			if self.canMove(position, rel_directions.index(command[1])):
				self.curCom = command[2]
				return self.__name + " senses " + dir_short[command[1]] + " and feels nothing. Goes to label '" + command[3] + "'", position
			else:
				self.curCom += 1
				return self.__name + " senses " + dir_short[command[1]] + " and feels a wall", position

		# GOTO
		elif command[0] == "goto":
			self.curCom = command[1]
			return self.__name + " goes to to label '" + command[2] + "'", position


	def updatePos(self, position, rel_direction):
		abs_direction = abs_directions[(rel_direction + self.face_direction)%4]

		if abs_direction == "n":
			return (position[0]-1, position[1])
		elif abs_direction == "s":
			return (position[0]+1, position[1])
		elif abs_direction == "w":
			return (position[0], position[1]-1)
		elif abs_direction == "e":
			return (position[0], position[1]+1)
		print "THIS SHOULDN'T BE HERE"


	def canMove(self, position, rel_direction):
		newPos = self.updatePos(position, rel_direction)
		if newPos[0] < 0 or newPos[1] < 0 or newPos[0] >= self.__maze.height or newPos[1] >= self.__maze.width:
			return False
		return not self.__maze.getWall(newPos)


	def loadRobot(self,robotfile):
		"""Reads robocode from the robot definition file"""
		try:
			infile = open("./robots/" + robotfile + ".rob", "r")
		except:
			print "The robot " + robotfile + " doesn't exist in 'robots' directory"
			sys.exit()
		rawrobot = []
		for line in infile:
			rawrobot.append(line.strip())
		return rawrobot


	def parseCommands(self, rawrobot):
		commands = []
		curCom = 0
		curLine = 0
		labels = {}

		start = 0
		quit = False

		for line in rawrobot:
			curLine += 1
			words = line.lower().split()

			if len(words) < 1 : continue

			if words[0] == "move":
				try:
					if words[1] in ("f", "b"):
						commands.append(["move", words[1]])
						curCom += 1
					else:
						print "ERROR on line" + curline + " of " + self.__name + ".rob. " + words[1] + " is not a valid move direction"
				except:
					print "ERROR on line" + curline + " of " + self.__name + ".rob. MOVE requires one argument"

			elif words[0] == "turn":
				try:
					if words[1] in ("l", "r"):
						commands.append(["turn", words[1]])
						curCom += 1
					else:
						print "ERROR on line" + curline + " of " + self.__name + ".rob. " + words[1] + " is not a valid turn direction"
						quit = True
				except:
					print "ERROR on line" + curline + " of " + self.__name + ".rob. TURN requires one argument"

			elif words[0] == "sense":
				try:
					if words[1] in ("f", "b", "l", "r"):
						commands.append(["sense",words[1],"",words[2]])
						curCom += 1
					else:
						print "ERROR on line" + curline + " of " + self.__name + ".rob. " + words[1] + " is not a valid direction"
						quit = True
				except:
					print "ERROR on line" + curline + " of " + self.__name + ".rob. SENSE requires two arguments"
					quit = True

			elif words[0] == "goto":
				try:
					commands.append(["goto", "", words[1]])
					curCom += 1
				except:
					print "ERROR on line" + curline + " of " + self.__name + ".rob. GOTO requires one argument"
					quit = True

			elif words[0] == "start":
				# add the start label to current command (next line)
				start = curCom

			elif words[0][-1:] == ":":
				# add label to current command (next line)
				labels[words[0][:-1]] = curCom

		# replace goto labels with command numbers
		for command in commands:
			if command[0] == "goto":
				try:
					command[1] = labels[command[2]]
				except:
					print "ERROR: Label " + command[2] + " does not exist."
					quit = True
			elif command[0] == "sense":
				try:
					command[2] = labels[command[3]]
				except:
					print "ERROR: Label " + command[3] + " does not exist."
					quit = True

#		if quit: sys.exit()
		return commands, start
