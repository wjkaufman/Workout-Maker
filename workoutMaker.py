#this is a workoutMaker
#let's hope I remember Python...
import random, re

# print "hello world\n\n=====\n\n"

debug = False

class Drill:
    name = ""
    meanReps = 10
    repStdDev = 5
    reps = None

    meanSets = None
    setStdDev = None
    sets = None

    meanWeight = None
    weightStdDev = None
    weightStep = 10
    weight = None


    def __init__(self, data, r = None, s = None, w = None): # name, meanReps, stdDev):
        self.getData(data)
        self.reps = r
        self.sets = s
        self.weight = w

    def getData(self, data): #data of form "[name] ([meanReps],[stdDev])"
        if debug:
            print ("in getData for Drill\nData is: " + data)
        dataType1 = r"(.*?) \((.*?),(.*?);(.*?),(.*?);(.*?),(.*?)\)"
        dataType2 = r"(.*?) \((.*?),(.*?);(.*?),(.*?)\)"
        dataType3 = r"(.*?) \((.*?),(.*?)\)"
        dataTypes = [dataType1, dataType2, dataType3]

        for dt in dataTypes:
            pattern = re.compile(dt)
            matcher = pattern.match(data)



            if (matcher != None): #if matcher has matches
                if debug:
                    print ("changing data in Drill")
                    print matcher.groups()
                try:
                    self.name = matcher.group(1)
                    self.meanReps = float(matcher.group(2))
                    self.repStdDev = float(matcher.group(3))
                    self.meanSets = float(matcher.group(4))
                    self.setStdDev = float(matcher.group(5))
                    self.meanWeight = float(matcher.group(6))
                    self.weightStdDev = float(matcher.group(7))
                except IndexError:
                    if debug:
                        print "in except statement"
                    print "IndexError caught"
                return

        if debug:
            print ("====="*5)

    def getDataAsString(self):
        string = self.name + " (" + str(self.meanReps) + ", " + str(self.repStdDev)
        if self.meanSets != None:
            string += "; " + str(self.meanSets) + ", " + str(self.setStdDev)
            if self.meanWeight != None:
                string += "; " + str(self.meanWeight) + ", " + str(self.weightStdDev)

        string += ")"

        return string


    def __repr__(self):
        returnString = self.name + ": " + str(self.reps)

        if self.sets != None:
            returnString += ", x" + str(self.sets)

        return returnString

    def getDrill(self):
        self.reps = int(round(random.gauss(self.meanReps, self.repStdDev)))
        if self.meanSets != None:
            self.sets = int(round(random.gauss(self.meanSets, self.setStdDev)))
        if self.meanWeight != None:
            self.weight = int(round(random.gauss(self.meanWeight, self.weightStdDev)))

        return Drill(self.getDataAsString(), self.reps, self.sets, self.weight)

    def printAll(self):
        returnString = self.name + ": mean reps: " + str(self.meanReps)
        returnString += ", standard deviation: " + str(self.repStdDev) + "\n"
        returnString += "mean sets: " + str(self.meanSets)
        returnString += ", standard deviation: " + str(self.setStdDev)

        return returnString

    def printDrill(self):
        print(self.getDrill())

class DrillGroup:

    drillList = []
    name = "new drillGroup"


    def __init__(self, data):
        self.drillList = []
        self.getData(data)

    def __repr__(self):
        returnString = self.name + ":\n"
        for drill in self.drillList:
            returnString += str(drill) + "\n"

        return returnString

    def getData(self, data):
        if debug:
            print ("in getData for drillGroup")
            print ("data:\n" + data)
        pattern = re.compile(r"=(.*)") #idk if this regex will work
        matcher = pattern.match(data)

        if debug:
            print matcher.groups() #for debugging purposes

        if (len(matcher.groups()) >= 0):
            if debug:
                print ("changing data in DrillGroup")
                print (matcher.group(1))
            self.name = matcher.group(1)

        if debug:
            print self.drillList
            print ("\n=====\n")

    def getRandomDrill(self):
        return self.drillList[random.randint(0, len(self.drillList) - 1)].getDrill()

    def getDrill(self, drillIndex = -1):
        if drillIndex == -1:
            return self.getRandomDrill()
        else:
            return self.drillList[drillIndex].getDrill()

    def getDrills(self, ordered = False, number = -1):
        if (number < 0 or number > len(self.drillList)):
            number = len(self.drillList)
        drills = self.name + ": \n"
        if ordered:
            for drill in self.drillList:
                drills += str(drill.getDrill()) + "\n"

                number += -1
                if number == 0:
                    break
        else:
            for i in range(number):
                drills += str(self.getRandomDrill()) + "\n"

        return drills

    def addDrill(self, d):
        self.drillList.append(d)


class DrillReader:
    drillGroupList = []

    def __init__(self, filePath):
        file = open(filePath, 'r')

        for line in file:
            if (len(line.replace(" ","")) > 1 \
                and line[0] != "#"): #checks for blank lines and comments
                if (line[0] == "="): #new drillGroup
                    dg = DrillGroup(line)
                    if debug:
                        print("in drillReader constructor, adding drillGroup")
                        print dg
                    self.drillGroupList.append(dg)

                else:
                    d = Drill(line)
                    if debug:
                        print("in drillReader constructor, adding drill")
                        print(d)
                        print("adding to " + str(self.drillGroupList[-1]))
                    self.drillGroupList[-1].addDrill(d)

    def __repr__(self):
        returnString = ""
        for drillGroup in self.drillGroupList:
            returnString += str(drillGroup) + "\n=====\n"

        return returnString


    def getDrillGroup(self, index):
        return self.drillGroupList[index]

    def getRandomDrillGroup(self):
        return self.getDrillGroup(int(random.randint(0, len(self.drillGroupList) - 1)))

    def getDrill(self, drillGroup = -1):
        if (drillGroup == -1): #picks a random drillGroup
            return self.getDrill(int( \
                        random.randint(0,len(self.drillGroupList) - 1)))
        else:
            return self.drillGroupList[drillGroup].getDrill()

    def getDrills(self, drillGroup = -1, ordered = False, number = -1):
        dg = None
        if (drillGroup == -1): #picks a random drillGroup
            dg = self.getRandomDrillGroup()
        else:
            dg = self.getDrillGroup(drillGroup)

        if number < 0:
            return dg.getDrills(ordered)
        else:
            return dg.getDrills(ordered, number)

    def printDrillGroups(self):
        index = 0
        for dg in self.drillGroupList:
            print (str(index) + ": " + dg.name)
            index += 1

        print "\n"




##############################
#Implementation and test code#
##############################

dr = DrillReader("drills.txt")

# dr.printDrillGroups()

# 0: warm up
# 1: long jump warmup
# 2: high jump drills
# 3: 1 ball handling
# 4: 2 ball handling
# 5: shooting warmup
# 6: shooting drills
# 7: auxiliary
# 8: upper body
# 9: core
# 10: stretching

warmup =  dr.getDrills(0, True) #warmup

highJump = dr.getDrills(2,False, 10)

ballHandle1 = dr.getDrills(3, False, 12)
ballHandle2 = dr.getDrills(4, False, 10)
shootWarmup = dr.getDrills(5, True)
shooting    = dr.getDrills(6, False, 10)

core    = dr.getDrills(9, False, 20)
upperBody = dr.getDrills(8, False, 10)
stretch = dr.getDrills(10, False, 20)

BREAK = "=====" * 2 + "\n"

# print warmup
#
# print BREAK
#
# print highJump
#
# print BREAK
#
# print ballHandle1
# print ballHandle2
# print shootWarmup
# print shooting
# print ballHandle1
# print shooting
# print ballHandle2
#
# print BREAK

print warmup
print core
print upperBody
print stretch
