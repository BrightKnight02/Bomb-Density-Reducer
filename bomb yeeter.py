import numpy
import json

rankableSpacing = 20 #ms
maxSpace = .25 #beats. Maximum space between bombs in a tunnel. if you are less dense than this what the crap.

def main():
    files, bpm = getFiles()
    minSpace = rankableSpacing / 60000 * bpm #beats
    for i in files:
        diffFile = open(i, "r")
        diff = json.load(diffFile)
        diffFile.close()
        snakes = findSnakes(diff)
        yeetBombs(diff)
        placeBombs(diff, snakes, minSpace)
        diffFile = open(i, "w")
        json.dump(diff, diffFile)
        diffFile.close()
    
"""
Currently there are bugs with bombs
"""

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
            if len(snakes[a][b]) % 2 > 0:
                snakes[a][b].append(i["_time"])
            elif i["_time"] < snakes[a][b][-1] + maxSpace:
                snakes[a][b][-1] = i["_time"]
            else:
                snakes[a][b].append(i["_time"])
    return snakes
    
def yeetBombs(diff):
    toYeet = []
    for i in diff["_notes"]:
        if i["_type"] == 3:
            toYeet.append(i)
    for i in toYeet:
        diff["_notes"].remove(i)
        
def placeBombs(diff, snakes, minSpace):
    for i in range(3):
        for j in range(4):
            if snakes[i][j][0] != -1:
                for k in range(int(len(snakes[i][j]) / 2)):
                    if snakes[i][j][k] == snakes[i][j][k + 1]:
                        diff["_notes"].append({
  "_time" : snakes[i][j][k],
  "_lineIndex" : j,
  "_lineLayer" : i,
  "_type" : 3,
  "_cutDirection" : 1
})
                    else:
                        for l in numpy.arange(snakes[i][j][k], snakes[i][j][k + 1], minSpace):
                            diff["_notes"].append({
  "_time" : l,
  "_lineIndex" : j,
  "_lineLayer" : i,
  "_type" : 3,
  "_cutDirection" : 1
})
    sorted(diff["_notes"], key = lambda i : i["_time"])
    print(diff["_notes"])
   
def getFiles():
    infoFile = open("info.dat", "r")
    info = json.load(infoFile)
    bpm = info["_beatsPerMinute"]
    fileNames = []
    for i in info["_difficultyBeatmapSets"][0]["_difficultyBeatmaps"]:
        fileNames.append(i["_beatmapFilename"])
    infoFile.close()
    return fileNames, bpm
    
if __name__ == "__main__":
    main()