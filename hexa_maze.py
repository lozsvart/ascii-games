import random
from app import Key, Controllable

class App(Controllable):
    def __init__(self):
        self.seed = 0
        self.show_solution = False
        self.generate()

    def generate(self):
        global parentMap
        parentMap = {}
        self.nodes = getNodes(SIZE)
        edgeList = getEdges(self.nodes, SIZE)
        shuffle(edgeList, self.seed)
        self.mazeEdges = generateMazeEdges(edgeList)

    def press(self, key):
        if key == Key.DOWN:
            self.seed -= 1
            self.generate()
        if key == Key.UP:
            self.seed += 1
            self.generate()
        if key == Key.A:
            self.show_solution = not self.show_solution

    def show(self):
        return "Seed: " + str(self.seed) + "\n" +\
            renderMaze(self.nodes, self.mazeEdges, SIZE, MAZE_STYLES["D"], self.show_solution)

SIZE = 4

DIR_A = (1, 0, -1)
DIR_B = (1, -1, 0)
DIR_C = (0, 1, -1)
DIR_D = (-1, 0, 1)
DIR_E = (-1, 1, 0)
DIR_F = (0, -1, 1)

DIRS = (DIR_A, DIR_B, DIR_C, DIR_D, DIR_E, DIR_F)

parentMap = {}

def getParent(node):
  return parentMap.get(node, node)

def setParent(node, parent):
  parentMap[node] = parent

def find(node):
  if getParent(node) == node:
    return node
  else:
    result = find(getParent(node))
    setParent(node, result)
    return result
    
def componentunion(nodeX, nodeY):
  roots = [find(nodeX), find(nodeY)]
  if roots[0] != roots[1]:
    random.shuffle(roots)
    setParent(roots[0], roots[1])

def isAlreadyConnected(nodeX, nodeY):
  return find(nodeX) == find(nodeY)


# ---------------------------------
TRANSPARENT = ""

def spaceToTransparent(char):
  return TRANSPARENT if char == " " else char

def createEmpty():
  return lambda coord: TRANSPARENT

def create(string):
  lines = string.split("\n")
  def result(coord):
    x, y = coord
    if x >= 0  and x < len(lines):
      if y >= 0 and y < len(lines[x]):
        return spaceToTransparent(lines[x][y])
    return TRANSPARENT  
  return result
    
def translate(stringArt, vect):
  return lambda coord: stringArt((coord[0] - vect[0], coord[1] - vect[1]))

def saunion(stringArts):
  def result(coord):
    x, y = coord
    for art in stringArts:
      if art(coord) != TRANSPARENT:
        return art(coord)
    return TRANSPARENT
  return result


#-------------------------------------
def isInside(node, size):
    x, y, z = node
    return max((abs(x), abs(y), abs(z))) <= size

def addVector(vec1, vec2):
    return tuple(map(lambda x, y: x + y, vec1, vec2))

def getNeighbors(node):
   return tuple(map(lambda x: addVector(node, x), DIRS))
    
def getNodes(size):
    result = []
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            if abs(i + j) <= size:
                result.append(tuple([i, j, -(i+j)]))
    return tuple(result)

def createEdge(node1, node2):
    if node1 < node2:
        return (node1, node2)
    else:
        return (node2, node1)

def getEdges(nodes, size):
    result = list()
    for node in nodes:
        for neighbor in getNeighbors(node):
            if isInside(neighbor, size):
                result.append(createEdge(node, neighbor))
    return result

def generateMazeEdges(edgeList):
  mazeEdges = set()
  for edge in edgeList:
    node1, node2 = edge
    if not isAlreadyConnected(node1, node2):
      componentunion(node1, node2)
      mazeEdges |= {edge}
  return mazeEdges

def shuffle(edgeList, seed = None):
    if seed == None:
        seed = random.randint(0, 1000)
    random.seed(seed)
    random.shuffle(edgeList)


#-------------------


def resolveChar(char):
  return  " " if char == TRANSPARENT else char

def renderArt(stringArt, dimension):
  sizeX, sizeY = dimension
  lines = []
  for i in range(sizeX):
    lines.append("".join([resolveChar(stringArt((i, j))) for j in range(sizeY)]))
  return "\n".join(lines)  
    
# -----------------------------------

V1_A = (2, 0)
V2_A = (1, 2)
def nodeToCoordStyleA(node):
    x, y, z = node
    return (x * V1_A[0] + y * V2_A[0], x * V1_A[1] + y * V2_A[1])

V1_B = (0, 4)
V2_B = (-2, 2)
def nodeToCoordStyleB(node):
    x, y, z = node
    return (x * V1_B[0] + y * V2_B[0], x * V1_B[1] + y * V2_B[1])

V1_C = (1, 2)
V2_C = (-1, 2)
def nodeToCoordStyleC(node):
    x, y, z = node
    return (x * V1_C[0] + y * V2_C[0], x * V1_C[1] + y * V2_C[1])

V1_D = (4, 0)
V2_D = (2, 5)
def nodeToCoordStyleD(node):
    x, y, z = node
    return (x * V1_D[0] + y * V2_D[0], x * V1_D[1] + y * V2_D[1])

def getOpenDoorsFrom(node, edges):
  nodeEdges = set(filter(lambda edge: node in edge, edges))
  return {direction for direction in DIRS if createEdge(node, addVector(node, direction)) in nodeEdges}

def getMazeArt(nodes, edges, pathNodes, style):
    def getNodeArt(node):
        translation = style["hexaCoordToFieldCoord"](node)
        hexaProvider = style["fieldArtProvider"]
        openDoors = getOpenDoorsFrom(node, edges)
        hexaArt = hexaProvider(openDoors, node in pathNodes)
        #hexaArt = saunion([translate(create(str(node)), (2, 1)), hexaArt])
        return translate(hexaArt, translation)
    return saunion([getNodeArt(node) for node in nodes])

def addEdgeToDict(edge, dictionary):
  start, end = edge
  if (start in dictionary):
    dictionary[start].append(end)
  else:
    dictionary[start] = [end]

def getNeighborsDict(edges):
  result = {}
  for edge in edges:
    addEdgeToDict(edge, result)
    addEdgeToDict(edge[::-1], result)
  return result

def backtracePath(previousFieldDict, start):
  current = start
  result = []
  while (current != previousFieldDict[current]):
    result.append(current)
    current = previousFieldDict[current]
  result.append(current)
  return result

def getPath(edges, startNode, endNode):
    parentDict = {startNode: startNode}
    neighborsDict = getNeighborsDict(edges)
    queue = [startNode]
    while len(queue) > 0:
      current = queue.pop(0)
      neighbors = neighborsDict[current]

      unvisitedNeighbors = [neighbor for neighbor in neighbors if neighbor not in parentDict]
      unvisitedNeighborsDict = {neighbor: current for neighbor in unvisitedNeighbors}
      
      parentDict.update(unvisitedNeighborsDict)
      queue.extend(unvisitedNeighbors)

    if endNode in parentDict:
        return backtracePath(parentDict, endNode)
    else:
        return None

START = (SIZE, 0, -SIZE)
END = (-SIZE, 0, SIZE)
def renderMaze(nodes, edges, size, style, showSolution = False):
    pathNodes = set()
    if showSolution:
        pathNodes = getPath(edges, START, END)
    mazeArt = translate(getMazeArt(nodes, edges, pathNodes, style), style["translation"](size))
    return renderArt(mazeArt, style["totalSize"](size))

DOORS_STYLE_A = {
  DIR_A: create("\n\n _"),
  DIR_B: create("\n\n\\"),
  DIR_C: create("\n\n  /"),
  DIR_D: create(" _"),
  DIR_E: create("\n  \\"),
  DIR_F: create("\n/")  
}
def hexProviderA(openDoors, isInPath = False):
  doors = [door for direction, door in DOORS_STYLE_A.items() if direction not in openDoors]
  return saunion(doors)

DOORS_STYLE_B = {
  DIR_A: create("\n    O"),
  DIR_B: create("\n\n   O"),
  DIR_C: create("   O"),
  DIR_D: create("\nO"),
  DIR_E: create(" O"),
  DIR_F: create("\n\n O")
}
def hexProviderB(openDoors, isInPath = False):
  doors = [door for direction, door in DOORS_STYLE_B.items() if direction not in openDoors]
  return saunion(doors)

DOORS_STYLE_C = {
  DIR_A: create("\n\n  /"),
  DIR_B: create("\n\n _"),
  DIR_C: create("\n  \\"),
  DIR_D: create("\n/"),
  DIR_E: create(" _"),
  DIR_F: create("\n\n\\")
}
def hexProviderC(openDoors, isInPath = False):
  doors = [door for direction, door in DOORS_STYLE_C.items() if direction not in openDoors]
  return saunion(doors)

DOORS_STYLE_D = {
  DIR_A: create("\n\n\n\n   --"),
  DIR_B: create("\n\n\n \\"),
  DIR_C: create("\n\n\n      /"),
  DIR_D: create("   --"),
  DIR_E: create("\n      \\"),
  DIR_F: create("\n /")
}
D_HEX =        create("  O  O\n\nO      O\n\n  O  O")
D_HEX_MARKED = create("  O  O\n\nO  ##  O\n\n  O  O")
def hexProviderD(openDoors, isInPath = False):
  doors = [door for direction, door in DOORS_STYLE_D.items() if direction not in openDoors]
  return saunion([D_HEX if not isInPath else D_HEX_MARKED] + doors)

MAZE_STYLES = {
  "A": {
      "fieldArtProvider": hexProviderA,
      "totalSize": lambda size: (4 * size + 3, 4 * size + 3),
      "translation": lambda size: (2 * size, 2 * size),
      "hexaCoordToFieldCoord": nodeToCoordStyleA,
  },
  "B": {
      "fieldArtProvider": hexProviderB,
      "totalSize": lambda size: (4 * size + 3, 5 * 8 * size),
      "translation": lambda size: (2 * size, 4 * size),
      "hexaCoordToFieldCoord": nodeToCoordStyleB,
  },
  "C": {
      "fieldArtProvider": hexProviderC,
      "totalSize": lambda size: (4 * size + 3, 4 * size + 3),
      "translation": lambda size: (2 * size, 2 * size),
      "hexaCoordToFieldCoord": nodeToCoordStyleC,
  },
  "D": {
      "fieldArtProvider": hexProviderD,
      "totalSize": lambda size: (8 * size + 5, 10 * size + 8),
      "translation": lambda size: (4 * size, 5 * size),
      "hexaCoordToFieldCoord": nodeToCoordStyleD,
  }
}
