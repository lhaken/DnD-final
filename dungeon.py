import random
import entities

class dungeon:
    def createDungeon(self):
        global dungeonScheme
        
        print("P - player, R - room, M - monster, N - nothing") 
        print("[[0,0][0,1][0,2]]")
        print("[[1,0][1,1][1,2]]")
        print("[[2,0][2,1][2,2]]")
        self.name = input("Dungeon name > ")
        r0 = input("row #0 > P,")
        r1 = input("row #1 > ")
        r2 = input("row #2 > ")
        dungeonScheme = [["P", r0.split(",")[0], r0.split(",")[1]],
                   [r1.split(",")[0],r1.split(",")[1],r1.split(",")[2]],
                   [r2.split(",")[0],r2.split(",")[1],r2.split(",")[2]]]
        for row in dungeonScheme:
            print(row)

    def addMonster(self):
        monsterInput = input("Monster name > ")
        if entities.activeEnemy().findEntity(monsterInput):
            self.monster = monsterInput
        else:
            print("Monster doesn't exist. Please try again.")
            self.addMonster()

    def saveDungeon(self):
        dungeonFile = open("dungeons.txt", "a")
        dungeonFile.write("#{}\n".format(self.name))
        yIndex = 0
        pos = [-1, 1]
        for row in dungeonScheme:
            xIndex = 0
            for room in row:
                doors = ""
                ownCords = "{},{}".format(yIndex, xIndex)
                if dungeonScheme[yIndex][xIndex] == "M":
                    self.addMonster()
                else:
                    self.monster = "none"
                if dungeonScheme[yIndex][xIndex] == "R" or dungeonScheme[yIndex][xIndex] == "P" or dungeonScheme[yIndex][xIndex] == "M":
                    for num in pos:
                        try:
                            if dungeonScheme[yIndex + num][xIndex] == "R" or dungeonScheme[yIndex + num][xIndex] == "P" or dungeonScheme[yIndex + num][xIndex] == "M":
                                if yIndex + num == -1:
                                    pass
                                else:
                                    newDoor = "{},{}|".format(yIndex + num, xIndex)
                                    doors = doors + newDoor
                        except:
                            pass
                        try:
                            if dungeonScheme[yIndex][xIndex + num] == "R" or dungeonScheme[yIndex][xIndex + num] == "P" or dungeonScheme[yIndex][xIndex + num] == "M":
                                if xIndex + num == -1:
                                    pass
                                else:
                                    newDoor = "{},{}|".format(yIndex, xIndex + num)
                                    doors = doors + newDoor
                        except:
                            pass
                doors = doors[:-1]
                dungeonFile.write("{};{};{}\n".format(ownCords, doors, self.monster))
                xIndex += 1
            yIndex += 1
        dungeonFile.close()

class activeDungeon:
    global checkMove
    def __init__(self):
        self.leave = False
    
    def loadDungeon(self, name):
        global dungeonMap
        global playerX
        global playerY
        global foundDungeon
        global dungeon

        xIndex = 1 # rooms
        playerX = 0
        playerY = 0
        
        lineIndex = 1
        dungeonMap = [["P"],[],[]]
        
        with open("dungeons.txt", "r") as dungeonFile:
            dungeonsText = dungeonFile.read()
            
        allDungeons = dungeonsText.split("#")
        allDungeons.pop(0)
        for dungeon in allDungeons:
            if dungeon.split("\n")[0] == name:
                self.name = name
                foundDungeon = dungeon.split("\n")
                foundDungeon.pop(0) # removing the name
                for y in range(0, 3):
                    for x in range(xIndex, 3):
                        room = foundDungeon[lineIndex]
                        if room.split(";")[1] != "" and room.split(";")[2] == "none":
                            dungeonMap[y].append("R")
                        elif room.split(";")[1] != "" and room.split(";")[2] != "none":
                            dungeonMap[y].append("M")
                        else:
                            dungeonMap[y].append("N")
                        lineIndex += 1     
                    xIndex = 0
                return
        print("Dungeon does not exist")
            
    def showMap(self):
        for row in dungeonMap:
            print(row)

    def checkMove(direction):
        global movement
        
        movement = {"north":playerY - 1, "south":playerY + 1, "east":playerX + 1, "west":playerX - 1}
        if movement[direction] < 0 or movement[direction] > 2:
            print("Can't move through walls.")
            return False
        if direction in ["north", "south"]:
            cords = "{},{}".format(movement[direction], playerX)
            for room in foundDungeon:
                if room.split(";")[0] == cords and room.split(";")[1] != "":
                    return True
            print("Can't move through walls.")
            return False
                
        elif direction in ["east", "west"]:
            cords = "{},{}".format(playerY, movement[direction])
            for room in foundDungeon:
                if room.split(";")[0] == cords and room.split(";")[1] != "":
                    return True
            print("Can't move through walls.")
            return False
        else:
            print("out")
            
            return False
        

    def checkMonster(self):
        
        cords = "{},{}".format(playerY, playerX)
        for room in foundDungeon:
            if room.split(";")[0] == cords:
                if room.split(";")[2] != "none":
                    self.enemyName = room.split(";")[2]
                    return True
                else:
                    return False

    def monsterDefeat(self):
        global foundDungeon
        
        roomIndex = 0
        newDungeon = []
        finalRoom = ""
        cords = "{},{}".format(playerY, playerX)
        
        for room in foundDungeon:
            if room.split(";")[0] == cords:
                newRoom = room.split(";")
                newRoom[2] = "none"
                for part in newRoom:
                    finalRoom = finalRoom + part + ";"
                finalRoom = finalRoom[:-1]
                newDungeon.append(finalRoom)
            else:
                newDungeon.append(room)
        newDungeon.pop(-1)
        foundDungeon = newDungeon

    def move(self, direction):
        global dungeonMap
        global playerY
        global playerX
        global leave
        #                 N [x, y - 1]
        #                /\
        #  [x - 1, y] W <  > E [x + 1, y]
        #                \/
        #                 S [x, y + 1]
        if direction == "north":
            if checkMove("north") == True:
                dungeonMap[playerY][playerX] = "R"
                playerY -= 1
                dungeonMap[playerY][playerX] = "P"
        elif direction == "south":
            if checkMove("south") == True:
                dungeonMap[playerY][playerX] = "R"
                playerY += 1
                dungeonMap[playerY][playerX] = "P"
        elif direction == "east":
            if checkMove("east") == True:
                dungeonMap[playerY][playerX] = "R"
                playerX += 1
                dungeonMap[playerY][playerX] = "P"
        elif direction == "west":
            if checkMove("west") == True:
                dungeonMap[playerY][playerX] = "R"
                playerX -= 1
                dungeonMap[playerY][playerX] = "P"
        elif direction == "leave":
            self.leave = True
        else:
            print("unknown error")
            
    def dungeonClear(self):
        for room in foundDungeon:
            if room.split(";")[2] != "none":
                return False
        return True
                             
if __name__ == "__main__":    
    d = dungeon()
    d.createDungeon()
    d.saveDungeon()



