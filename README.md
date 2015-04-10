# Workout-Maker
A small Python program to generate workouts based on a list of drills

##How to use it
Add drills to ```drills.txt``` (or to wherever the Python program points) in the form:

```
=[drillType]
[Drill] ([mean # of reps]/[standard deviation for reps])
```

From there, you can edit the implementation code at the bottom of ```workoutMaker.py``` to create sets of drills
from the drillReader (```dr```)


running ```DrillReader#getDrills(drillGroup, ordered, number)``` will return a string of drills from the
specified drillGroup (ordered 0 to n from the order in the drill txt) that is ordered or not (depending on the
boolean parameter) with ```number``` number of drills.

Running the program will then print the workout!

##To Do

* add weight-bearing capabilities to drills, including amount of weight, weight step (25lb to 35lb, 45, etc.)
* make a workout class that has different types of workouts saved
* add an "improve" capability that updates drills, drillGroups, and drillLists by increasing meanReps and changing standard deviation
* add set capabilities to drills (drillgroup?)
* supersets?
* prevent drills from coming up 2 in a row
