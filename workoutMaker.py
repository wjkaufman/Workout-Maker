#this is a workoutMaker
#let's hope I remember Python...
import random, re
print "hello world\n\n=====\n\n"

debug = False

class Drill:
    name = "";
    meanReps = 10;
    stdDev = 5;

    def __init__(self, data): # name, meanReps, stdDev):
        self.getData(data)

    def getData(self, data): #data of form "[name] ([meanReps],[stdDev])"
        if debug:
            print ("in getData for Drill\nData is: " + data)
        pattern = re.compile(r"(.*?) \((.*?)/(.*?)\)")
        matcher = pattern.match(data)

        if debug:
            print matcher.groups()

        if (len(matcher.groups()) > 0):
            if debug:
                print ("changing data in Drill")
            self.name = matcher.group(1)
            self.meanReps = int(matcher.group(2))
            self.stdDev = int(matcher.group(3))

        if debug:
            print ("=====")


    def __repr__(self):
        returnString = self.name + ": mean reps: " + str(self.meanReps) + \
                        ", standard deviation: " + str(self.stdDev)
        return returnString

    def getDrill(self):
        drill = self.name + ": " + \
                str(int(round(random.gauss(self.meanReps, self.stdDev))))

        return drill

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

    def getDrill(self, drillIndex = -1):
        if drillIndex == -1:
            return self.drillList[random.randint(0, len(self.drillList) - 1)].getDrill()
        else:
            return self.drillList[drillIndex].getDrill()

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

    def getDrill(self, drillGroup = -1):
        if (drillGroup == -1): #picks a random drillGroup
            return self.getDrill(int( \
                        random.randint(0,len(self.drillGroupList) - 1)))
        else:
            return self.drillGroupList[drillGroup].getDrill()

    def printDrillGroups(self):
        index = 0
        for dg in self.drillGroupList:
            print (str(index) + ": " + dg.name)
            index += 1




##############################
#Implementation and test code#
##############################

dr = DrillReader("drills.txt")

# print dr

for i in range(20):
    print dr.getDrill(2)

# dr.printDrillGroups()
