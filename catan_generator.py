from app import Key, Controllable

class App(Controllable):

    def __init__(self):
        self.seed = 0

    def press(self, key):
        if key == Key.UP:
            self.seed += 1
        if key == Key.DOWN:
            self.seed -= 1
        if key == Key.A:
            global DESERT_IN_THE_MIDDLE
            DESERT_IN_THE_MIDDLE = not DESERT_IN_THE_MIDDLE
        if key == Key.B:
            self.seed = random.randint(0, 1000)

    def show(self):
        deckList = getFieldDeckList(self.seed)
        fieldMap = getFieldMap(deckList)
        return renderFieldMap(fieldMap) + "\nMap seed: " + str(self.seed)
        
DESERT_IN_THE_MIDDLE = True
#
ORE_FIELD_STRING    = r"""
  O--O
 /  ^ \
O  ^ ^ O
 \    /
  O--O"""[1:]
WOOD_FIELD_STRING   = r"""
  O--O
 /  T \
O  TT  O
 \ T  /
  O--O"""[1:]
WOOL_FIELD_STRING   = r"""
  O--O
 / WW \
O WWWW O
 \ WW /
  O--O"""[1:]
WHEAT_FIELD_STRING  = r"""
  O--O
 / /  \
O   /  O
 \ \  /
  O--O"""[1:]
WATER_FIELD_STRING  = r"""
  O--O
 /~~~~\
O~~~~~~O
 \~~~~/
  O--O"""[1:]
BRICK_FIELD_STRING  = r"""
  O--O
 / ++ \
O  ++  O
 \ ++ /
  O--O"""[1:]
DESERT_FIELD_STRING = r"""
  O--O
 /    \
O      O
 \    /
  O--O"""[1:]

ORE = "ore"
WOOD = "wood"
WOOL = "wool"
BRICK = "brick"
WATER = "water"
DESERT = "desert"
WHEAT = "wheat"

FIELD_COUNTS = {
  ORE: 3,
  WOOD: 4,
  WOOL: 4,
  BRICK: 3,
  DESERT: 1,
  WHEAT: 4
}
#
# --------------------------

import random
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
    return max(map(abs, node)) <= size
	
def getNodes(size):
    result = []
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            if abs(i + j) <= size:
                result.append(tuple([i, j, -(i+j)]))
    return tuple(result)

def shuffle(list, seed = None):
    if seed == None:
        seed = random.randint(0, 1000)
    random.seed(seed)
    random.shuffle(list)

def resolveChar(char):
  return  " " if char == TRANSPARENT else char

def renderArt(stringArt, dimension):
  sizeX, sizeY = dimension
  lines = []
  for i in range(sizeX):
    lines.append("".join([resolveChar(stringArt((i, j))) for j in range(sizeY)]))
  return "\n".join(lines)


FIELD_ART_BY_NAME = {
    ORE: create(ORE_FIELD_STRING),
    WOOD: create(WOOD_FIELD_STRING),
    WOOL: create(WOOL_FIELD_STRING),
    BRICK: create(BRICK_FIELD_STRING),
    WATER: create(WATER_FIELD_STRING),
    WHEAT: create(WHEAT_FIELD_STRING),
    DESERT: create(DESERT_FIELD_STRING)
}

def getFieldDeckList(seed = None):
    fieldDeckList = []
    for field, num in FIELD_COUNTS.items():
        for i in range(num):
            fieldDeckList.append(field)
    shuffle(fieldDeckList, seed)
    return fieldDeckList

FIELDS = sorted(getNodes(2), key = lambda x: sum(map(abs, x)))
def getFieldMap(deckList):
    fieldMap = dict()
    listCopy = deckList[:]
    if DESERT_IN_THE_MIDDLE:
        listCopy.sort(key = lambda field: 0 if field == DESERT else 1)
    for field in FIELDS:
        fieldMap[field] = listCopy.pop(0)
    return fieldMap

def getFieldTranslation(field):
    x, y, z = field
    return (x * 4 + y * 2, y * 5)

def getFieldArt(field, fieldType):
    baseArt = FIELD_ART_BY_NAME.get(fieldType)
    translatedArt = translate(baseArt, getFieldTranslation(field))
    return translatedArt

def getFieldArts(fieldMap):
    fields = getNodes(3)
    return [getFieldArt(field, fieldMap.get(field, WATER)) for field in fields]

def getLegendItem(name, art):
    labelArt = translate(create(" - " + name), (2, 9))
    return saunion([art, labelArt])

def getLegendArt():
    arts = []
    x = 0
    for name, art in FIELD_ART_BY_NAME.items():
        arts.append(translate(getLegendItem(name, art), (x, 0)))
        x += 4
    return saunion(arts)

def renderFieldMap(fieldMap):
    fieldsArt = translate(saunion(getFieldArts(fieldMap)), (12, 15))
    legendArt = translate(getLegendArt(), (0, 45))
    return renderArt(saunion([fieldsArt, legendArt]), (30, 65))
