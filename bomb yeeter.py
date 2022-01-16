import numpy
import json
import os
import sys


maxSpace = .25 #beats. Maximum space between bombs in a tunnel. if you are less dense than this what the crap.

def main():
    files, bpm, njss = getFiles()
    valid = False
    while not valid:
        precisionStr  = input("Enter target precision for bombs (0 for max bombs): 1/")
        try:
            precision = int(precisionStr)
            if precision == 0:
                valid = True
            elif precision < 2:
                go = input("This low of precision may cause problems. Proceed? (y/n)").strip().lower()
                if go == "y":
                    valid = True
                    
                else:
                    print("repeating \n")
            else:
                valid = True 
        except:
            print("Error with precision entered")
        
    for i in range(len(files)):
        space = getSpace(njss[i], precision, bpm)
        print(f"In {files[i]}")
        diffFile = open(files[i], "r")
        diff = json.load(diffFile)
        diffFile.close()
        snakes = findSnakes(diff)
        yeetBombs(diff)
        placeBombs(diff, snakes, space)
        diffFile = open("New" + files[i], "w")
        json.dump(diff, diffFile)
        diffFile.close()
        
def getSpace(njs, precision, bpm):
    minSpace = max(bpm / njs / 120, .02 * bpm / 60)
    if precision == 0:
        return minSpace
    elif minSpace > 1 / precision:
        while 1 / precision < minSpace:
            precision /= 2
    return 1 / precision

def findSnakes(diff):
    snakes = []
    for i in range(3):
        snakes.append([])
        for j in range(4):
            snakes[i].append([-1])
    for i in diff["_notes"]:
        if i["_type"] == 3:
            a = i["_lineLayer"]
            b = i["_lineIndex"]
            if snakes[a][b][0] == -1:
                snakes[a][b][0] = i["_time"]
                snakes[a][b].append(i["_time"])
            elif i["_time"] <= snakes[a][b][-1] + maxSpace:
                snakes[a][b][-1] = i["_time"]
            else:
                snakes[a][b].append(i["_time"])
                snakes[a][b].append(i["_time"])
    return snakes
    
def yeetBombs(diff):
    toYeet = []
    yeeted = 0
    for i in diff["_notes"]:
        if i["_type"] == 3:
            toYeet.append(i)
    for i in toYeet:
        diff["_notes"].remove(i)
        yeeted += 1
    print(f"{yeeted} bombs removed")
        
def placeBombs(diff, snakes, minSpace):
    yeeted = 0
    for i in range(3):
        for j in range(4):
            if snakes[i][j][0] != -1:
                for k in range(0, len(snakes[i][j]), 2):
                    if snakes[i][j][k] == snakes[i][j][k + 1]:
                        diff["_notes"].append({
  "_time" : round(snakes[i][j][k], 3),
  "_lineIndex" : j,
  "_lineLayer" : i,
  "_type" : 3,
  "_cutDirection" : 1
})
                        yeeted += 1
                    else:
                        for l in numpy.arange(snakes[i][j][k], snakes[i][j][k + 1], minSpace):
                            diff["_notes"].append({
  "_time" : round(l, 3),
  "_lineIndex" : j,
  "_lineLayer" : i,
  "_type" : 3,
  "_cutDirection" : 1
})
                            yeeted += 1
    sorted(diff["_notes"], key = lambda q : q["_time"])
    print(f"{yeeted} bombs placed")
   
def getFiles():
    infoFile = None
    if os.path.exists("Info.dat"):
        infoFile = open("Info.dat", "r")
    elif os.path.exists("info.dat"):
        infoFile = open("info.dat", "r")
    else:
        input("Error: no Info.dat file detected")
        sys.exit()
        
    info = json.load(infoFile)
    bpm = info["_beatsPerMinute"]
    fileNames = []
    njss = []
    for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]:
        fileNames.append(i["_beatmapFilename"])
        njss.append(i["_noteJumpMovementSpeed"])
    infoFile.close()
    return fileNames, bpm, njss

if __name__ == "__main__":
    main()
    input("Press Enter to close")