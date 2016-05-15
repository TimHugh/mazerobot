import sys

class Maze:
  def __init__(self, mazefile):
    rawmaze = self.loadMaze(mazefile)
    self.wallmap, self.graphic, self.exits = self.parseMaze(rawmaze)
    self.height = len(self.wallmap)
    self.width = len(self.wallmap[0])


  def getWall(self, position):
    return self.wallmap[position[0]][position[1]]


  def loadMaze(self, mazefile):
    """Reads maze data from the maze definition file"""
    try:
      infile = open("./mazes/" + mazefile + ".maze",'r')
    except:
      print "The maze " + mazefile + " doesn't exist in 'mazes' directory"
      sys.exit()
    rawmaze = []
    for line in infile:
      rawmaze.append(line[:-1])
    return rawmaze


  def parseMaze(self, rawmaze):
    """Converts a raw text maze into the logical and ascii forms we will use to represent it"""
    graphic = []  # an ascii representation that is easier to see
    wallmap = []  # a boolean representation (True is wall, False is open)
    exits = []
    for y in range(len(rawmaze)):
      graphic.append([])
      wallmap.append([])
      for x in range(len(rawmaze[y])):  # for each square
        if rawmaze[y][x] == "#":  # if there is a wall piece
          wallmap[y].append(True)
          sideDesc = []
          if y > 0: # check the top
            if rawmaze[y-1][x] == "#": sideDesc.append(True)
            else: sideDesc.append(False)
          else:
            sideDesc.append(False)
          if y < len(rawmaze) - 1:  # check the bottom
            if rawmaze[y+1][x] == "#": sideDesc.append(True)
            else: sideDesc.append(False)
          else:
            sideDesc.append(False)
          if x > 0: # check the left
            if rawmaze[y][x-1] == "#": sideDesc.append(True)
            else: sideDesc.append(False)
          else:
            sideDesc.append(False)
          if x < len(rawmaze[y]) - 1: # check the right
            if rawmaze[y][x+1] == "#": sideDesc.append(True)
            else: sideDesc.append(False)
          else:
            sideDesc.append(False)
          graphic[y].append (self.getWallGraphic(sideDesc))
        else:   # if there is no wall piece
          wallmap[y].append(False)
          graphic[y].append("  ")
          if y == 0 or y == len(rawmaze)-1 or x == 0 or x == len(rawmaze[y])-1:
            exits.append((y,x))

    if len(exits) < 2:
      print "This maze doesn't have enough exits (Must be at least one exit and one entrance)"
#     sys.exit()

    return (wallmap, graphic, exits)


  def getWallGraphic(self, sideDesc):
    """Returns the appropriate ascii character for a wall piece depending on the location of walls around it"""
    # sideDesc is 4 bools, in order Top, Bottom, Left, Right
    if sideDesc[0]:
      if sideDesc[1]:
        if sideDesc[2]:
          if sideDesc[3]:
            return u"\u254b\u2501"
          else:
            return u"\u252b "
        else:
          if sideDesc[3]:
            return u"\u2523\u2501"
          else:
            return u"\u2503 "
      else:
        if sideDesc[2]:
          if sideDesc[3]:
            return u"\u253b\u2501"
          else:
            return u"\u251b "
        else:
          if sideDesc[3]:
            return u"\u2517\u2501"
          else:
            return u"\u2503 "
    else:
      if sideDesc[1]:
        if sideDesc[2]:
          if sideDesc[3]:
            return u"\u2533\u2501"
          else:
            return u"\u2513 "
        else:
          if sideDesc[3]:
            return u"\u250f\u2501"
          else:
            return u"\u2503 "
      else:
        return u"\u2501\u2501"
