#this is a workoutMaker
#let's hope I remember Python...

import random, re

debug = True


def roundToNearest(x, base = 5):
    return int(base * round(float(x) / base))

class Drill:
    name = ""
    meanReps = None
    repStdDev = None
    reps = None

    meanWeight = None
    weightStdDev = None
    weightStep = 5
    weight = None

    meanSets = None
    setStdDev = None
    sets = None

    def __init__(self, data, r = None, w = None, s = None): # name, meanReps, stdDev):
        self.getData(data)
        self.reps = r
        self.weight = w
        self.sets = s

    def getData(self, data): #data of form "[name] ([meanReps],[stdDev])"
        if debug:
            print ("in getData for Drill\nData is: " + data)
        dataType1 = r"(.*?) \((.*?),(.*?);(.*?),(.*?);(.*?),(.*?)\)"
        dataType2 = r"(.*?) \((.*?),(.*?);(.*?),(.*?)\)"
        dataType3 = r"(.*?) \((.*?),(.*?)\)"
        dataType4 = r"(.*)"

        dataTypes = [dataType1, dataType2, dataType3, dataType4]

        dtCount = 0
        for dt in dataTypes:
            dtCount += 1
            if debug:
                print "in dataType" + str(dtCount)

            pattern = re.compile(dt)
            matcher = pattern.match(data)

            if (matcher != None): #if matcher has matches
                if debug:
                    print ("changing data in Drill")
                    print matcher.groups()
                try:
                    self.name = matcher.group(1)
                    if debug:
                        print "past matcher group 1"
                    self.meanReps = float(matcher.group(2))
                    if debug:
                        print "past matcher group 2"
                    self.repStdDev = float(matcher.group(3))
                    if debug:
                        print "past matcher group 3"
                    self.meanWeight = float(matcher.group(4))
                    if debug:
                        print "past matcher group 4"
                    self.weightStdDev = float(matcher.group(5))
                    if debug:
                        print "past matcher group 5"
                    self.meanSets = float(matcher.group(6))
                    if debug:
                        print "past matcher group 6"
                    self.setStdDev = float(matcher.group(7))
                    if debug:
                        print "past matcher group 7"

                    break

                except IndexError:
                    if debug:
                        print "in except statement, drill is currently:"
                        print self.meanReps
                        print "breaking now"

                    break


        if debug:
            print ("====="*5)

    def getDataAsString(self):
        string = self.name
        if self.meanReps != None:
            string += " (" + str(self.meanReps) + ", " + str(self.repStdDev)
            if self.meanWeight != None:
                string += "; " + str(self.meanWeight) + ", " + str(self.weightStdDev)
                if self.meanSets != None:
                    string += "; " + str(self.meanSets) + ", " + str(self.setStdDev)

            string += ")"

        return string


    def __repr__(self):
        string = ""
        if self.reps != None:
            string = self.name + ": " + str(self.reps)

            if self.weight != None:
                string += " w/ " + str(self.weight)

            if self.sets != None:
                string += ", x" + str(self.sets)

        else:
            string = self.getDataAsString()

        return string

    def getDrill(self):
        if debug:
            print "Im in getDrill for " + str(self)

        if self.meanReps != None:
            self.reps = int(round(random.gauss(self.meanReps, self.repStdDev)))
        if self.meanWeight != None:
            if debug:
                print "getting weight (the problem area)"
                print "meanWeight: " + str(self.meanWeight)
                print "weightStdDev: " + str(self.weightStdDev)
                print "weightStep: " + str(self.weightStep)

            self.weight = int(roundToNearest(random.gauss(self.meanWeight, self.weightStdDev),
                              self.weightStep))

            if debug:
                print "weight: " + str(self.weight)

        if self.meanSets != None:
            self.sets = int(round(random.gauss(self.meanSets, self.setStdDev)))

        return Drill(self.getDataAsString(), self.reps, self.weight, self.sets)

    def printDrill(self):
        returnString = self.name + ": mean reps: " + str(self.meanReps)
        returnString += ", rep standard deviation: " + str(self.repStdDev) + "\n"
        if self.meanWeight != None:
            returnString += "mean weight: " + str(self.meanWeight)
            returnString += ", weight std dev: " + str(self.weightStdDev)
        if self.meanSets != None:
            returnString += "mean sets: " + str(self.meanSets)
            returnString += ", standard deviation: " + str(self.setStdDev)

        return returnString

    def improve(self, factor):
        self.meanReps = round(self.meanReps * factor, 1)
        self.meanWeight = round(self.meanWeight * factor, 1)

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
        if (number < 0):
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
bball = DrillReader("drills-basketball.txt")
running =  DrillReader("drills-running.txt")
track = DrillReader("drills-track.txt")

warmup =  dr.getDrills(0, True) #warmup

highJump = track.getDrills(1,False, 10)

ballHandle1 = bball.getDrills(0, False, 12)
ballHandle2 = bball.getDrills(1, False, 10)
shootWarmup = bball.getDrills(2, True)
shooting    = bball.getDrills(3, False, 10)

core    = dr.getDrills(3, False, 20)
upperBody = dr.getDrills(2, False, 10)
stretch = dr.getDrills(4, False, 20)

BREAK = "=====" * 2 + "\n"

print warmup

print BREAK

print highJump

print BREAK

print ballHandle1
print ballHandle2
print shootWarmup
print shooting
print ballHandle1
print shooting
print ballHandle2

print BREAK

print warmup
print core
print upperBody
print stretch
