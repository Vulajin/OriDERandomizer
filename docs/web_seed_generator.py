import re
import math
import time

#A custom implementation of a Mersenne Twister
#(since javascript hates everything)
#https://en.wikipedia.org/wiki/Mersenne_Twister
class Random:

    def seed(self, seed):
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed_hash(seed)
        for i in range(1, 624):
            self.mt[i] = int(0xFFFFFFFF & (1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i))

    def generate_sequence(self):
        for i in range(624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = int(0xFFFFFFFF & (self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

    def random(self):
        if self.index >= 624:
            self.generate_sequence()

        y = self.mt[self.index]

        # Right shift by 11 bits
        y = y ^ y >> 11
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ y << 7 & 2636928640
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        # Right shift by 18 bits
        y = y ^ y >> 18

        self.index = self.index + 1

        # javascript drops the 32nd bit (grrr), so this must be modified
        return int(0x7FFFFFFF & y) / float(0x80000000)

    def randrange(self, length):
        return int(self.random() * length)

    def randint(self, low, high):
        return int(low + self.random() * (high - low + 1))

    def uniform(self, low, high):
        return self.random() * (high - low) + low

    def shuffle(self, items):
        original = list(items)
        for i in range(len(items)):
            items[i] = original.pop(self.randrange(len(original)))

class Area:

    def __init__(self, name):
        self.name = name
        self.connections = []
        self.locations = []
        self.difficulty = 1

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def add_location(self, location):
        self.locations.append(location)

    def get_locations(self):
        return self.locations

    def clear_locations(self):
        self.locations = []

    def remove_location(self, location):
        self.locations.remove(location)


class Connection:

    def __init__(self, home, target):
        self.home = home
        self.target = target
        self.keys = 0
        self.mapstone = False
        self.requirements = []
        self.difficulties = []

    def add_requirements(self, req, difficulty):
        if shards:
            match = re.match(".*GinsoKey.*", str(req))
            if match:
                req.remove("GinsoKey")
                req.append("WaterVeinShard")
                req.append("WaterVeinShard")
                req.append("WaterVeinShard")
                req.append("WaterVeinShard")
                req.append("WaterVeinShard")
            match = re.match(".*ForlornKey.*", str(req))
            if match:
                req.remove("ForlornKey")
                req.append("GumonSealShard")
                req.append("GumonSealShard")
                req.append("GumonSealShard")
                req.append("GumonSealShard")
                req.append("GumonSealShard")
            match = re.match(".*HoruKey.*", str(req))
            if match:
                req.remove("HoruKey")
                req.append("SunstoneShard")
                req.append("SunstoneShard")
                req.append("SunstoneShard")
                req.append("SunstoneShard")
                req.append("SunstoneShard")
        self.requirements.append(req)
        self.difficulties.append(difficulty)
        match = re.match(".*KS.*KS.*KS.*KS.*", str(req))
        if match:
            self.keys = 4
            return
        match = re.match(".*KS.*KS.*", str(req))
        if match:
            self.keys = 2
            return
        match = re.match(".*MS.*", str(req))
        if match:
            self.mapstone = True
            return

    def get_requirements(self):
        return self.requirements

    def cost(self):
        minReqScore = 7777
        minDiff = 7777
        minReq = []
        for i in range(0,len(self.requirements)):
            score = 0
            energy = 0
            health = 0
            for abil in self.requirements[i]:
                if abil == "EC":
                    energy += 1
                    if inventory["EC"] < energy:
                        score += costs[abil.strip()]
                elif abil == "HC":
                    health += 1
                    if inventory["HC"] < health:
                        score += costs[abil.strip()]
                else:
                    score += costs[abil.strip()]
            if score < minReqScore:
                minReqScore = score
                minReq = self.requirements[i]
                minDiff = self.difficulties[i]
        return (minReqScore, minReq, minDiff)

class Location:

    factor = 4.0

    def __init__(self, x, y, area, orig, difficulty, zone):
        self.x = int(math.floor((x)/self.factor) * self.factor)
        self.y = int(math.floor((y)/self.factor) * self.factor)
        self.orig = orig
        self.area = area
        self.difficulty = difficulty
        self.zone = zone

    def get_key(self):
        return self.x*10000 + self.y

    def to_string(self):
        return self.area + " " + self.orig + " (" + str(self.x) + " " + str(self.y) + ")"

def open_free_connections():
    global seedDifficulty
    found = False
    keystoneCount = 0
    mapstoneCount = 0
    for area in areaList:
        if area in areasReached.keys():
            for connection in areas[area].get_connections():
                cost = connection.cost()
                if cost[0] <= 0:
                    areas[connection.target].difficulty = cost[2]
                    if connection.keys > 0:
                        if area not in doorQueue.keys():
                            doorQueue[area] = connection
                            keystoneCount += connection.keys
                    elif connection.mapstone:
                        if connection.target not in areasReached:
                            visitMap = True
                            for map in mapQueue.keys():
                                if map == area or mapQueue[map].target == connection.target:
                                    visitMap = False
                            if visitMap:
                                mapQueue[area] = connection
                                mapstoneCount += 1
                    else:
                        if connection.target not in areasReached:
                            currentAreas.append(connection.target)
                            seedDifficulty += cost[2] * cost[2]
                        areasReached[connection.target] = True
                        connectionQueue.append((area, connection))
                        found = True
    return (found, keystoneCount, mapstoneCount)


def get_all_accessible_locations():
    locations = []
    for area in areaList:
        if area in areasReached.keys():
            currentLocations = areas[area].get_locations()
            for location in currentLocations:
                location.difficulty += areas[area].difficulty
            if limitkeys:
                loc = ""
                for location in currentLocations:
                    if location.orig in keySpots.keys():
                        loc = location
                        break
                if loc:
                    force_assign(keySpots[loc.orig], loc)
                    currentLocations.remove(loc)
            locations.extend(currentLocations)
            areas[area].clear_locations()
    if reservedLocations:
        locations.append(reservedLocations.pop(0))
        locations.append(reservedLocations.pop(0))
    if itemCount > 2 and len(locations) >= 2:
        reservedLocations.append(locations.pop(random.randrange(len(locations))))
        reservedLocations.append(locations.pop(random.randrange(len(locations))))
    return locations


def prepare_path(free_space):
    abilities_to_open = {}
    totalCost = 0.0
    # find the sets of abilities we need to get somewhere
    for area in areaList:
        if area in areasReached.keys():
            for connection in areas[area].get_connections():
                if connection.target in areasReached:
                    continue
                if limitkeys and connection.get_requirements() and ("GinsoKey" in connection.get_requirements()[0] or "ForlornKey" in connection.get_requirements()[0] or "HoruKey" in connection.get_requirements()[0]):
                    continue
                for req_set in connection.get_requirements():
                    requirements = []
                    cost = 0
                    energy = 0
                    health = 0
                    waterVeinShard = 0
                    gumonSealShard = 0
                    sunstoneShard = 0
                    for req in req_set:
                        if costs[req] > 0:
                            if req == "EC":
                                energy += 1
                                if energy > inventory["EC"]:
                                    requirements.append(req)
                                    cost += costs[req]
                            elif req == "HC":
                                health += 1
                                if health > inventory["HC"]:
                                    requirements.append(req)
                                    cost += costs[req]
                            elif req == "WaterVeinShard":
                                waterVeinShard += 1
                                if waterVeinShard > inventory["WaterVeinShard"]:
                                    requirements.append(req)
                                    cost += costs[req]
                            elif req == "GumonSealShard":
                                gumonSealShard += 1
                                if gumonSealShard > inventory["GumonSealShard"]:
                                    requirements.append(req)
                                    cost += costs[req]
                            elif req == "SunstoneShard":
                                sunstoneShard += 1
                                if sunstoneShard > inventory["SunstoneShard"]:
                                    requirements.append(req)
                                    cost += costs[req]
                            else:
                                requirements.append(req)
                                cost += costs[req]
                    # cost *= len(requirements) # decrease the rate of multi-ability paths
                    if len(requirements) <= free_space:
                        for req in requirements:
                            if req not in abilities_to_open:
                                abilities_to_open[req] = (cost, requirements)
                            elif abilities_to_open[req][0] > cost:
                                abilities_to_open[req] = (cost, requirements)
    # pick a random path weighted by cost
    for path in abilities_to_open:
        totalCost += 1.0/abilities_to_open[path][0]
    position = 0
    target = random.random() * totalCost
    for path in itemList:
        if path in abilities_to_open.keys():
            position += 1.0/abilities_to_open[path][0]
            if target <= position:
                for req in abilities_to_open[path][1]:
                    if itemPool[req] > 0:
                        assignQueue.append(req)
                return abilities_to_open[path][1]


def assign_random(recurseCount = 0):
    value = random.random()
    position = 0.0
    for key in itemList:
        position += itemPool[key]/itemCount
        if value <= position:
            if starved and key in skillsOutput and recurseCount < 3:
                return assign_random(recurseCount = recurseCount + 1)
            return assign(key)

def assign(item):
    itemPool[item] = max(itemPool[item]-1,0)
    if item == "EC" or item == "KS" or item == "HC":
        if costs[item] > 0:
            costs[item] -= 1
    elif item == "WaterVeinShard" or item == "GumonSealShard" or item == "SunstoneShard":
        if costs[item] > 0:
            costs[item] -= 1
    elif item in costs.keys():
        costs[item] = 0
    inventory[item] += 1
    return item

# for use in limitkeys mode
def force_assign(item, location):

    assign(item)
    assign_to_location(item, location)

def assign_to_location(item, location):

    global outputStr
    global eventList
    global spoilerGroup
    global mapstonesAssigned
    global skillCount
    global expRemaining
    global expSlots

    assignment = ""

    # if mapstones are progressive, set a special location
    if not nonProgressiveMapstones and location.orig == "MapStone":
        mapstonesAssigned += 1
        assignment += (str(20 + mapstonesAssigned * 4) + "|")
        if item in costs.keys():
            if item not in spoilerGroup:
                spoilerGroup[item] = []
            spoilerGroup[item].append(item + " from MapStone " + str(mapstonesAssigned) + "\r\n")
    else:
        assignment += (str(location.get_key()) + "|")
        if item in costs.keys():
            if item not in spoilerGroup:
                spoilerGroup[item] = []
            spoilerGroup[item].append(item + " from " + location.to_string() + "\r\n")

    if item in skillsOutput:
        assignment += (str(skillsOutput[item][:2]) + "|" + skillsOutput[item][2:])
    elif item in eventsOutput:
        assignment += (str(eventsOutput[item][:2]) + "|" + eventsOutput[item][2:])
    elif item == "EX*":
        value = get_random_exp_value(expRemaining, expSlots)
        expRemaining -= value
        expSlots -= 1
        assignment += "EX|" + str(value)
    elif item[2:]:
        assignment += (item[:2] + "|" + item[2:])
    else:
        assignment += (item[:2] + "|1")
    assignment += ("|" + location.zone + "\r\n")

    if item in eventsOutput:
        eventList.append(assignment)
    else:
        outputStr += assignment


def get_random_exp_value(expRemaining, expSlots):

    min = random.randint(2,9)

    if expSlots <= 1:
        return max(expRemaining,min)

    return int(max(expRemaining * (inventory["EX*"] + expSlots / 4) * random.uniform(0.0,2.0) / (expSlots * (expSlots + inventory["EX*"])), min))

def preferred_difficulty_assign(item, locationsToAssign):
    total = 0.0
    for loc in locationsToAssign:
        if pathDifficulty == "easy":
            total += (15 - loc.difficulty) * (15 - loc.difficulty)
        else:
            total += (loc.difficulty * loc.difficulty)
    value = random.random()
    position = 0.0
    for i in range(0,len(locationsToAssign)):
        if pathDifficulty == "easy":
            position += (15 - locationsToAssign[i].difficulty) * (15 - locationsToAssign[i].difficulty)/total
        else:
            position += locationsToAssign[i].difficulty * locationsToAssign[i].difficulty/total
        if value <= position:
            assign_to_location(item, locationsToAssign[i])
            break
    del locationsToAssign[i]

def selectText(selectFrom, selectTo, line):

    return re.match(".*" + selectFrom + "(.*)" + selectTo + ".*", line).group(1)

def placeItems(seed, expPool, hardMode, includePlants, shardsMode, limitkeysMode, cluesMode, noTeleporters, modes, flags, starvedMode, preferPathDifficulty, setNonProgressiveMapstones):

    global costs
    global areas
    global areasReached
    global currentAreas
    global itemCount
    global itemPool
    global assignQueue
    global inventory
    global doorQueue
    global mapQueue
    global connectionQueue
    global outputStr
    global eventList
    global mapstonesAssigned
    global skillCount
    global expRemaining
    global expSlots
    global areaList

    global shards
    global limitkeys
    global clues
    global starved
    global pathDifficulty
    global nonProgressiveMapstones

    shards = shardsMode
    limitkeys = limitkeysMode
    starved = starvedMode
    pathDifficulty = preferPathDifficulty
    nonProgressiveMapstones = setNonProgressiveMapstones

    global skillsOutput
    global eventsOutput

    skillsOutput = {
        "WallJump": "SK3",
        "ChargeFlame": "SK2",
        "Dash": "SK50",
        "Stomp": "SK4",
        "DoubleJump": "SK5",
        "Glide": "SK14",
        "Bash": "SK0",
        "Climb": "SK12",
        "Grenade": "SK51",
        "ChargeJump": "SK8"
    }

    eventsOutput = {
        "GinsoKey": "EV0",
        "Water": "EV1",
        "ForlornKey": "EV2",
        "Wind": "EV3",
        "HoruKey": "EV4",
        "Warmth": "EV5",
        "WaterVeinShard": "RB17",
        "GumonSealShard": "RB19",
        "SunstoneShard": "RB21"
    }

    global seedDifficulty

    seedDifficultyMap = {
        "Dash": 2,
        "Bash": 2,
        "Glide": 3,
        "DoubleJump": 2,
        "ChargeJump": 1
    }
    seedDifficulty = 0

    limitKeysPool = ["SKWallJump", "SKChargeFlame", "SKDash", "SKStomp", "SKDoubleJump", "SKGlide", "SKClimb", "SKGrenade", "SKChargeJump", "EVGinsoKey", "EVForlornKey", "EVHoruKey", "SKBash", "EVWater", "EVWind"]

    difficultyMap = {
        "normal": 1,
        "speed": 2,
        "lure": 2,
        "dboost": 2,
        "dboost-light": 1,
        "dboost-hard": 3,
        "cdash": 2,
        "cdash-farming": 2,
        "dbash": 3,
        "extended": 3,
        "extended-damage": 3,
        "lure-hard": 4,
        "extreme": 4,
        "glitched": 5,
        "timed-level": 5
    }

    outputStr = ""
    eventList = []
    spoilerStr = ""
    groupDepth = 0

    costs = {
        "Free": 0,
        "MS": 0,
        "KS": 2,
        "EC": 6,
        "HC": 12,
        "WallJump": 13,
        "ChargeFlame": 13,
        "DoubleJump": 13,
        "Bash": 41,
        "Stomp": 29,
        "Glide": 17,
        "Climb": 41,
        "ChargeJump": 59,
        "Dash": 13,
        "Grenade": 29,
        "GinsoKey": 12,
        "ForlornKey": 12,
        "HoruKey": 12,
        "Water": 80,
        "Wind": 80,
        "WaterVeinShard": 5,
        "GumonSealShard": 5,
        "SunstoneShard": 5,
        "TPForlorn": 120,
        "TPGrotto": 60,
        "TPSorrow": 90,
        "TPGrove": 60,
        "TPSwamp": 60,
        "TPValley": 90
    }

    areas = {}

    areasReached = {"SunkenGladesRunaway": True}
    currentAreas = ["SunkenGladesRunaway"]
    areaList = []
    connectionQueue = []
    assignQueue = []

    itemCount = 244.0
    expRemaining = expPool
    keystoneCount = 0
    mapstoneCount = 0

    if not hardMode:
        itemPool = {
            "EX1": 1,
            "EX*": 93,
            "KS": 40,
            "MS": 9,
            "AC": 33,
            "EC": 14,
            "HC": 12,
            "WallJump": 1,
            "ChargeFlame": 1,
            "Dash": 1,
            "Stomp": 1,
            "DoubleJump": 1,
            "Glide": 1,
            "Bash": 1,
            "Climb": 1,
            "Grenade": 1,
            "ChargeJump": 1,
            "GinsoKey": 1,
            "ForlornKey": 1,
            "HoruKey": 1,
            "Water": 1,
            "Wind": 1,
            "Warmth": 1,
            "RB0": 3,
            "RB1": 3,
            "RB6": 3,
            "RB8": 1,
            "RB9": 1,
            "RB10": 1,
            "RB11": 1,
            "RB12": 1,
            "RB13": 3,
            "RB15": 3,
            "WaterVeinShard": 0,
            "GumonSealShard": 0,
            "SunstoneShard": 0,
            "TPForlorn": 1,
            "TPGrotto": 1,
            "TPSorrow": 1,
            "TPGrove": 1,
            "TPSwamp": 1,
            "TPValley": 1
        }
    else:
        itemPool = {
            "EX1": 1,
            "EX*": 169,
            "KS": 40,
            "MS": 9,
            "AC": 0,
            "EC": 3,
            "HC": 0,
            "WallJump": 1,
            "ChargeFlame": 1,
            "Dash": 1,
            "Stomp": 1,
            "DoubleJump": 1,
            "Glide": 1,
            "Bash": 1,
            "Climb": 1,
            "Grenade": 1,
            "ChargeJump": 1,
            "GinsoKey": 1,
            "ForlornKey": 1,
            "HoruKey": 1,
            "Water": 1,
            "Wind": 1,
            "Warmth": 1,
            "WaterVeinShard": 0,
            "GumonSealShard": 0,
            "SunstoneShard": 0,
            "TPForlorn": 1,
            "TPGrotto": 1,
            "TPSorrow": 1,
            "TPGrove": 1,
            "TPSwamp": 1,
            "TPValley": 1
        }

    plants = []
    if not includePlants:
        itemCount -= 24
        itemPool["EX*"] -= 24

    if shards:
        itemPool["WaterVeinShard"] = 5
        itemPool["GumonSealShard"] = 5
        itemPool["SunstoneShard"] = 5
        itemPool["GinsoKey"] = 0
        itemPool["ForlornKey"] = 0
        itemPool["HoruKey"] = 0
        itemPool["EX*"] -= 12

    if limitkeys:
        satisfied = False
        while not satisfied:
            ginso = random.randint(0,12)
            if ginso == 12:
                ginso = 14
            forlorn = random.randint(0,13)
            horu = random.randint(0,14)
            if ginso != forlorn and ginso != horu and forlorn != horu and ginso+forlorn < 26:
                satisfied = True
        global keySpots
        keySpots = {limitKeysPool[ginso]:"GinsoKey", limitKeysPool[forlorn]:"ForlornKey", limitKeysPool[horu]:"HoruKey"}
        itemPool["GinsoKey"] = 0
        itemPool["ForlornKey"] = 0
        itemPool["HoruKey"] = 0
        itemCount -= 3

    if noTeleporters:
        itemPool["TPForlorn"] = 0
        itemPool["TPGrotto"] = 0
        itemPool["TPSorrow"] = 0
        itemPool["TPGrove"] = 0
        itemPool["TPSwamp"] = 0
        itemPool["TPValley"] = 0
        itemPool["EX*"] += 6

    inventory = {
        "EX1": 0,
        "EX*": 0,
        "KS": 0,
        "MS": 0,
        "AC": 0,
        "EC": 1,
        "HC": 3,
        "WallJump": 0,
        "ChargeFlame": 0,
        "Dash": 0,
        "Stomp": 0,
        "DoubleJump": 0,
        "Glide": 0,
        "Bash": 0,
        "Climb": 0,
        "Grenade": 0,
        "ChargeJump": 0,
        "GinsoKey": 0,
        "ForlornKey": 0,
        "HoruKey": 0,
        "Water": 0,
        "Wind": 0,
        "Warmth": 0,
        "RB0": 0,
        "RB1": 0,
        "RB6": 0,
        "RB8": 0,
        "RB9": 0,
        "RB10": 0,
        "RB11": 0,
        "RB12": 0,
        "RB13": 0,
        "RB15": 0,
        "WaterVeinShard": 0,
        "GumonSealShard": 0,
        "SunstoneShard": 0,
        "TPForlorn": 1,
        "TPGrotto": 1,
        "TPSorrow": 1,
        "TPGrove": 1,
        "TPSwamp": 1,
        "TPValley": 1
    }

    lines = '<?xml version="1.0"?>\n<Areas>\n  <Area name="SunkenGladesRunaway">\n    <Locations>\n      <Location>\n        <X>92</X>\n        <Y>-227</Y>\n        <Item>EX15</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-154</X>\n        <Y>-271</Y>\n        <Item>EX15</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>83</X>\n        <Y>-222</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-11</X>\n        <Y>-206</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="SunkenGladesNadePool"/>\n        <Requirements>\n          <Requirement mode="normal">Water+Grenade</Requirement>\n          <Requirement mode="dboost">Grenade+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">Grenade+HC+HC+HC+HC+HC+Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="SunkenGladesNadeTree"/>\n        <Requirements>\n          <Requirement mode="speed">Grenade+WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Grenade+ChargeJump</Requirement>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="SunkenGladesMainPool"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">Bash</Requirement>\n          <Requirement mode="dboost">Stomp</Requirement>\n          <Requirement mode="dboost">HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="SunkenGladesMainPoolDeep"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">HC+HC+HC+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="WallJump"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="DashArea"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="FronkeyWalkRoof"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="lure">Bash</Requirement>\n          <Requirement mode="normal">Glide+Wind</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="Forlorn"/>\n        <Requirements>\n          <Requirement mode="dboost-light">ForlornKey+TPForlorn+DoubleJump+ChargeJump</Requirement>\n          <Requirement mode="dboost-light">ForlornKey+TPForlorn+DoubleJump+Bash</Requirement>\n          <Requirement mode="dboost-light">ForlornKey+TPForlorn+Glide+ChargeJump</Requirement>\n          <Requirement mode="dboost-light">ForlornKey+TPForlorn+Glide+Bash</Requirement>\n          <Requirement mode="dboost-light">ForlornKey+TPForlorn+Grenade+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="MoonGrotto"/>\n        <Requirements>\n          <Requirement mode="normal">TPGrotto+ChargeJump</Requirement>\n          <Requirement mode="normal">TPGrotto+WallJump</Requirement>\n          <Requirement mode="normal">TPGrotto+Climb</Requirement>\n          <Requirement mode="normal">TPGrotto+Grenade+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="GumoHideoutMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">TPGrotto+MS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="HollowGrove"/>\n        <Requirements>\n          <Requirement mode="normal">TPSwamp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="SpiritTreeRefined"/>\n        <Requirements>\n          <Requirement mode="normal">TPGrove</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="ValleyRight"/>\n        <Requirements>\n          <Requirement mode="normal">TPValley+Bash+WallJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SunkenGladesRunaway"/>\n        <Target name="Sunstone"/>\n        <Requirements>\n          <Requirement mode="normal">TPSorrow+Glide+Climb+ChargeJump+Stomp</Requirement>\n          <Requirement mode="extended-damage">TPSorrow+Glide+Stomp+ChargeJump+Dash+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dbash">TPSorrow+Glide+Stomp+Bash</Requirement>\n          <Requirement mode="dbash">TPSorrow+Glide+ChargeJump+Bash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="SunkenGladesNadePool">\n    <Locations>\n      <Location>\n        <X>59</X>\n        <Y>-280</Y>\n        <Item>EX200</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SunkenGladesNadeTree">\n    <Locations>\n      <Location>\n        <X>82</X>\n        <Y>-196</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SunkenGladesMainPool">\n    <Locations>\n      <Location>\n        <X>5</X>\n        <Y>-241</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SunkenGladesMainPoolDeep">\n    <Locations>\n      <Location>\n        <X>-40</X>\n        <Y>-239</Y>\n        <Item>EC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="FronkeyWalkRoof">\n    <Locations>\n      <Location>\n        <X>257</X>\n        <Y>-199</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="WallJump">\n    <Locations>\n      <Location>\n        <X>-80</X>\n        <Y>-189</Y>\n        <Item>HC</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-59</X>\n        <Y>-244</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-316</X>\n        <Y>-308</Y>\n        <Item>SKWallJump</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-283</X>\n        <Y>-236</Y>\n        <Item>EX15</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="DeathGauntlet"/>\n        <Requirements>\n          <Requirement mode="dboost-light">EC+EC+EC+EC+WallJump</Requirement>\n          <Requirement mode="dboost-light">EC+EC+EC+EC+Climb</Requirement>\n          <Requirement mode="dboost-light">EC+EC+EC+EC+ChargeJump+Bash</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+Grenade+Bash</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+Climb+DoubleJump+Glide</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+WallJump+DoubleJump+Glide</Requirement>\n          <Requirement mode="timed-level">EC+EC+WallJump</Requirement>\n          <Requirement mode="timed-level">EC+EC+Climb</Requirement>\n          <Requirement mode="timed-level">EC+EC+ChargeJump+Bash</Requirement>\n          <Requirement mode="timed-level">EC+EC+Grenade+Bash</Requirement>\n          <Requirement mode="lure">EC+EC+EC+EC+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="AboveFourthHealth"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+WallJump</Requirement>\n          <Requirement mode="normal">Bash+Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="speed">WallJump+DoubleJump</Requirement>\n          <Requirement mode="extended">Climb+DoubleJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="RightWallJump"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="lure-hard">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="LeftWallJump"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="lure-hard">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="SpiritCaverns"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+Climb</Requirement>\n          <Requirement mode="normal">KS+KS+WallJump</Requirement>\n          <Requirement mode="normal">KS+KS+ChargeJump</Requirement>\n          <Requirement mode="normal">KS+KS+Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="GladesLaser"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+Climb</Requirement>\n          <Requirement mode="normal">ChargeJump+WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Bash+DoubleJump+Glide</Requirement>\n          <Requirement mode="normal">Bash+DoubleJump+WallJump</Requirement>\n          <Requirement mode="normal">Bash+DoubleJump+Climb</Requirement>\n          <Requirement mode="normal">Bash+Grenade+Climb</Requirement>\n          <Requirement mode="normal">Bash+Grenade+WallJump</Requirement>\n          <Requirement mode="lure">Bash+WallJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n          <Requirement mode="cdash-farming">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="ChargeFlame"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+Grenade</Requirement>\n          <Requirement mode="normal">WallJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">Climb+Grenade</Requirement>\n          <Requirement mode="normal">Climb+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+Grenade</Requirement>\n          <Requirement mode="normal">ChargeJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="glitched">Dash+Bash+WallJump</Requirement>\n          <Requirement mode="glitched">Dash+Bash+Climb</Requirement>\n          <Requirement mode="glitched">Dash+WallJump+DoubleJump</Requirement>\n          <Requirement mode="glitched">Dash+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="ChargeFlameOrb"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="WallJump"/>\n        <Target name="WallJumpMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="DeathGauntlet">\n    <Locations>\n      <Location>\n        <X>303</X>\n        <Y>-190</Y>\n        <Item>EX100</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="DeathGauntlet"/>\n        <Target name="DeathStomp"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+Water</Requirement>\n          <Requirement mode="dboost">Stomp</Requirement>\n          <Requirement mode="extended-damage">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DeathGauntlet"/>\n        <Target name="DeathGauntletRoof"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DeathGauntlet"/>\n        <Target name="DeathWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water+EC+EC+EC+EC</Requirement>\n          <Requirement mode="dboost">EC+EC+EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DeathGauntlet"/>\n        <Target name="MoonGrotto"/>\n        <Requirements>\n          <Requirement mode="dboost-light">WallJump</Requirement>\n          <Requirement mode="dboost-light">Climb</Requirement>\n          <Requirement mode="dboost-light">ChargeJump+Bash</Requirement>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n          <Requirement mode="normal">Climb+DoubleJump+Glide</Requirement>\n          <Requirement mode="normal">WallJump+DoubleJump+Glide</Requirement>\n          <Requirement mode="timed-level">WallJump</Requirement>\n          <Requirement mode="timed-level">Climb</Requirement>\n          <Requirement mode="timed-level">ChargeJump+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DeathGauntlet"/>\n        <Target name="SunkenGladesRunaway"/>\n        <Requirements>\n          <Requirement mode="normal">DoubleJump+EC+EC+EC+EC</Requirement>\n          <Requirement mode="normal">Glide+EC+EC+EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="WallJumpMapStone">\n    <Locations>\n      <Location>\n        <X>-81</X>\n        <Y>-248</Y>\n        <Item>MapStone</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="AboveFourthHealth">\n    <Locations>\n      <Location>\n        <X>-48</X>\n        <Y>-166</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightWallJump">\n    <Locations>\n      <Location>\n        <X>-245</X>\n        <Y>-277</Y>\n        <Item>EX200</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LeftWallJump">\n    <Locations>\n      <Location>\n        <X>-336</X>\n        <Y>-288</Y>\n        <Item>EC</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-247</X>\n        <Y>-207</Y>\n        <Item>EX15</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-238</X>\n        <Y>-212</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-184</X>\n        <Y>-227</Y>\n        <Item>MS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiritCaverns">\n    <Locations>\n      <Location>\n        <X>-182</X>\n        <Y>-193</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-217</X>\n        <Y>-183</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n      <Location>\n        <X>-177</X>\n        <Y>-154</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="SpiritCaverns"/>\n        <Target name="SpiritCavernsTopLeft"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">DoubleJump</Requirement>\n          <Requirement mode="dboost-light">ChargeJump</Requirement>\n          <Requirement mode="dboost-light">Bash</Requirement>\n          <Requirement mode="extreme">Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiritCaverns"/>\n        <Target name="GladesLaser"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+EC+EC+DoubleJump</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+Bash</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+ChargeJump</Requirement>\n          <Requirement mode="cdash-farming">EC+EC+EC+EC+Dash</Requirement>\n          <Requirement mode="extended-damage">EC+EC+EC+EC+WallJump+Glide</Requirement>\n          <Requirement mode="glitched">EC+EC+EC+DoubleJump</Requirement>\n          <Requirement mode="glitched">EC+EC+EC+Bash</Requirement>\n          <Requirement mode="glitched">EC+EC+EC+ChargeJump</Requirement>\n          <Requirement mode="glitched">EC+EC+EC+Dash</Requirement>\n          <Requirement mode="glitched">EC+EC+EC+WallJump+Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiritCaverns"/>\n        <Target name="SpiritCavernsAC"/>\n        <Requirements>\n          <Requirement mode="speed">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiritCaverns"/>\n        <Target name="SpiritTreeRefined"/>\n        <Requirements>\n          <!-- will cause some painted-into-corner scenarios, revisit this if it is too much -->\n          <Requirement mode="normal">KS+KS+KS+KS</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="SpiritCavernsTopLeft">\n    <Locations>\n      <Location>\n        <X>-217</X>\n        <Y>-146</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiritCavernsAC">\n    <Locations>\n      <Location>\n        <X>-216</X>\n        <Y>-176</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="GladesLaser">\n    <Locations>\n      <Location>\n        <X>-155</X>\n        <Y>-186</Y>\n        <Item>EC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="GladesLaser"/>\n        <Target name="WallJump"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GladesLaser"/>\n        <Target name="SpiritCaverns"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+EC+EC</Requirement>\n          <Requirement mode="timed-level">EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GladesLaser"/>\n        <Target name="GladesLaserGrenade"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade+Bash+WallJump</Requirement>\n          <Requirement mode="normal">Grenade+Bash+Climb</Requirement>\n          <Requirement mode="extended">Grenade+ChargeJump+Water</Requirement>\n          <Requirement mode="extended-damage">Grenade+ChargeJump</Requirement>\n          <Requirement mode="cdash">Grenade+Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="GladesLaserGrenade">\n    <Locations>\n      <Location>\n        <X>-165</X>\n        <Y>-140</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ChargeFlame">\n    <Locations>\n      <Location>\n        <X>-56</X>\n        <Y>-160</Y>\n        <Item>SKChargeFlame</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="ChargeFlame"/>\n        <Target name="SpiritTreeRefined"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+Grenade</Requirement>\n          <Requirement mode="speed">ChargeJump+Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ChargeFlame"/>\n        <Target name="ChargeFlamePlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash-farming">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ChargeFlame"/>\n        <Target name="WallJump"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="normal">Stomp+WallJump</Requirement>\n          <Requirement mode="normal">Stomp+Climb</Requirement>\n          <Requirement mode="normal">Stomp+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ChargeFlame"/>\n        <Target name="ChargeFlameOrb"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ChargeFlamePlant">\n    <Locations>\n      <Location>\n        <X>43</X>\n        <Y>-156</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ChargeFlameOrb">\n    <Locations>\n      <Location>\n        <X>4</X>\n        <Y>-196</Y>\n        <Item>EX100</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Glades</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiritTreeRefined">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="SpiritTreeRefined"/>\n        <Target name="ChargeFlame"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiritTreeRefined"/>\n        <Target name="ValleyEntry"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="normal">Stomp+WallJump</Requirement>\n          <Requirement mode="normal">Stomp+Climb</Requirement>\n          <Requirement mode="normal">Stomp+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiritTreeRefined"/>\n        <Target name="ChargeFlameTree"/>\n        <Requirements>\n          <Requirement mode="normal">DoubleJump+Climb</Requirement>\n          <Requirement mode="normal">DoubleJump+WallJump</Requirement>\n          <Requirement mode="normal">ChargeJump+Climb</Requirement>\n          <Requirement mode="normal">ChargeJump+WallJump</Requirement>\n          <Requirement mode="normal">ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeJump+Glide</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="speed">Dash+WallJump</Requirement>\n          <Requirement mode="speed">Dash+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiritTreeRefined"/>\n        <Target name="SpiderSac"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame+WallJump</Requirement>\n          <Requirement mode="normal">ChargeFlame+ChargeJump</Requirement>\n          <Requirement mode="normal">ChargeFlame+Climb+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeFlame+Climb+Glide</Requirement>\n          <Requirement mode="normal">ChargeFlame+Climb+Dash</Requirement>\n          <Requirement mode="normal">Grenade+WallJump</Requirement>\n          <Requirement mode="normal">Grenade+ChargeJump</Requirement>\n          <Requirement mode="normal">Grenade+Climb+DoubleJump</Requirement>\n          <Requirement mode="normal">Grenade+Climb+Glide</Requirement>\n          <Requirement mode="normal">Grenade+Climb+Dash</Requirement>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n          <Requirement mode="extended">ChargeFlame+Climb</Requirement>\n          <Requirement mode="extended">Grenade+Climb</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ChargeFlameTree">\n    <Locations>\n      <Location>\n        <X>-14</X>\n        <Y>-95</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiderSac">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="SpiderSacHealth"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="SpiderSacEnergy"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">DoubleJump</Requirement>\n          <Requirement mode="normal">Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="SpiderSacGrenadeDoor"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n          <Requirement mode="normal">Grenade+DoubleJump+WallJump</Requirement>\n          <Requirement mode="normal">Grenade+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="SpiderSacEnergyDoor"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+EC+EC</Requirement>\n          <!-- you can level up with the spider exp -->\n          <Requirement mode="timed-level">EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="HollowGrove"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">DoubleJump</Requirement>\n          <Requirement mode="normal">Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="DeathGauntletRoof"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+Water</Requirement>\n          <Requirement mode="dboost">Stomp+Bash+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">Stomp+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="SpiritTreeRefined"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame+WallJump</Requirement>\n          <Requirement mode="normal">ChargeFlame+Climb</Requirement>\n          <Requirement mode="normal">ChargeFlame+ChargeJump</Requirement>\n          <Requirement mode="normal">Grenade+WallJump</Requirement>\n          <Requirement mode="normal">Grenade+Climb</Requirement>\n          <Requirement mode="normal">Grenade+ChargeJump</Requirement>\n          <Requirement mode="normal">Stomp+WallJump</Requirement>\n          <Requirement mode="normal">Stomp+Climb</Requirement>\n          <Requirement mode="normal">Stomp+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SpiderSac"/>\n        <Target name="ChargeFlameTree"/>\n        <Requirements>\n          <Requirement mode="extended">ChargeFlame+Glide</Requirement>\n          <Requirement mode="extended">Grenade+Glide</Requirement>\n          <Requirement mode="extended">Stomp+Glide</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="SpiderSacEnergyDoor">\n    <Locations>\n      <Location>\n        <X>64</X>\n        <Y>-109</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiderSacHealth">\n    <Locations>\n      <Location>\n        <X>151</X>\n        <Y>-117</Y>\n        <Item>HC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiderSacEnergy">\n    <Locations>\n      <Location>\n        <X>60</X>\n        <Y>-155</Y>\n        <Item>EC</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SpiderSacGrenadeDoor">\n    <Locations>\n      <Location>\n        <X>93</X>\n        <Y>-92</Y>\n        <Item>AC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DashArea">\n    <Locations>\n      <Location>\n        <X>154</X>\n        <Y>-291</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n      <Location>\n        <X>183</X>\n        <Y>-291</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n      <Location>\n        <X>197</X>\n        <Y>-229</Y>\n        <Item>EX100</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n      <Location>\n        <X>292</X>\n        <Y>-256</Y>\n        <Item>SKDash</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="DashArea"/>\n        <Target name="DeathGauntlet"/>\n        <Requirements>\n          <Requirement mode="dboost-light">EC+EC+EC+EC+WallJump</Requirement>\n          <Requirement mode="dboost-light">EC+EC+EC+EC+Climb</Requirement>\n          <Requirement mode="dboost-light">EC+EC+EC+EC+ChargeJump+Bash</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+Grenade+Bash</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+Climb+DoubleJump+Glide</Requirement>\n          <Requirement mode="normal">EC+EC+EC+EC+WallJump+DoubleJump+Glide</Requirement>\n          <Requirement mode="timed-level">EC+EC+WallJump</Requirement>\n          <Requirement mode="timed-level">EC+EC+Climb</Requirement>\n          <Requirement mode="timed-level">EC+EC+ChargeJump+Bash</Requirement>\n          <Requirement mode="timed-level">EC+EC+Grenade+Bash</Requirement>\n          <Requirement mode="lure">EC+EC+EC+EC+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DashArea"/>\n        <Target name="LowerBlackRoot"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+ChargeJump</Requirement>\n          <Requirement mode="normal">Stomp+Grenade+Bash</Requirement>\n          <Requirement mode="normal">Stomp+Dash+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+Dash+Grenade+Bash</Requirement>\n          <Requirement mode="normal">Stomp+Dash</Requirement>\n          <Requirement mode="normal">Stomp+ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+Grenade</Requirement>\n          <Requirement mode="normal">Stomp+Grenade+Water</Requirement>\n          <Requirement mode="timed-level">Stomp</Requirement>\n          <Requirement mode="extended">Stomp</Requirement>\n          <Requirement mode="extended">ChargeJump+Climb</Requirement>\n          <Requirement mode="extreme">Bash</Requirement>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DashArea"/>\n        <Target name="RazielNo"/>\n        <Requirements>\n          <Requirement mode="normal">Dash+WallJump</Requirement>\n          <Requirement mode="normal">Dash+ChargeJump</Requirement>\n          <Requirement mode="normal">Dash+Bash+Grenade</Requirement>\n          <Requirement mode="normal">Dash+Climb+DoubleJump</Requirement>\n          <Requirement mode="speed">WallJump</Requirement>\n          <Requirement mode="speed">ChargeJump</Requirement>\n          <Requirement mode="speed">Bash+Grenade</Requirement>\n          <Requirement mode="speed">Climb+DoubleJump</Requirement>\n          <Requirement mode="extended">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DashArea"/>\n        <Target name="BlackrootMap"/>\n        <Requirements>\n          <Requirement mode="normal">Dash</Requirement>\n          <Requirement mode="extended">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DashArea"/>\n        <Target name="DashAreaPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+Climb+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+WallJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">Glide+WallJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+Climb+Grenade</Requirement>\n          <Requirement mode="normal">ChargeJump+WallJump+Grenade</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="normal">Glide+WallJump+Grenade</Requirement>\n          <Requirement mode="extended">DoubleJump+Grenade</Requirement>\n          <Requirement mode="extended">DoubleJump+ChargeFlame</Requirement>\n          <Requirement mode="cdash-farming">ChargeJump+Climb+Dash</Requirement>\n          <Requirement mode="cdash-farming">ChargeJump+WallJump+Dash</Requirement>\n          <Requirement mode="cdash-farming">DoubleJump+Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="DashAreaPlant">\n    <Locations>\n      <Location>\n        <X>313</X>\n        <Y>-232</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RazielNo">\n    <Locations>\n      <Location>\n        <X>304</X>\n        <Y>-303</Y>\n        <Item>EX100</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="RazielNo"/>\n        <Target name="BoulderExp"/>\n        <Requirements>\n          <Requirement mode="normal">Dash+Stomp</Requirement>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="RazielNo"/>\n        <Target name="BlackrootGrottoConnection"/>\n        <Requirements>\n          <Requirement mode="normal">Dash+DoubleJump</Requirement>\n          <Requirement mode="normal">Dash+ChargeJump</Requirement>\n          <Requirement mode="normal">Dash+Bash+Grenade</Requirement>\n          <Requirement mode="extended">WallJump</Requirement>\n          <Requirement mode="extended">DoubleJump</Requirement>\n          <Requirement mode="extended">ChargeJump</Requirement>\n          <Requirement mode="extended">Dash</Requirement>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="RazielNo"/>\n        <Target name="GumoHideout"/>\n        <Requirements>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="BlackrootMap">\n    <Locations>\n      <Location>\n        <X>346</X>\n        <Y>-255</Y>\n        <Item>MS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="BlackrootGrottoConnection">\n    <Locations>\n      <Location>\n        <X>394</X>\n        <Y>-309</Y>\n        <Item>HC</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="BlackrootGrottoConnection"/>\n        <Target name="SideFallCell"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="BlackrootGrottoConnection"/>\n        <Target name="BlackrootMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="BlackrootMapStone">\n    <Locations>\n      <Location>\n        <X>418</X>\n        <Y>-291</Y>\n        <Item>MapStone</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="BoulderExp">\n    <Locations>\n      <Location>\n        <X>432</X>\n        <Y>-324</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LowerBlackRoot">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="LowerBlackRoot"/>\n        <Target name="LowerBlackRootCell"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerBlackRoot"/>\n        <Target name="FarRightBlackRoot"/>\n        <Requirements>\n          <Requirement mode="speed">Dash+DoubleJump</Requirement>\n          <Requirement mode="normal">Dash+Grenade+Bash</Requirement>\n          <Requirement mode="extended">DoubleJump</Requirement>\n          <Requirement mode="extended">Grenade+Bash</Requirement>\n          <!-- for extended mode, this and the right blackroot connection can be done without dash, using a laser crouch -->\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerBlackRoot"/>\n        <Target name="RightBlackRoot"/>\n        <Requirements>\n          <Requirement mode="normal">Dash</Requirement>\n          <Requirement mode="extended">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerBlackRoot"/>\n        <Target name="LeftBlackRoot"/>\n        <Requirements>\n          <Requirement mode="speed">ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n           <Requirement mode="timed-level">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerBlackRoot"/>\n        <Target name="BottomBlackRoot"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerBlackRoot"/>\n        <Target name="GrenadeArea"/>\n        <Requirements>\n          <Requirement mode="normal">Dash</Requirement>\n          <Requirement mode="extended">ChargeJump+Climb+Grenade</Requirement>\n          <Requirement mode="extended">Bash+Grenade</Requirement>\n          <Requirement mode="extended">DoubleJump</Requirement>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="GrenadeArea">\n    <Locations>\n      <Location>\n        <X>72</X>\n        <Y>-380</Y>\n        <Item>SKGrenade</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="GrenadeArea"/>\n        <Target name="RightGrenadeArea"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">DoubleJump</Requirement>\n          <Requirement mode="normal">Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GrenadeArea"/>\n        <Target name="UpperGrenadeArea"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n          <Requirement mode="normal">Grenade+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="RightGrenadeArea">\n    <Locations>\n      <Location>\n        <X>224</X>\n        <Y>-359</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="UpperGrenadeArea">\n    <Locations>\n      <Location>\n        <X>252</X>\n        <Y>-331</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LowerBlackRootCell">\n    <Locations>\n      <Location>\n        <X>279</X>\n        <Y>-375</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="FarRightBlackRoot">\n    <Locations>\n      <Location>\n        <X>391</X>\n        <Y>-423</Y>\n        <Item>AC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightBlackRoot">\n    <Locations>\n      <Location>\n        <X>339</X>\n        <Y>-418</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LeftBlackRoot">\n    <Locations>\n      <Location>\n        <X>208</X>\n        <Y>-431</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="BottomBlackRoot">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="BottomBlackRoot"/>\n        <Target name="FinalBlackRoot"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="extended-damage">Grenade+ChargeJump+Dash+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">Grenade+ChargeJump+Glide+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">Grenade+ChargeJump+DoubleJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="BottomBlackRoot"/>\n        <Target name="BlackRootWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost-hard">HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="FinalBlackRoot">\n    <Locations>\n      <Location>\n        <X>459</X>\n        <Y>-506</Y>\n        <Item>AC</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n      <Location>\n        <X>462</X>\n        <Y>-489</Y>\n        <Item>EX100</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n      <Location>\n        <X>307</X>\n        <Y>-525</Y>\n        <Item>EX100</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="BlackRootWater">\n    <Locations>\n      <Location>\n        <X>527</X>\n        <Y>-544</Y>\n        <Item>AC</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Blackroot</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HollowGrove">\n    <Locations>\n      <Location>\n        <X>300</X>\n        <Y>-94</Y>\n        <Item>MS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="MoonGrotto"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="DeathGauntlet"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="DeathGauntletRoof"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">WallJump+Stomp+Water</Requirement>\n          <Requirement mode="normal">Climb+Stomp+Water</Requirement>\n          <Requirement mode="normal">Bash+Stomp+Water</Requirement>\n          <Requirement mode="dboost">Stomp+Bash+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">WallJump+Stomp+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">Climb+Stomp+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">WallJump+Stomp</Requirement>\n          <Requirement mode="extreme">Climb+Stomp</Requirement>\n          <Requirement mode="extreme">WallJump+Bash</Requirement>\n          <Requirement mode="extreme">Climb+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="SpiderSac"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+Bash</Requirement>\n          <Requirement mode="normal">Climb+Bash</Requirement>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Climb+DoubleJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="GroveWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">HC+HC+HC+HC+HC+Bash</Requirement>\n          <Requirement mode="extreme">Bash</Requirement>\n          <Requirement mode="extreme">HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="UpperGroveSpiderArea"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+WallJump</Requirement>\n          <Requirement mode="normal">ChargeJump+WallJump+DoubleJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="LeftGinsoCell"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+DoubleJump+Glide</Requirement>\n          <Requirement mode="normal">Wind+Glide</Requirement>\n          <Requirement mode="extended">Grenade+Bash</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="GroveWaterStomp"/>\n        <Requirements>\n          <Requirement mode="normal">Water+Stomp</Requirement>\n          <Requirement mode="dboost">Stomp+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="lure-hard">Bash+Water</Requirement>\n          <Requirement mode="lure-hard">Bash+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">Stomp</Requirement>\n          <Requirement mode="extreme">Bash</Requirement>\n          <Requirement mode="glitched">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="RightGinsoOrb"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade+WallJump</Requirement>\n          <Requirement mode="normal">Grenade+Climb</Requirement>\n          <Requirement mode="normal">Grenade+ChargeJump</Requirement>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="LowerGinsoTree"/>\n        <Requirements>\n          <Requirement mode="normal">GinsoKey+WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">GinsoKey+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="HoruFields"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+DoubleJump</Requirement>\n          <Requirement mode="normal">Bash+Glide</Requirement>\n          <Requirement mode="normal">Stomp+ChargeJump+Glide+WallJump</Requirement>\n          <Requirement mode="normal">Stomp+ChargeJump+Glide+Climb</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="HoruFieldsStomp"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="lure">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="HollowGroveMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="HollowGrovePlants"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash-farming">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HollowGrove"/>\n        <Target name="HollowGroveTree"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Wind+Glide</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="lure">Bash+WallJump</Requirement>\n          <Requirement mode="lure">Bash+Climb</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="MoonGrotto">\n    <Locations>\n      <Location>\n        <X>423</X>\n        <Y>-169</Y>\n        <Item>EC</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>703</X>\n        <Y>-82</Y>\n        <Item>AC</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n      <Location>\n        <X>618</X>\n        <Y>-98</Y>\n        <Item>EX100</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="HollowGrove"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Climb+DoubleJump</Requirement>\n          <Requirement mode="normal">Grenade+Bash</Requirement>\n          <Requirement mode="extended">WallJump</Requirement>\n          <Requirement mode="extended">Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="DeathGauntlet"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="UpperGrottoOrbs"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="extreme">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="UpperGrotto200"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Climb+DoubleJump+ChargeJump</Requirement>\n          <Requirement mode="extended">Grenade+Bash</Requirement>\n          <Requirement mode="dboost">ChargeJump</Requirement>\n          <Requirement mode="extreme">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="MortarCell"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="extreme">WallJump+DoubleJump</Requirement>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="SwampGrottoWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="Swamp"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+ChargeJump</Requirement>\n          <Requirement mode="normal">ChargeJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+Grenade</Requirement>\n          <Requirement mode="lure">Bash+ChargeFlame+Water</Requirement>\n          <Requirement mode="lure">Bash+Grenade+Water</Requirement>\n          <Requirement mode="lure">Bash+Climb</Requirement>\n          <Requirement mode="lure">Bash+WallJump</Requirement>\n          <Requirement mode="lure">Bash+Grenade</Requirement>\n          <Requirement mode="lure">Bash+ChargeJump</Requirement>\n          <Requirement mode="extended">ChargeJump+Climb</Requirement>\n          <Requirement mode="extended">DoubleJump+ChargeFlame+Dash+Water</Requirement>\n          <Requirement mode="extended">DoubleJump+ChargeFlame+Glide+Water</Requirement>\n          <Requirement mode="extended-damage">DoubleJump+ChargeFlame+Water+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">Dash+Stomp+ChargeFlame+Water+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost-hard">DoubleJump+ChargeFlame+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost-hard">Stomp+ChargeFlame+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">DoubleJump+ChargeFlame+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">Stomp+ChargeFlame+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="glitched">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="DrainExp"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade+Climb+ChargeJump</Requirement>\n          <Requirement mode="speed">Grenade+Bash</Requirement>\n          <Requirement mode="extended-damage">ChargeFlame+Climb+ChargeJump</Requirement>\n          <Requirement mode="extended-damage">ChargeFlame+DoubleJump</Requirement>\n          <Requirement mode="dbash">ChargeFlame+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="SwampEnergy"/>\n        <Requirements>\n          <Requirement mode="glitched">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="DrainlessCell"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="extended">ChargeJump+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="RightGrottoHealth"/>\n        <Requirements>\n          <Requirement mode="normal">DoubleJump+Bash</Requirement>\n          <Requirement mode="normal">DoubleJump+ChargeJump</Requirement>\n          <Requirement mode="normal">Glide+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="MoonGrottoEnergyWater"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+Water</Requirement>\n          <Requirement mode="dboost">EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="MoonGrottoEnergyTop"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+ChargeJump</Requirement>\n          <Requirement mode="normal">EC+EC+WallJump+DoubleJump</Requirement>\n          <Requirement mode="speed">EC+EC+WallJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="GumoHideout"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="MoonGrottoAirOrb"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="SwampPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="MoonGrottoStompPlant"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+ChargeFlame</Requirement>\n          <Requirement mode="normal">Stomp+Grenade</Requirement>\n          <Requirement mode="cdash">Stomp+Dash</Requirement>\n          <Requirement mode="extended">ChargeFlame</Requirement>\n          <Requirement mode="extreme">Bash+Grenade</Requirement>\n          <Requirement mode="extreme">Bash+Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="SwampMortarPlant"/>\n        <Requirements>\n          <Requirement mode="normal">DoubleJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">DoubleJump+Grenade</Requirement>\n          <Requirement mode="normal">ChargeJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+Grenade</Requirement>\n          <Requirement mode="normal">Bash+ChargeFlame</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="normal">Glide+ChargeFlame</Requirement>\n          <Requirement mode="normal">Glide+Grenade</Requirement>\n          <Requirement mode="speed">Dash+ChargeFlame</Requirement>\n          <Requirement mode="speed">Dash+Grenade</Requirement>\n          <Requirement mode="extended">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MoonGrotto"/>\n        <Target name="DeathGauntletRoofPlant"/>\n        <Requirements>\n          <Requirement mode="extended">ChargeFlame+DoubleJump</Requirement>\n          <Requirement mode="extended">ChargeFlame+Bash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="HollowGroveMapStone">\n    <Locations>\n      <Location>\n        <X>351</X>\n        <Y>-119</Y>\n        <Item>MapStone</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HollowGroveTree">\n    <Locations>\n      <Location>\n        <X>333</X>\n        <Y>-61</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HollowGrovePlants">\n    <Locations>\n      <Location>\n        <X>365</X>\n        <Y>-119</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n      <Location>\n        <X>330</X>\n        <Y>-78</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SwampPlant">\n    <Locations>\n      <Location>\n        <X>628</X>\n        <Y>-120</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MoonGrottoStompPlant">\n    <Locations>\n      <Location>\n        <X>435</X>\n        <Y>-140</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SwampMortarPlant">\n    <Locations>\n      <Location>\n        <X>515</X>\n        <Y>-100</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="GroveWaterStomp">\n    <Locations>\n      <Location>\n        <X>354</X>\n        <Y>-178</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightGinsoOrb">\n    <Locations>\n      <Location>\n        <X>666</X>\n        <Y>-48</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LeftGinsoCell">\n    <Locations>\n      <Location>\n        <X>409</X>\n        <Y>-34</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="UpperGroveSpiderArea">\n    <Locations>\n      <Location>\n        <X>174</X>\n        <Y>-105</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n      <Location>\n        <X>261</X>\n        <Y>-117</Y>\n        <Item>HC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="UpperGroveSpiderArea"/>\n        <Target name="UpperGroveSpiderEnergy"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="UpperGroveSpiderEnergy">\n    <Locations>\n      <Location>\n        <X>272</X>\n        <Y>-97</Y>\n        <Item>EC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="GroveWater">\n    <Locations>\n      <Location>\n        <X>187</X>\n        <Y>-163</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DeathWater">\n    <Locations>\n      <Location>\n        <X>339</X>\n        <Y>-216</Y>\n        <Item>AC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DeathStomp">\n    <Locations>\n      <Location>\n        <X>356</X>\n        <Y>-207</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="UpperGrottoOrbs">\n    <Locations>\n      <Location>\n        <X>477</X>\n        <Y>-140</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>432</X>\n        <Y>-108</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>365</X>\n        <Y>-109</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n      <Location>\n        <X>581</X>\n        <Y>-67</Y>\n        <Item>HC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="UpperGrottoOrbs"/>\n        <Target name="UpperGrottoOrbsPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="UpperGrottoOrbsPlant">\n    <Locations>\n      <Location>\n        <X>540</X>\n        <Y>-220</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="UpperGrotto200">\n    <Locations>\n      <Location>\n        <X>449</X>\n        <Y>-166</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MortarCell">\n    <Locations>\n      <Location>\n        <X>502</X>\n        <Y>-108</Y>\n        <Item>AC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SwampGrottoWater">\n    <Locations>\n      <Location>\n        <X>595</X>\n        <Y>-136</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightGrottoHealth">\n    <Locations>\n      <Location>\n        <X>543</X>\n        <Y>-189</Y>\n        <Item>HC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MoonGrottoEnergyWater">\n    <Locations>\n      <Location>\n        <X>423</X>\n        <Y>-274</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MoonGrottoEnergyTop">\n    <Locations>\n      <Location>\n        <X>424</X>\n        <Y>-220</Y>\n        <Item>HC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MoonGrottoAirOrb">\n    <Locations>\n      <Location>\n        <X>552</X>\n        <Y>-141</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="MoonGrottoAirOrb"/>\n        <Target name="MoonGrottoAirOrbPlant"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+ChargeFlame+WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+ChargeFlame+ChargeJump+Glide</Requirement>\n          <Requirement mode="normal">Stomp+ChargeFlame+ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+ChargeFlame+ChargeJump+Climb</Requirement>\n          <Requirement mode="normal">Stomp+Grenade</Requirement>\n          <Requirement mode="extended">Grenade</Requirement>\n          <Requirement mode="extended">ChargeFlame+Bash</Requirement>\n          <Requirement mode="extended-damage">ChargeFlame+WallJump+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">ChargeFlame+ChargeJump+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">ChargeFlame+DoubleJump+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">ChargeFlame+Glide+HC+HC+HC+HC</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="MoonGrottoAirOrbPlant">\n    <Locations>\n      <Location>\n        <X>537</X>\n        <Y>-176</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SideFallCell">\n    <Locations>\n      <Location>\n        <X>451</X>\n        <Y>-296</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="SideFallCell"/>\n        <Target name="GumoHideout"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SideFallCell"/>\n        <Target name="GumoHideoutPartialMobile"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="SideFallCell"/>\n        <Target name="GumoHideoutRedirectAC"/>\n        <Requirements>\n          <Requirement mode="dboost-light">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="GumoHideout">\n    <Locations>\n      <Location>\n        <X>513</X>\n        <Y>-413</Y>\n        <Item>MS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>620</X>\n        <Y>-404</Y>\n        <Item>KS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>572</X>\n        <Y>-378</Y>\n        <Item>EX100</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>590</X>\n        <Y>-384</Y>\n        <Item>KS</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="DoubleJumpArea"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+WallJump</Requirement>\n          <Requirement mode="dboost-light">KS+KS+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="MobileGumoHideout"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">WallJump+ChargeJump</Requirement>\n          <Requirement mode="extreme">WallJump+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="GumoHideoutPartialMobile"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">WallJump+ChargeJump</Requirement>\n          <Requirement mode="normal">Glide+Wind</Requirement>\n          <Requirement mode="extreme">WallJump+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="GumoHideoutRedirectAC"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">WallJump+ChargeJump</Requirement>\n          <Requirement mode="normal">Glide+Wind</Requirement>\n          <Requirement mode="extreme">WallJump+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="GumoHideoutMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="LowerBlackRoot"/>\n        <Requirements>\n          <Requirement mode="glitched">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideout"/>\n        <Target name="SideFallCell"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="normal">Glide+Wind</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="GumoHideoutPartialMobile">\n    <Locations>\n      <Location>\n        <X>496</X>\n        <Y>-369</Y>\n        <Item>EX15</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>467</X>\n        <Y>-369</Y>\n        <Item>EX15</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="GumoHideoutPartialMobile"/>\n        <Target name="MobileGumoHideoutPlants"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideoutPartialMobile"/>\n        <Target name="GumoHideoutWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideoutPartialMobile"/>\n        <Target name="HideoutRedirect"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="GumoHideoutPartialMobile"/>\n        <Target name="GumoHideoutRedirectAC"/>\n        <Requirements>\n          <Requirement mode="dboost-light">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="GumoHideoutRedirectAC">\n    <Locations>\n      <Location>\n        <X>449</X>\n        <Y>-430</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="GumoHideoutMapStone">\n    <Locations>\n      <Location>\n        <X>477</X>\n        <Y>-389</Y>\n        <Item>MapStone</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DoubleJumpArea">\n    <Locations>\n      <Location>\n        <X>784</X>\n        <Y>-412</Y>\n        <Item>SKDoubleJump</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="DoubleJumpArea"/>\n        <Target name="MobileDoubleJumpArea"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="normal">Climb+DoubleJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="MobileDoubleJumpArea">\n    <Locations>\n      <Location>\n        <X>759</X>\n        <Y>-398</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MobileGumoHideout">\n    <Locations>\n      <Location>\n        <X>545</X>\n        <Y>-357</Y>\n        <Item>EC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>567</X>\n        <Y>-246</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>0</X>\n        <Y>0</Y>\n        <Item>EVGinsoKey</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>406</X>\n        <Y>-386</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>393</X>\n        <Y>-375</Y>\n        <Item>HC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>328</X>\n        <Y>-353</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="MobileGumoHideout"/>\n        <Target name="MoonGrotto"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MobileGumoHideout"/>\n        <Target name="GumoHideoutWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MobileGumoHideout"/>\n        <Target name="HideoutRedirect"/>\n        <Requirements>\n          <Requirement mode="normal">EC+EC+EC+EC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MobileGumoHideout"/>\n        <Target name="MobileGumoHideoutPlants"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="MobileGumoHideoutPlants">\n    <Locations>\n      <Location>\n        <X>447</X>\n        <Y>-368</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>439</X>\n        <Y>-344</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>492</X>\n        <Y>-400</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="GumoHideoutWater">\n    <Locations>\n      <Location>\n        <X>397</X>\n        <Y>-411</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HideoutRedirect">\n    <Locations>\n      <Location>\n        <X>515</X>\n        <Y>-441</Y>\n        <Item>EC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n      <Location>\n        <X>505</X>\n        <Y>-439</Y>\n        <Item>EX200</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grotto</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DrainlessCell">\n    <Locations>\n      <Location>\n        <X>643</X>\n        <Y>-127</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DeathGauntletRoof">\n    <Locations>\n      <Location>\n        <X>321</X>\n        <Y>-179</Y>\n        <Item>HC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="DeathGauntletRoof"/>\n        <Target name="DeathGauntlet"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="DeathGauntletRoof"/>\n        <Target name="DeathGauntletRoofPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="DeathGauntletRoofPlant">\n    <Locations>\n      <Location>\n        <X>342</X>\n        <Y>-179</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LowerGinsoTree">\n    <Locations>\n      <Location>\n        <X>523</X>\n        <Y>142</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>531</X>\n        <Y>267</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>540</X>\n        <Y>277</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>508</X>\n        <Y>304</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>529</X>\n        <Y>297</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="LowerGinsoTree"/>\n        <Target name="BashTree"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerGinsoTree"/>\n        <Target name="LowerGinsoTreePlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerGinsoTree"/>\n        <Target name="Horu"/>\n        <Requirements>\n          <Requirement mode="glitched">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="LowerGinsoTreePlant">\n    <Locations>\n      <Location>\n        <X>540</X>\n        <Y>101</Y>\n        <Item>Plant</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="BashTree">\n    <Locations>\n      <Location>\n        <X>532</X>\n        <Y>328</Y>\n        <Item>SKBash</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="BashTree"/>\n        <Target name="UpperGinsoTree"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="UpperGinsoTree">\n    <Locations>\n      <Location>\n        <X>518</X>\n        <Y>339</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>507</X>\n        <Y>476</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>535</X>\n        <Y>488</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>531</X>\n        <Y>502</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>508</X>\n        <Y>498</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="UpperGinsoTree"/>\n        <Target name="TopGinsoTree"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS+Bash+WallJump</Requirement>\n          <Requirement mode="normal">KS+KS+KS+KS+Bash+Climb</Requirement>\n          <Requirement mode="normal">KS+KS+KS+KS+Bash+ChargeJump</Requirement>\n          <Requirement mode="dboost">KS+KS+KS+KS+ChargeJump+WallJump+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">KS+KS+KS+KS+ChargeJump+Climb+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">KS+KS+KS+KS+ChargeJump+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">KS+KS+KS+KS+ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="extreme">WallJump+DoubleJump+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <!-- this can be reached with chargejump only due to a micro ledge-->\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="UpperGinsoTree"/>\n        <Target name="UpperGinsoFloors"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="extended">ChargeFlame</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="UpperGinsoFloors">\n    <Locations>\n      <Location>\n        <X>517</X>\n        <Y>384</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>530</X>\n        <Y>407</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>536</X>\n        <Y>434</Y>\n        <Item>EC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="TopGinsoTree">\n    <Locations>\n      <Location>\n        <X>456</X>\n        <Y>566</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>471</X>\n        <Y>614</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="TopGinsoTree"/>\n        <Target name="GinsoEscape"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="speed">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="TopGinsoTree"/>\n        <Target name="TopGinsoTreePlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="TopGinsoTreePlant">\n    <Locations>\n      <Location>\n        <X>610</X>\n        <Y>611</Y>\n        <Item>Plant</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="GinsoEscape">\n    <Locations>\n      <Location>\n        <X>534</X>\n        <Y>661</Y>\n        <Item>EX200</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>537</X>\n        <Y>733</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>533</X>\n        <Y>827</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>519</X>\n        <Y>867</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n      <Location>\n        <X>0</X>\n        <Y>4</Y>\n        <Item>EVWater</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Ginso</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="Swamp">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="DrainlessCell"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="extended">ChargeJump+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="SwampWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="DrainExp"/>\n        <Requirements>\n          <Requirement mode="normal">Water+Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">Water+DoubleJump</Requirement>\n          <Requirement mode="normal">Water+Glide</Requirement>\n          <Requirement mode="normal">Water+Dash</Requirement>\n          <Requirement mode="normal">Water+Bash+Grenade</Requirement>\n          <Requirement mode="dbash">Water+Bash</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC+HC+Climb+ChargeJump</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC+HC+DoubleJump</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC+HC+Glide</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC+HC+Dash</Requirement>\n          <Requirement mode="extreme">HC+HC+HC+HC+HC+HC+HC+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="SwampStomp"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="extended">Climb+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="SwampEnergy"/>\n        <Requirements>\n          <Requirement mode="normal">Wind+Glide</Requirement>\n          <Requirement mode="normal">ChargeJump+Climb+Glide</Requirement>\n          <Requirement mode="normal">ChargeJump+Climb+DoubleJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n          <!-- dbash here requires dboosting, but only 2 if done right -->\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="RightSwamp"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+WallJump</Requirement>\n          <Requirement mode="normal">KS+KS+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Swamp"/>\n        <Target name="SwampMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="SwampMapStone">\n    <Locations>\n      <Location>\n        <X>677</X>\n        <Y>-129</Y>\n        <Item>MapStone</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DrainExp">\n    <Locations>\n      <Location>\n        <X>636</X>\n        <Y>-162</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SwampWater">\n    <Locations>\n      <Location>\n        <X>761</X>\n        <Y>-173</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n      <Location>\n        <X>684</X>\n        <Y>-205</Y>\n        <Item>KS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n      <Location>\n        <X>766</X>\n        <Y>-183</Y>\n        <Item>KS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n      <Location>\n        <X>796</X>\n        <Y>-210</Y>\n        <Item>MS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SwampStomp">\n    <Locations>\n      <Location>\n        <X>770</X>\n        <Y>-148</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SwampEnergy">\n    <Locations>\n      <Location>\n        <X>722</X>\n        <Y>-95</Y>\n        <Item>EC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightSwamp">\n    <Locations>\n      <Location>\n        <X>860</X>\n        <Y>-96</Y>\n        <Item>SKStomp</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="RightSwamp"/>\n        <Target name="RightSwampStomp"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="normal">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="RightSwamp"/>\n        <Target name="RightSwampCJump"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="RightSwamp"/>\n        <Target name="RightSwampGrenade"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade+Water</Requirement>\n          <Requirement mode="dboost">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="RightSwampCJump">\n    <Locations>\n      <Location>\n        <X>914</X>\n        <Y>-71</Y>\n        <Item>EX200</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightSwampStomp">\n    <Locations>\n      <Location>\n        <X>884</X>\n        <Y>-98</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightSwampGrenade">\n    <Locations>\n      <Location>\n        <X>874</X>\n        <Y>-143</Y>\n        <Item>EX200</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Swamp</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HoruFields">\n    <Locations>\n      <Location>\n        <X>97</X>\n        <Y>-37</Y>\n        <Item>EX200</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="HoruFields"/>\n        <Target name="HoruFieldsEnergy"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n          <Requirement mode="normal">DoubleJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HoruFields"/>\n        <Target name="BelowHoruFields"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+DoubleJump+Bash</Requirement>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="dboost">WallJump+Bash+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">DoubleJump+Bash+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HoruFields"/>\n        <Target name="Horu"/>\n        <Requirements>\n          <Requirement mode="normal">HoruKey+Bash+DoubleJump+Glide+WallJump</Requirement>\n          <Requirement mode="normal">HoruKey+Bash+DoubleJump+ChargeJump+WallJump</Requirement>\n          <Requirement mode="normal">HoruKey+Bash+Glide+ChargeJump+WallJump</Requirement>\n          <Requirement mode="normal">HoruKey+Bash+DoubleJump+Glide+Climb</Requirement>\n          <Requirement mode="normal">HoruKey+Bash+DoubleJump+ChargeJump+Climb</Requirement>\n          <Requirement mode="normal">HoruKey+Bash+Glide+ChargeJump+Climb</Requirement>\n          <Requirement mode="extended">HoruKey+Bash+Grenade+WallJump</Requirement>\n          <Requirement mode="extended">HoruKey+Bash+Grenade+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HoruFields"/>\n        <Target name="DoorWarp"/>\n        <Requirements>\n          <Requirement mode="extended">HoruKey</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="HoruFieldsEnergy">\n    <Locations>\n      <Location>\n        <X>175</X>\n        <Y>1</Y>\n        <Item>EC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="HoruFieldsEnergy"/>\n        <Target name="HoruFieldsEnergyPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="HoruFieldsEnergyPlant">\n    <Locations>\n      <Location>\n        <X>124</X>\n        <Y>21</Y>\n        <Item>Plant</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="BelowHoruFields">\n    <Locations>\n      <Location>\n        <X>176</X>\n        <Y>-34</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HoruFieldsStomp">\n    <Locations>\n      <Location>\n        <X>160</X>\n        <Y>-78</Y>\n        <Item>HC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Grove</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="Horu">\n    <Locations>\n      <Location>\n        <X>193</X>\n        <Y>384</Y>\n        <Item>EX100</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>148</X>\n        <Y>363</Y>\n        <Item>MS</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>249</X>\n        <Y>403</Y>\n        <Item>EC</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="Horu"/>\n        <Target name="HoruStomp"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Horu"/>\n        <Target name="HoruMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Horu"/>\n        <Target name="LowerGinsoTree"/>\n        <Requirements>\n          <Requirement mode="glitched">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="HoruMapStone">\n    <Locations>\n      <Location>\n        <X>56</X>\n        <Y>343</Y>\n        <Item>MapStone</Item>\n        <Difficulty>6</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="HoruStomp">\n    <Locations>\n      <Location>\n        <X>191</X>\n        <Y>165</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>253</X>\n        <Y>194</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>163</X>\n        <Y>136</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>-191</X>\n        <Y>194</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>-29</X>\n        <Y>148</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>13</X>\n        <Y>164</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>129</X>\n        <Y>165</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n      <Location>\n        <X>98</X>\n        <Y>130</Y>\n        <Item>EX200</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="HoruStomp"/>\n        <Target name="HoruStompPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HoruStomp"/>\n        <Target name="End"/>\n        <Requirements>\n          <Requirement mode="normal">Climb+Dash+Stomp+Glide+Bash+ChargeJump+Grenade+GinsoKey+ForlornKey+HoruKey</Requirement>\n          <Requirement mode="extended">Dash+Stomp+Glide+Bash+ChargeJump+Grenade+GinsoKey+ForlornKey+HoruKey</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="HoruStomp"/>\n        <Target name="DoorWarp"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="HoruStompPlant">\n    <Locations>\n      <Location>\n        <X>318</X>\n        <Y>245</Y>\n        <Item>Plant</Item>\n        <Difficulty>7</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="DoorWarp">\n    <Locations>\n      <Location>\n        <X>106</X>\n        <Y>112</Y>\n        <Item>EX200</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>  \n  <Area name="End">\n    <Locations>\n      <Location>\n        <X>0</X>\n        <Y>20</Y>\n        <Item>EVWarmth</Item>\n        <Difficulty>0</Difficulty>\n        <Zone>Horu</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyEntry">\n    <Locations>\n      <Location>\n        <X>-205</X>\n        <Y>-113</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="ValleyEntry"/>\n        <Target name="ValleyEntryTree"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Bash+Climb</Requirement>\n          <Requirement mode="normal">DoubleJump+Climb</Requirement>\n          <Requirement mode="normal">ChargeJump+Climb</Requirement>\n          <Requirement mode="lure">Bash</Requirement>\n          <Requirement mode="dboost">ChargeJump+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyEntry"/>\n        <Target name="ValleyRight"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp+Bash+WallJump</Requirement>\n          <Requirement mode="normal">Stomp+Bash+DoubleJump</Requirement>\n          <Requirement mode="normal">Stomp+Bash+Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">Stomp+Bash+Grenade</Requirement>\n          <Requirement mode="extended">Bash+DoubleJump</Requirement>\n          <Requirement mode="extended">Bash+Climb+ChargeJump</Requirement>\n          <Requirement mode="extended">Bash+WallJump</Requirement>\n          <Requirement mode="extended">Bash+Grenade</Requirement>\n          <Requirement mode="extended-damage">Stomp+ChargeJump+DoubleJump+WallJump+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n          <Requirement mode="extreme">Stomp+WallJump+DoubleJump+ChargeJump</Requirement>\n          <Requirement mode="extreme">Stomp+WallJump+DoubleJump+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyEntry"/>\n        <Target name="ValleyEntryTreePlant"/>\n        <Requirements>\n          <Requirement mode="extended">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyEntry"/>\n        <Target name="ValleyWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water+Stomp+WallJump+DoubleJump</Requirement>\n          <Requirement mode="normal">Water+Stomp+WallJump+Bash</Requirement>\n          <Requirement mode="normal">Water+Stomp+WallJump+ChargeJump</Requirement>\n          <Requirement mode="normal">Water+Stomp+Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">Water+Stomp+Climb+DoubleJump</Requirement>\n          <Requirement mode="dboost">Stomp+WallJump+DoubleJump</Requirement>\n          <Requirement mode="dboost">Stomp+WallJump+Bash</Requirement>\n          <Requirement mode="dboost">Stomp+WallJump+ChargeJump</Requirement>\n          <Requirement mode="dboost">Stomp+Climb+ChargeJump</Requirement>\n          <Requirement mode="dboost">Stomp+Climb+DoubleJump</Requirement>\n          <Requirement mode="extended">Bash+Water</Requirement>\n          <Requirement mode="extended-damage">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyEntry"/>\n        <Target name="SpiritTreeRefined"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ValleyEntryTree">\n    <Locations>\n      <Location>\n        <X>-221</X>\n        <Y>-84</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="ValleyEntryTree"/>\n        <Target name="ValleyGrenadeWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water+Grenade</Requirement>\n          <Requirement mode="dboost-hard">Grenade+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost-hard">Grenade+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC+Bash</Requirement>\n          <Requirement mode="extreme">Grenade+HC+HC+HC+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyEntryTree"/>\n        <Target name="ValleyEntryTreePlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+Climb+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+Climb+Grenade</Requirement>\n          <Requirement mode="normal">ChargeJump+DoubleJump+ChargeFlame</Requirement>\n          <Requirement mode="normal">ChargeJump+DoubleJump+Grenade</Requirement>\n          <Requirement mode="normal">Bash+ChargeFlame</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n          <Requirement mode="normal">Glide+ChargeFlame</Requirement>\n          <Requirement mode="normal">Glide+Grenade</Requirement>\n          <Requirement mode="cdash-farming">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ValleyEntryTreePlant">\n    <Locations>\n      <Location>\n        <X>-179</X>\n        <Y>-88</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyGrenadeWater">\n    <Locations>\n      <Location>\n        <X>-320</X>\n        <Y>-162</Y>\n        <Item>EC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyRight">\n    <Locations>\n      <Location>\n        <X>-355</X>\n        <Y>65</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n      <Location>\n        <X>-418</X>\n        <Y>67</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="ValleyRight"/>\n        <Target name="ValleyMain"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+Stomp</Requirement>\n          <Requirement mode="extended">Dash+Bash</Requirement>\n          <Requirement mode="extended">Dash+Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyRight"/>\n        <Target name="BirdStompCell"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+Climb</Requirement>\n          <Requirement mode="speed">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="BirdStompCell">\n    <Locations>\n      <Location>\n        <X>-292</X>\n        <Y>20</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyMain">\n    <Locations>\n      <Location>\n        <X>-460</X>\n        <Y>-20</Y>\n        <Item>SKGlide</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n      <Location>\n        <X>-546</X>\n        <Y>54</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n     <Location>\n        <X>-678</X>\n        <Y>-29</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-822</X>\n        <Y>-9</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="PreSorrowOrb"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="Sorrow"/>\n        <Requirements>\n          <Requirement mode="normal">Wind+Glide</Requirement>\n          <Requirement mode="speed">Glide+DoubleJump+Bash+Dash</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n          <Requirement mode="extended-damage">ChargeJump+DoubleJump+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">ChargeJump+Glide+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extended-damage">ChargeJump+Dash+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">ChargeJump+DoubleJump+HC+HC+HC+HC+HC+HC+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="Misty"/>\n        <Requirements>\n          <Requirement mode="normal">Glide+Bash</Requirement>\n          <Requirement mode="dboost">Bash+DoubleJump+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">DoubleJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="Forlorn"/>\n        <Requirements>\n          <Requirement mode="normal">ForlornKey</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="RightForlorn"/>\n        <Requirements>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="OutsideForlornGrenade"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="ValleyMainFACS"/>\n        <Requirements>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="extended">Bash+Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="ValleyMainPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="ValleyMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ValleyMain"/>\n        <Target name="LowerValley"/>\n        <Requirements>\n          <Requirement mode="normal">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ValleyMapStone">\n    <Locations>\n      <Location>\n        <X>-408</X>\n        <Y>-170</Y>\n        <Item>MapStone</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyMainPlant">\n    <Locations>\n      <Location>\n        <X>-468</X>\n        <Y>-67</Y>\n        <Item>Plant</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="PreSorrowOrb">\n    <Locations>\n      <Location>\n        <X>-572</X>\n        <Y>157</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyWater">\n    <Locations>\n      <Location>\n        <X>-359</X>\n        <Y>-87</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ValleyMainFACS">\n    <Locations>\n      <Location>\n        <X>-415</X>\n        <Y>-80</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="OutsideForlornGrenade">\n    <Locations>\n      <Location>\n        <X>-460</X>\n        <Y>-187</Y>\n        <Item>AC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LowerValley">\n    <Locations>\n      <Location>\n        <X>-350</X>\n        <Y>-98</Y>\n        <Item>AC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n      <Location>\n        <X>-561</X>\n        <Y>-89</Y>\n        <Item>MS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n      <Location>\n        <X>-538</X>\n        <Y>-104</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="LowerValley"/>\n        <Target name="ValleyMainFACS"/>\n        <Requirements>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="extended">Bash+Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerValley"/>\n        <Target name="LowerValleyPlantApproach"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+DoubleJump</Requirement>\n          <Requirement mode="normal">Bash+Glide</Requirement>\n          <Requirement mode="normal">ChargeJump+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeJump+Glide</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LowerValley"/>\n        <Target name="ValleyEntry"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="LowerValleyPlantApproach">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="LowerValleyPlantApproach"/>\n        <Target name="ValleyMainPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>    \n    </Connections>\n  </Area>\n  <Area name="OutsideForlorn">\n    <Locations>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="OutsideForlorn"/>\n        <Target name="OutsideForlornTree"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="OutsideForlorn"/>\n        <Target name="OutsideForlornWater"/>\n        <Requirements>\n          <Requirement mode="normal">Water</Requirement>\n          <Requirement mode="dboost">HC+HC+HC+HC</Requirement>\n          <Requirement mode="dboost">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="OutsideForlorn"/>\n        <Target name="OutsideForlornCliff"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump+ChargeJump</Requirement>\n          <Requirement mode="normal">Climb+ChargeJump</Requirement>\n          <Requirement mode="normal">Bash+Glide</Requirement>\n          <Requirement mode="normal">Bash+DoubleJump</Requirement>\n          <Requirement mode="normal">Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="OutsideForlornTree">\n    <Locations>\n      <Location>\n        <X>-460</X>\n        <Y>-255</Y>\n        <Item>EX100</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="OutsideForlornWater">\n    <Locations>\n      <Location>\n        <X>-514</X>\n        <Y>-277</Y>\n        <Item>EX100</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="OutsideForlornCliff">\n    <Locations>\n      <Location>\n        <X>-538</X>\n        <Y>-234</Y>\n        <Item>EX200</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="OutsideForlornCliff"/>\n        <Target name="OutsideForlornGrenade"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+Stomp+Grenade</Requirement>\n          <Requirement mode="extreme">Bash+Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="OutsideForlornCliff"/>\n        <Target name="ValleyMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS+Bash+Stomp</Requirement>\n          <Requirement mode="extreme">MS+Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="OutsideForlornCliff"/>\n        <Target name="OutsideForlornMS"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+Stomp</Requirement>\n          <Requirement mode="extreme">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="OutsideForlornCliff"/>\n        <Target name="LowerValley"/>\n        <Requirements>\n          <Requirement mode="normal">Bash+ChargeJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="OutsideForlornMS">\n    <Locations>\n      <Location>\n        <X>-443</X>\n        <Y>-152</Y>\n        <Item>MS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Valley</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="Forlorn">\n    <Locations>\n      <Location>\n        <X>-703</X>\n        <Y>-390</Y>\n        <Item>EX200</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n      <Location>\n        <X>-841</X>\n        <Y>-350</Y>\n        <Item>EX100</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n      <Location>\n        <X>-858</X>\n        <Y>-353</Y>\n        <Item>KS</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n      <Location>\n        <X>-892</X>\n        <Y>-328</Y>\n        <Item>KS</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n      <Location>\n        <X>-888</X>\n        <Y>-251</Y>\n        <Item>KS</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n      <Location>\n        <X>-869</X>\n        <Y>-255</Y>\n        <Item>KS</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="Forlorn"/>\n        <Target name="RightForlorn"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS+Glide+Stomp+Bash+WallJump</Requirement>\n          <Requirement mode="normal">KS+KS+KS+KS+Glide+Stomp+Bash+Climb</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Forlorn"/>\n        <Target name="ForlornPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Forlorn"/>\n        <Target name="ForlornMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Forlorn"/>\n        <Target name="OutsideForlorn"/>\n        <Requirements>\n          <Requirement mode="normal">WallJump</Requirement>\n          <Requirement mode="normal">Climb</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ForlornMapStone">\n    <Locations>\n      <Location>\n        <X>-843</X>\n        <Y>-308</Y>\n        <Item>MapStone</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="ForlornPlant">\n    <Locations>\n      <Location>\n        <X>-815</X>\n        <Y>-266</Y>\n        <Item>Plant</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="RightForlorn">\n    <Locations>\n      <Location>\n        <X>-625</X>\n        <Y>-315</Y>\n        <Item>HC</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n      <Location>\n        <X>0</X>\n        <Y>12</Y>\n        <Item>EVWind</Item>\n        <Difficulty>6</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="RightForlorn"/>\n        <Target name="RightForlornPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="RightForlornPlant">\n    <Locations>\n      <Location>\n        <X>-607</X>\n        <Y>-314</Y>\n        <Item>Plant</Item>\n        <Difficulty>6</Difficulty>\n        <Zone>Forlorn</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="Sorrow">\n    <Locations>\n      <Location>\n        <X>-510</X>\n        <Y>204</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-485</X>\n        <Y>323</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-503</X>\n        <Y>274</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-514</X>\n        <Y>303</Y>\n        <Item>KS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-596</X>\n        <Y>229</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="LeftSorrow"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS+Glide</Requirement>\n          <Requirement mode="extreme">KS+KS+KS+KS+Bash</Requirement>\n          <Requirement mode="extreme">KS+KS+KS+KS+ChargeJump+Climb+DoubleJump+HC+HC+HC+HC+HC+HC+HC+HC+HC+HC</Requirement>\n          <Requirement mode="extreme">KS+KS+KS+KS+ChargeJump+Dash+WallJump+DoubleJump+HC</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="SorrowHealth"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="SorrowMapFragment"/>\n        <Requirements>\n          <Requirement mode="normal">Bash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="SorrowMapStone"/>\n        <Requirements>\n          <Requirement mode="normal">MS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="Horu"/>\n        <Requirements>\n          <Requirement mode="glitched">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="ValleyMain"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sorrow"/>\n        <Target name="PreSorrowOrb"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n          <Requirement mode="dbash">Bash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="SorrowMapStone">\n    <Locations>\n      <Location>\n        <X>-451</X>\n        <Y>284</Y>\n        <Item>MapStone</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SorrowMapFragment">\n    <Locations>\n      <Location>\n        <X>-435</X>\n        <Y>322</Y>\n        <Item>MS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="SorrowHealth">\n    <Locations>\n      <Location>\n        <X>-609</X>\n        <Y>299</Y>\n        <Item>HC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LeftSorrow">\n    <Locations>\n      <Location>\n        <X>-671</X>\n        <Y>289</Y>\n        <Item>AC</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-608</X>\n        <Y>329</Y>\n        <Item>KS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-612</X>\n        <Y>347</Y>\n        <Item>KS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-604</X>\n        <Y>361</Y>\n        <Item>KS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-613</X>\n        <Y>371</Y>\n        <Item>KS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-627</X>\n        <Y>393</Y>\n        <Item>EC</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="LeftSorrow"/>\n        <Target name="LeftSorrowGrenade"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LeftSorrow"/>\n        <Target name="UpperSorrow"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="LeftSorrow"/>\n        <Target name="LeftSorrowPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="LeftSorrowPlant">\n    <Locations>\n      <Location>\n        <X>-630</X>\n        <Y>249</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="LeftSorrowGrenade">\n    <Locations>\n      <Location>\n        <X>-677</X>\n        <Y>269</Y>\n        <Item>EX200</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="UpperSorrow">\n    <Locations>\n      <Location>\n        <X>-456</X>\n        <Y>419</Y>\n        <Item>KS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-414</X>\n        <Y>429</Y>\n        <Item>KS</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-514</X>\n        <Y>427</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-545</X>\n        <Y>409</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n      <Location>\n        <X>-592</X>\n        <Y>445</Y>\n        <Item>KS</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="UpperSorrow"/>\n        <Target name="ChargeJump"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="UpperSorrow"/>\n        <Target name="Sorrow"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="extended">Climb+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="ChargeJump">\n    <Locations>\n      <Location>\n        <X>-696</X>\n        <Y>408</Y>\n        <Item>SKChargeJump</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="ChargeJump"/>\n        <Target name="Sunstone"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump+Climb</Requirement>\n          <Requirement mode="extended">Bash+Glide</Requirement>\n          <Requirement mode="extended">Bash+Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="ChargeJump"/>\n        <Target name="AboveChargeJump"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="AboveChargeJump">\n    <Locations>\n      <Location>\n        <X>-646</X>\n        <Y>473</Y>\n        <Item>AC</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="Sunstone">\n    <Locations>\n      <Location>\n        <X>0</X>\n        <Y>16</Y>\n        <Item>EVHoruKey</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="Sunstone"/>\n        <Target name="SunstonePlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Sunstone"/>\n        <Target name="UpperSorrow"/>\n        <Requirements>\n          <Requirement mode="normal">Stomp</Requirement>\n          <Requirement mode="extended">Climb+ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="SunstonePlant">\n    <Locations>\n      <Location>\n        <X>-478</X>\n        <Y>586</Y>\n        <Item>Plant</Item>\n        <Difficulty>4</Difficulty>\n        <Zone>Sorrow</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="Misty">\n    <Locations>\n      <Location>\n        <X>-979</X>\n        <Y>23</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-1075</X>\n        <Y>-2</Y>\n        <Item>AC</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-1082</X>\n        <Y>8</Y>\n        <Item>EX100</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-1009</X>\n        <Y>-35</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-1076</X>\n        <Y>32</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-1188</X>\n        <Y>-100</Y>\n        <Item>SKClimb</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="Misty"/>\n        <Target name="MistyPostClimb"/>\n        <Requirements>\n          <Requirement mode="normal">Climb+DoubleJump</Requirement>\n          <Requirement mode="normal">ChargeJump</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Misty"/>\n        <Target name="MistyPlant"/>\n        <Requirements>\n          <Requirement mode="normal">ChargeFlame</Requirement>\n          <Requirement mode="normal">Grenade</Requirement>\n          <Requirement mode="cdash">Dash</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Misty"/>\n        <Target name="Forlorn"/>\n        <Requirements>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="Misty"/>\n        <Target name="RightForlorn"/>\n        <Requirements>\n          <Requirement mode="glitched">Free</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="MistyPlant">\n    <Locations>\n      <Location>\n        <X>-1102</X>\n        <Y>-67</Y>\n        <Item>Plant</Item>\n        <Difficulty>2</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MistyPostClimb">\n    <Locations>\n      <Location>\n        <X>-837</X>\n        <Y>-123</Y>\n        <Item>EX100</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-796</X>\n        <Y>-144</Y>\n        <Item>EX200</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-912</X>\n        <Y>-36</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n      <Location>\n        <X>-768</X>\n        <Y>-144</Y>\n        <Item>KS</Item>\n        <Difficulty>1</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n      <Connection>\n        <Home name="MistyPostClimb"/>\n        <Target name="MistyEndGrenade"/>\n        <Requirements>\n          <Requirement mode="normal">Grenade</Requirement>\n        </Requirements>\n      </Connection>\n      <Connection>\n        <Home name="MistyPostClimb"/>\n        <Target name="MistyEnd"/>\n        <Requirements>\n          <Requirement mode="normal">KS+KS+KS+KS</Requirement>\n        </Requirements>\n      </Connection>\n    </Connections>\n  </Area>\n  <Area name="MistyEnd">\n    <Locations>\n      <Location>\n        <X>0</X>\n        <Y>8</Y>\n        <Item>EVForlornKey</Item>\n        <Difficulty>3</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n  <Area name="MistyEndGrenade">\n    <Locations>\n      <Location>\n        <X>-671</X>\n        <Y>-39</Y>\n        <Item>EX200</Item>\n        <Difficulty>5</Difficulty>\n        <Zone>Misty</Zone>\n      </Location>\n    </Locations>\n    <Connections>\n    </Connections>\n  </Area>\n</Areas>\n'.split('\n')

    i = 0
    while i < len(lines):

        match = re.match(".*<Area name=\"(.+)\".*", lines[i])
        if match:
            area = Area(match.group(1))
            areaList.append(match.group(1))
            i += 1
            continue

        match = re.match(".*<Location>.*", lines[i])
        if match:
            loc = Location(int(selectText('<X>', '</X>', lines[i+1])), int(selectText('<Y>', '</Y>', lines[i+2])), area.name, selectText('<Item>', '</Item>', lines[i+3]), int(selectText('<Difficulty>', '</Difficulty>', lines[i+4])), selectText('<Zone>', '</Zone>', lines[i+5]))
            i += 6
            if not includePlants:
                if re.match(".*Plant.*", area.name):
                    plants.append(loc)
                    continue
            area.add_location(loc)
            continue

        match = re.match(".*<Connection>.*", lines[i])
        if match:
            connection = Connection(selectText("\"", "\"", lines[i+1]), selectText("\"", "\"", lines[i+2]))
            i += 4
            if not includePlants:
                if re.match(".*Plant.*", connection.target):
                    currentConnection = None
                    continue
            currentConnection = connection
            continue

        match = re.match(".*<Requirement mode=.*", lines[i])
        if match and currentConnection:
            mode = selectText("\"", "\"", lines[i])
            if mode in modes:
                currentConnection.add_requirements(selectText(">", "</Requirement>", lines[i]).split('+'), difficultyMap[mode])
            i += 1
            continue

        match = re.match(".*</Requirements>.*", lines[i])
        if match and currentConnection:
            area.add_connection(currentConnection)
            i += 1
            continue

        match = re.match(".*</Area>.*", lines[i])
        if match:
            areas[area.name] = area
            i += 1
            continue

        i += 1


    # flags line
    outputStr += (flags + "|" + str(seed) + "\r\n")

    outputStr += ("-280256|EC|1|Glades\r\n")  # first energy cell
    outputStr += ("-1680104|EX|100|Grove\r\n")  # glitchy 100 orb at spirit tree
    outputStr += ("-12320248|EX|100|Forlorn\r\n")  # forlorn escape plant
    # the 2nd keystone in misty can get blocked by alt+R, so make it unimportant
    outputStr += ("-10440008|EX|100|Misty\r\n")

    if not includePlants:
        for location in plants:
            outputStr += (str(location.get_key()) + "|NO|0\r\n")

    locationsToAssign = []
    connectionQueue = []
    global reservedLocations
    reservedLocations = []

    skillCount = 10
    mapstonesAssigned = 0
    expSlots = itemPool["EX*"]
    while itemCount > 0:
        assignQueue = []
        doorQueue = {}
        mapQueue = {}
        spoilerPath = ""

        global spoilerGroup
        spoilerGroup = {"MS": [], "KS": [], "EC": [], "HC": []}

        # open all paths that we can already access
        opening = True
        while opening:
            (opening, keys, mapstones) = open_free_connections()
            keystoneCount += keys
            mapstoneCount += mapstones
            for connection in connectionQueue:
                areas[connection[0]].remove_connection(connection[1])
            connectionQueue = []

        locationsToAssign = get_all_accessible_locations()
        # if there aren't any doors to open, it's time to get a new skill
        # consider -- work on stronger anti-key-lock logic so that we don't
        # have to give keys out right away (this opens up the potential of
        # using keys in the wrong place, will need to be careful)
        if not doorQueue and not mapQueue:
            spoilerPath = prepare_path(len(locationsToAssign))
            if not assignQueue:
                # we've painted ourselves into a corner, try again
                if not reservedLocations:
                    return placeItems(seed, expPool, hardMode, includePlants, shardsMode, limitkeysMode, cluesMode, noTeleporters, modes, flags, starvedMode, preferPathDifficulty, setNonProgressiveMapstones)
                locationsToAssign.append(reservedLocations.pop(0))
                locationsToAssign.append(reservedLocations.pop(0))
                spoilerPath = prepare_path(len(locationsToAssign))
        # pick what we're going to put in our accessible space
        itemsToAssign = []
        if len(locationsToAssign) < len(assignQueue) + keystoneCount - inventory["KS"] + mapstoneCount - inventory["MS"]:
            # we've painted ourselves into a corner, try again
            if not reservedLocations:
                return placeItems(seed, expPool, hardMode, includePlants, shardsMode, limitkeysMode, cluesMode, noTeleporters, modes, flags, starvedMode, preferPathDifficulty, setNonProgressiveMapstones)
            locationsToAssign.append(reservedLocations.pop(0))
            locationsToAssign.append(reservedLocations.pop(0))
        for i in range(0, len(locationsToAssign)):
            if assignQueue:
                itemsToAssign.append(assign(assignQueue.pop(0)))
            elif inventory["KS"] < keystoneCount:
                itemsToAssign.append(assign("KS"))
            elif inventory["MS"] < mapstoneCount:
                itemsToAssign.append(assign("MS"))
            else:
                itemsToAssign.append(assign_random())
            itemCount -= 1

        # force assign things if using --prefer-path-difficulty
        if pathDifficulty:
            for item in list(itemsToAssign):
                if item in skillsOutput or item in eventsOutput:
                    preferred_difficulty_assign(item, locationsToAssign)
                    itemsToAssign.remove(item)

        # shuffle the items around and put them somewhere
        random.shuffle(itemsToAssign)
        for i in range(0, len(locationsToAssign)):
            assign_to_location(itemsToAssign[i], locationsToAssign[i])

        currentGroupSpoiler = ""

        if spoilerPath:
            currentGroupSpoiler += ("    Forced pickups: " + str(spoilerPath) + "\r\n")

        for skill in skillsOutput:
            if skill in spoilerGroup:
                for instance in spoilerGroup[skill]:
                    currentGroupSpoiler += "    " + instance
                if skill in seedDifficultyMap:
                    seedDifficulty += groupDepth * seedDifficultyMap[skill]

        for event in eventsOutput:
            if event in spoilerGroup:
                for instance in spoilerGroup[event]:
                    currentGroupSpoiler += "    " + instance

        for key in spoilerGroup:
            if key[:2] == "TP":
                for instance in spoilerGroup[key]:
                    currentGroupSpoiler += "    " + instance

        for instance in spoilerGroup["MS"]:
            currentGroupSpoiler += "    " + instance

        for instance in spoilerGroup["KS"]:
            currentGroupSpoiler += "    " + instance

        for instance in spoilerGroup["HC"]:
            currentGroupSpoiler += "    " + instance

        for instance in spoilerGroup["EC"]:
            currentGroupSpoiler += "    " + instance

        if currentGroupSpoiler:
            groupDepth += 1
            currentAreas.sort()

            spoilerStr += str(groupDepth) + ": " + str(currentAreas) + " {\r\n"

            spoilerStr += currentGroupSpoiler

            spoilerStr += "}\r\n"

        currentAreas = []

        # open all reachable doors (for the next iteration)
        for area in doorQueue.keys():
            if doorQueue[area].target not in areasReached:
                currentAreas.append(doorQueue[area].target)
                difficulty = doorQueue[area].cost()[2]
                seedDifficulty += difficulty * difficulty
            areasReached[doorQueue[area].target] = True
            areas[area].remove_connection(doorQueue[area])

        for area in mapQueue.keys():
            if mapQueue[area].target not in areasReached:
                currentAreas.append(mapQueue[area].target)
                difficulty = mapQueue[area].cost()[2]
                seedDifficulty += difficulty * difficulty
            areasReached[mapQueue[area].target] = True
            areas[area].remove_connection(mapQueue[area])

        locationsToAssign = []

    spoilerStr = flags + "|" + str(seed) + "\r\n" + "Difficulty Rating: " + str(seedDifficulty) + "\r\n" + spoilerStr
    random.shuffle(eventList)
    for event in eventList:
        outputStr += event

    return (outputStr, spoilerStr)


import pyjd # this is dummy in pyjs.
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.DisclosurePanel import DisclosurePanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Button import Button
from pyjamas.ui.RadioButton import RadioButton
from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.HTML import HTML
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.TextBox import TextBox
from pyjamas import DOM

class LogicListener():

    def __init__(self, element):
        element.addChangeListener(self)

    def onChange(self, sender):
        index = sender.getSelectedIndex()

        pathNormal.setChecked(True)

        pathSpeed.setChecked(False)
        pathDBoostLight.setChecked(False)
        pathDBoost.setChecked(False)
        pathDBoostHard.setChecked(False)
        pathLure.setChecked(False)
        pathLureHard.setChecked(False)
        pathDBash.setChecked(False)
        pathCDash.setChecked(False)
        pathCDashFarming.setChecked(False)
        pathExtended.setChecked(False)
        pathExtendedDamage.setChecked(False)
        pathExtreme.setChecked(False)
        pathTimedLevel.setChecked(False)
        pathGlitched.setChecked(False)

        diffSelection.setSelectedIndex(1)
        hardBox.setChecked(False)
        starvedBox.setChecked(False)
        ohkoBox.setChecked(False)
        zeroBox.setChecked(False)
        noPlantsBox.setChecked(False)

        # casual
        if index == 0:
            pathDBoostLight.setChecked(True)
        # standard
        elif index == 1:
            pathSpeed.setChecked(True)
            pathDBoostLight.setChecked(True)
            pathLure.setChecked(True)
        # expert
        elif index == 2:
            pathSpeed.setChecked(True)
            pathDBoostLight.setChecked(True)
            pathDBoost.setChecked(True)
            pathLure.setChecked(True)
            pathCDash.setChecked(True)
            pathExtended.setChecked(True)
            pathExtendedDamage.setChecked(True)
        # master
        elif index == 3:
            pathSpeed.setChecked(True)
            pathDBoostLight.setChecked(True)
            pathDBoost.setChecked(True)
            pathDBoostHard.setChecked(True)
            pathLure.setChecked(True)
            pathLureHard.setChecked(True)
            pathDBash.setChecked(True)
            pathCDash.setChecked(True)
            pathExtended.setChecked(True)
            pathExtendedDamage.setChecked(True)
            pathExtreme.setChecked(True)
            starvedBox.setChecked(True)
            diffSelection.setSelectedIndex(2)
        # hard
        elif index == 4:
            pathSpeed.setChecked(True)
            pathDBoostLight.setChecked(True)
            pathLure.setChecked(True)
            pathDBash.setChecked(True)
            pathCDash.setChecked(True)
            pathExtended.setChecked(True)
            hardBox.setChecked(True)
        # ohko
        elif index == 5:
            pathSpeed.setChecked(True)
            pathLure.setChecked(True)
            pathDBash.setChecked(True)
            pathCDash.setChecked(True)
            pathExtended.setChecked(True)
            hardBox.setChecked(True)
            ohkoBox.setChecked(True)
        # 0xp
        elif index == 6:
            pathSpeed.setChecked(True)
            pathDBoostLight.setChecked(True)
            pathLure.setChecked(True)
            hardBox.setChecked(True)
            zeroBox.setChecked(True)
        # glitched
        elif index == 7:
            pathSpeed.setChecked(True)
            pathDBoostLight.setChecked(True)
            pathDBoost.setChecked(True)
            pathDBoostHard.setChecked(True)
            pathLure.setChecked(True)
            pathLureHard.setChecked(True)
            pathDBash.setChecked(True)
            pathCDash.setChecked(True)
            pathCDashFarming.setChecked(True)
            pathExtended.setChecked(True)
            pathExtendedDamage.setChecked(True)
            pathExtreme.setChecked(True)
            pathTimedLevel.setChecked(True)
            pathGlitched.setChecked(True)
            diffSelection.setSelectedIndex(2)

class CustomPathListener:

    def __init__(self):
        pass

    def onClick(self, sender=None):
        logicSelection.setSelectedIndex(8)

def seed_hash(seed):
    value = 0
    for index in range(len(seed)):
        value = (value << 5) - value + ord(seed[index])
    return 0xFFFFFFFF & value

def generate():

    genButton.setText("Generating...")

    # Get arguments
    seed = seedSelection.getText()
    if seed == "":
        seed = str(0x7FFFFFFF & (time.time() * 1000))
    hard = hardBox.isChecked()
    exp_pool = 10000
    if hard:
        exp_pool = 5000
    includePlants = not noPlantsBox.isChecked()
    shards = modeSelection.getSelectedIndex() == 1
    limitkeys = modeSelection.getSelectedIndex() == 2
    clues = modeSelection.getSelectedIndex() == 3
    no_teleporters = noTeleBox.isChecked()
    mode = logicSelection.getItemText(logicSelection.getSelectedIndex())
    modes = []
    if pathNormal.isChecked():
        modes.append("normal")
    if pathSpeed.isChecked():
        modes.append("speed")
    if pathDBoostLight.isChecked():
        modes.append("dboost-light")
    if pathDBoost.isChecked():
        modes.append("dboost")
    if pathDBoostHard.isChecked():
        modes.append("dboost-hard")
    if pathLure.isChecked():
        modes.append("lure")
    if pathLureHard.isChecked():
        modes.append("lure-hard")
    if pathDBash.isChecked():
        modes.append("dbash")
    if pathCDash.isChecked():
        modes.append("cdash")
    if pathCDashFarming.isChecked():
        modes.append("cdash-farming")
    if pathExtended.isChecked():
        modes.append("extended")
    if pathExtendedDamage.isChecked():
        modes.append("extended-damage")
    if pathExtreme.isChecked():
        modes.append("extreme")
    if pathTimedLevel.isChecked():
        modes.append("timed-level")
    if pathGlitched.isChecked():
        modes.append("glitched")
    starved = starvedBox.isChecked()
    prefer_path_difficulty = diffSelection.getItemText(diffSelection.getSelectedIndex()).lower()
    if prefer_path_difficulty == "normal":
        prefer_path_difficulty = None
    non_progressive_mapstones = nonProgMapBox.isChecked()

    ohko = ohkoBox.isChecked()
    zeroxp = zeroBox.isChecked()
    nobonus = noBonusBox.isChecked()
    force_trees = forceBox.isChecked()

    flags = ""
    flags += mode + ","
    if limitkeys:
        flags += "limitkeys,"
    if shards:
        flags += "shards,"
    if clues:
        flags += "clues,"
    if starved:
        flags += "starved,"
    if prefer_path_difficulty:
        flags += "prefer_path_difficulty=" + prefer_path_difficulty + ","
    if hard:
        flags += "hard,"
    if ohko:
        flags += "OHKO,"
    if zeroxp:
        flags += "0XP,"
    if nobonus:
        flags += "NoBonus,"
    if not includePlants:
        flags += "NoPlants,"
    if force_trees:
        flags += "ForceTrees,"
    if non_progressive_mapstones:
        flags += "NonProgressMapStones,"
    if no_teleporters:
        flags += "NoTeleporters,"

    flags = flags[:-1]

    random.seed(seed)

    placement = placeItems(seed, exp_pool, hard, includePlants, shards, limitkeys, clues, no_teleporters, modes, flags, starved, prefer_path_difficulty, non_progressive_mapstones)

    genButton.setText("Generate")

    element = DOM.createElement('a')
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(placement[1]));
    element.setAttribute('download', 'spoiler.txt');

    element.style.display = 'none';

    dl = DOM.getElementById("dl")
    DOM.appendChild(dl, element);

    element.click();
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(placement[0]));
    element.setAttribute('download', 'randomizer.dat');
    element.click();

    DOM.removeChild(dl, element);

def main():

    pyjd.setup("public/web_seed_generator.html")

    global random
    global itemList

    itemList = ["EX1", "EX*", "KS", "MS", "AC", "EC", "HC", "WallJump", "ChargeFlame", "Dash", "Stomp", "DoubleJump", "Glide", "Bash", "Climb", "Grenade", "ChargeJump", "GinsoKey", "ForlornKey", "HoruKey", "Water", "Wind", "Warmth", "RB0", "RB1", "RB6", "RB8", "RB9", "RB10", "RB11", "RB12", "RB13", "RB15", "WaterVeinShard", "GumonSealShard", "SunstoneShard", "TPForlorn", "TPGrotto", "TPSorrow", "TPGrove", "TPSwamp", "TPValley"]

    random = Random()

    #set up the page
    panel = VerticalPanel(HorizontalAlignment=HasAlignment.ALIGN_CENTER, StyleName="main")
    row0 = HorizontalPanel(HorizontalAlignment=HasAlignment.ALIGN_LEFT)
    row1 = HorizontalPanel(HorizontalAlignment=HasAlignment.ALIGN_LEFT, StyleName="row")
    row2 = VerticalPanel(HorizontalAlignment=HasAlignment.ALIGN_LEFT, StyleName="row")
    row3 = DisclosurePanel("Logic Paths", StyleName="row")
    row4 = HorizontalPanel(HorizontalAlignment=HasAlignment.ALIGN_LEFT, StyleName="row")
    panel.add(row0)
    panel.add(row1)
    panel.add(row2)
    panel.add(row3)
    panel.add(row4)

    title = HTML("Ori DE Randomizer (v2.0.1)", StyleName="title")

    row0.add(title)

    #row 1
    row1_1 = HorizontalPanel(StyleName="inner_row")
    row1_2 = HorizontalPanel(StyleName="inner_row")
    row1_3 = HorizontalPanel(StyleName="inner_row")

    row1.add(row1_1)
    row1.add(row1_2)
    row1.add(row1_3)

    logicText = HTML("Logic", StyleName="label")
    global logicSelection
    logicSelection = ListBox(VisibleItemCount=1, StyleName="dropdown")
    logicSelection.addItem("Casual")
    logicSelection.addItem("Standard")
    logicSelection.addItem("Expert")
    logicSelection.addItem("Master")
    logicSelection.addItem("Hard")
    logicSelection.addItem("OHKO")
    logicSelection.addItem("0 XP")
    logicSelection.addItem("Glitched")
    logicSelection.addItem("Custom")
    logicSelection.setSelectedIndex(1)

    logicListener = LogicListener(logicSelection)

    row1_1.add(logicText)
    row1_1.add(logicSelection)

    modeText = HTML("Mode", StyleName="label")
    global modeSelection
    modeSelection = ListBox(VisibleItemCount=1, StyleName="dropdown")
    modeSelection.addItem("Default")
    modeSelection.addItem("Shards")
    modeSelection.addItem("Limitkeys")
    modeSelection.addItem("Clues")
    modeSelection.setSelectedIndex(1)

    row1_2.add(modeText)
    row1_2.add(modeSelection)

    diffText = HTML("Path Difficulty", StyleName="label")
    global diffSelection
    diffSelection = ListBox(VisibleItemCount=1, StyleName="dropdown")
    diffSelection.addItem("Easy")
    diffSelection.addItem("Normal")
    diffSelection.addItem("Hard")
    diffSelection.setSelectedIndex(1)

    row1_3.add(diffText)
    row1_3.add(diffSelection)

    #row 2
    variationText = HTML("Variations", StyleName="section")
    variationPanel = HorizontalPanel()

    row2.add(variationText)
    row2.add(variationPanel)

    variations1 = VerticalPanel(StyleName="var_column")
    variations2 = VerticalPanel(StyleName="var_column")
    variations3 = VerticalPanel(StyleName="var_column")

    variationPanel.add(variations1)
    variationPanel.add(variations2)
    variationPanel.add(variations3)

    global forceBox
    global hardBox
    global noTeleBox

    forceBox = CheckBox("Force Trees")
    hardBox = CheckBox("Hard Mode")
    noTeleBox = CheckBox("No Teleporters")

    forceBox.setChecked(True)

    variations1.add(forceBox)
    variations1.add(hardBox)
    variations1.add(noTeleBox)

    global starvedBox
    global ohkoBox
    global noPlantsBox

    starvedBox = CheckBox("Starved")
    ohkoBox = CheckBox("OHKO")
    noPlantsBox = CheckBox("No Plants")

    variations2.add(starvedBox)
    variations2.add(ohkoBox)
    variations2.add(noPlantsBox)

    global nonProgMapBox
    global zeroBox
    global noBonusBox

    nonProgMapBox = CheckBox("Discrete Mapstones")
    zeroBox = CheckBox("0 XP")
    noBonusBox = CheckBox("No Bonuses")

    variations3.add(nonProgMapBox)
    variations3.add(zeroBox)
    variations3.add(noBonusBox)

    #row 3
    pathsPanel = HorizontalPanel()

    row3.add(pathsPanel)

    paths1 = VerticalPanel(StyleName="logic_column")
    paths2 = VerticalPanel(StyleName="logic_column")
    paths3 = VerticalPanel(StyleName="logic_column")
    paths4 = VerticalPanel(StyleName="logic_column")
    paths5 = VerticalPanel(StyleName="logic_column")

    pathsPanel.add(paths1)
    pathsPanel.add(paths2)
    pathsPanel.add(paths3)
    pathsPanel.add(paths4)
    pathsPanel.add(paths5)

    customPathListener = CustomPathListener()

    global pathNormal
    global pathLure
    global pathExtended

    pathNormal = CheckBox("Normal")
    pathLure = CheckBox("Lure")
    pathExtended = CheckBox("Extended")

    pathNormal.setChecked(True)
    pathLure.setChecked(True)

    pathNormal.addClickListener(customPathListener)
    pathLure.addClickListener(customPathListener)
    pathExtended.addClickListener(customPathListener)

    paths1.add(pathNormal)
    paths1.add(pathLure)
    paths1.add(pathExtended)

    global pathSpeed
    global pathLureHard
    global pathExtendedDamage

    pathSpeed = CheckBox("Speed")
    pathLureHard = CheckBox("Lure-Hard")
    pathExtendedDamage = CheckBox("Extended-Damage")

    pathSpeed.setChecked(True)

    pathSpeed.addClickListener(customPathListener)
    pathLureHard.addClickListener(customPathListener)
    pathExtendedDamage.addClickListener(customPathListener)

    paths2.add(pathSpeed)
    paths2.add(pathLureHard)
    paths2.add(pathExtendedDamage)

    global pathDBoostLight
    global pathDBash
    global pathExtreme

    pathDBoostLight = CheckBox("DBoost-Light")
    pathDBash = CheckBox("DBash")
    pathExtreme = CheckBox("Extreme")

    pathDBoostLight.setChecked(True)

    pathDBoostLight.addClickListener(customPathListener)
    pathDBash.addClickListener(customPathListener)
    pathExtreme.addClickListener(customPathListener)

    paths3.add(pathDBoostLight)
    paths3.add(pathDBash)
    paths3.add(pathExtreme)

    global pathDBoost
    global pathCDash
    global pathTimedLevel

    pathDBoost = CheckBox("DBoost")
    pathCDash = CheckBox("CDash")
    pathTimedLevel = CheckBox("Timed-Level")

    pathDBoost.addClickListener(customPathListener)
    pathCDash.addClickListener(customPathListener)
    pathTimedLevel.addClickListener(customPathListener)

    paths4.add(pathDBoost)
    paths4.add(pathCDash)
    paths4.add(pathTimedLevel)

    global pathDBoostHard
    global pathCDashFarming
    global pathGlitched

    pathDBoostHard = CheckBox("DBoost-Hard")
    pathCDashFarming = CheckBox("CDash-Farming")
    pathGlitched = CheckBox("Glitched")

    pathDBoostHard.addClickListener(customPathListener)
    pathCDashFarming.addClickListener(customPathListener)
    pathGlitched.addClickListener(customPathListener)

    paths5.add(pathDBoostHard)
    paths5.add(pathCDashFarming)
    paths5.add(pathGlitched)

    #row 4

    seedPanel = HorizontalPanel("inner_row")

    seedText = HTML("Seed", StyleName="label")
    global seedSelection
    seedSelection = TextBox(StyleName="seed", MaxLength=10)
    global genButton
    genButton = Button("Generate", generate, StyleName='button')

    seedPanel.add(seedText)
    seedPanel.add(seedSelection)

    row4.add(seedPanel)
    row4.add(genButton)

    RootPanel().add(panel)
    pyjd.run()



if __name__ == "__main__":
    main()
