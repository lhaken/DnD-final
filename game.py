from random import randint
import dungeon
import inventory
import entities

hans = []
zeMap = []
big = 10
def generateMap(hans, big):
    global ListOfDungeons
    
    for i in range(big):
        temp = []
        for j in range(big):
            temp.append("")
        hans.append(temp)

    top = big - 1
    with open ("locations.txt", 'r') as L:
        file = L.read()
        file = file.split(", ")

    k = len(file) - 1
    for i, coords in enumerate(hans):
        for j, coord in enumerate(coords):
            rand = randint(0, k)
            hans[i][j] = file[rand]

    for i, coords in enumerate(hans):
        for j, coord in enumerate(coords):
            if i == 0 or j == 0 or i == top or j == top:
                which = randint(1, 2)
                if which == 1:
                    hans[i][j] = "beach"
                else:
                    hans[i][j] = "cliff"

    ListOfDungeons = {}
    inx = 1
    while inx < 8:
        X = randint(0, top)
        Y = randint(0, top)
        if inx <= 3:
            s = str(X) + ',' + str(Y)
            ListOfDungeons[s] = "easy"+str(inx)
            hans[X][Y] = "dungeon"
            inx += 1
        elif inx <= 5:
            if hans[X][Y] != "dungeon":
                s = str(X) + ',' + str(Y)
                ListOfDungeons[s] = "medium"+str(inx - 3)
                hans[X][Y] = "dungeon"
                inx += 1
        elif inx == 6:
            if hans[X][Y] != "dungeon":
                s = str(X) + ',' + str(Y)
                ListOfDungeons[s] = "hard"
                hans[X][Y] = "dungeon"
                inx += 1
        else:
            if hans[X][Y] != "dungeon":
                s = str(X) + ',' + str(Y)
                ListOfDungeons[s] = "final"
                hans[X][Y] = "dungeon"
                inx += 1
    return hans, big

def spawning(hans, zeMap, coordX, coordY, big):
    for i in range(big):
        temp = []
        for j in range(big):
            temp.append("       ")
        zeMap.append(temp)
    zeMap[coordX][coordY] = hans[coordX][coordY] + ", spawn"
    pozice=hans[coordX][coordY]
    return zeMap, pozice

generateMap(hans, big)
top = big - 1
alt = big//2 - 3
lat = big//2 + 3
coordX = randint(alt, lat)
coordY = randint(alt, lat)
spawning(hans, zeMap, coordX, coordY, big)
pozice=hans[coordX][coordY]
listPozic=[[coordX, coordY]]

def south(hans, coordX, listPozic):
    if coordX+1>top:
        print("There lies sea ahead. You shall not pass.")
    else:
        coordX+=1; listPozic+=[[coordX, coordY]]
    return coordX, listPozic

def north(hans, coordX, listPozic):
    if coordX-1<0:
        print("There lies sea ahead. You shall not pass.")
    else:
        coordX-=1; listPozic+=[[coordX, coordY]]
    return coordX, listPozic

def east(hans, coordY, listPozic):
    if coordY+1>top:
        print("There lies sea ahead. You shall not pass.")
    else:
        coordY+=1; listPozic+=[[coordX, coordY]]
    return coordY, listPozic

def west(hans, coordY, listPozic):
    if coordY-1<0:
        print("There lies sea ahead. You shall not pass.")
    else:
        coordY-=1; listPozic+=[[coordX, coordY]]
    return coordY, listPozic

def zpet(listPozic):
    if len(listPozic)>1: listPozic.pop(); coordX=listPozic[-1][0]; coordY=listPozic[-1][1]
    else: coordX=listPozic[-1][0]; coordY=listPozic[-1][1]
    return coordX, coordY, listPozic

chestky={}
wizardi={}
def dungeonMove():
    global option
    
    directions = ["north", "south", "west", "east", "leave"]
    option = str(input("Where would you like to go? > ")).lower()
    while option not in directions:
        print("Wrong input - try north, south, west or east")
        option = str(input("Where would you like to go? > ")).lower()
    return
    
def pohyb(hans, zeMap, coordX, coordY, listPozic, konec, pozice):
    global d
    global player
    
    zeMap[coordX][coordY] = hans[coordX][coordY]
    pozice=hans[coordX][coordY]
    print("You've walked to " + pozice)
    prikaz=input("What to do? ")
    inventory.bezInterakce(prikaz, inventory.inventoryDict)
    if prikaz.lower()=="inventory"or prikaz.lower()=="info"or prikaz.lower()=="stats"or prikaz.lower()=="equip"or prikaz.lower()=="unequip"or prikaz.lower()=="drop"or prikaz.lower()=="skip"or prikaz.lower()=="help": pass
    elif prikaz.lower()=="south": coordX, listPozic=south(hans, coordX, listPozic)
    elif prikaz.lower()=="north": coordX, listPozic=north(hans, coordX, listPozic)
    elif prikaz.lower()=="east": coordY, listPozic=east(hans, coordY, listPozic)
    elif prikaz.lower()=="west": coordY, listPozic=west(hans, coordY, listPozic)
    elif prikaz.lower()=="back": coordX, coordY, listPozic=zpet(listPozic)
    elif prikaz.lower()=="end": konec=True
    elif prikaz.lower()=="chart":
        for coords in zeMap:
            for coord in coords:
                print(coord + ' ' *(9-len(coord)) + ' ', end=" ")
            print(end="\n")
    elif prikaz.lower()=="enter":
        if pozice == "dungeon":
            d = dungeon.activeDungeon()
            d.loadDungeon(ListOfDungeons["{},{}".format(coordX, coordY)])
            d.showMap()
            initPlayer()
            if d.name == "hard":
                if player.lvl < 5:
                    print("This dungeon is too hard for you. Level up and come back.")
                    pass
                else:
                    while d.leave == False and konec == False:
                        dungeonMove()
                        d.move(option)
                        d.showMap()
                        if d.checkMonster() == True:
                            fight(d.enemyName)
                            if player.hp <= 0:
                                konec = True
                            else:
                                d.monsterDefeat()
                                if d.dungeonClear()==True:
                                    d.leave=True
                        else:
                            pass
                    if player.hp <= 0:
                        pass
                    elif d.dungeonClear() == True:
                        print("Congrats! You cleared the dungeon!")
                        inventory.staty['level'] += 3
                        inventory.staty['hp'] = player.hp
                        hans[coordX][coordY] = "cleared"
                    elif d.leave == True:
                        print("You left the dungeon. God knows why, but you can return anytime.")
                    else:
                        print("Why did this happen? Please contact my author with unknown_error#34")
            elif d.name == "final":
                if player.lvl < 8:
                    print("This dungeon is too hard for you. Level up and come back.")
                    pass
                else:
                    while d.leave == False and konec == False:
                        dungeonMove()
                        d.move(option)
                        d.showMap()
                        if d.checkMonster() == True:
                            fight(d.enemyName)
                            if player.hp <= 0:
                                konec = True
                            else:
                                d.monsterDefeat()
                                if d.dungeonClear()==True:
                                    d.leave=True
                        else:
                            pass
                    if player.hp <= 0:
                        pass
                    elif d.dungeonClear() == True:
                        playerWin()
                        konec = True
                    elif d.leave == True:
                        print("You left the dungeon. God knows why, but you can return anytime.")
                    else:
                        print("Why did this happen? Please contact my author with unknown_error#34")
            else:
                while d.leave == False and konec == False:
                    dungeonMove()
                    d.move(option)
                    d.showMap()
                    if d.checkMonster() == True:
                        fight(d.enemyName)
                        if player.hp <= 0:
                            konec = True
                        else:
                            d.monsterDefeat()
                            if d.dungeonClear()==True:
                                d.leave=True
                    else:
                        pass
                if player.hp <= 0:
                    pass
                elif d.dungeonClear() == True:
                    print("Congrats! You cleared the dungeon!")
                    if d.name == "easy1" or d.name == "easy2" or d.name == "easy3":
                        inventory.staty['level'] += 1
                        inventory.staty['hp'] = player.hp
                    elif d.name == "medium1" or d.name == "medium2":
                        inventory.staty['level'] += 2
                        inventory.staty['hp'] = player.hp
                    hans[coordX][coordY] = "cleared"
                elif d.leave == True:
                    print("You left the dungeon. God knows why, but you can return anytime.")
                else:
                    print("Why did this happen? Please contact my author with unknown_error#34")
        elif pozice == "cave" or pozice == "monastery" or pozice == "city" or pozice == "village" or pozice == "farm":
            if str([coordX, coordY]) in chestky.keys():
                if chestky[str([coordX, coordY])]==False:
                    print("There is no chest in the", pozice)
                    print("There is nothing else you can do in", pozice)
                else:
                    chestka=chestky[str([coordX, coordY])]
                    print("You have found a chest.")
                    prikaz=input("There are "+str(len(chestka))+" items in the chest, what to do? ")
                    inventory.interakceSChestkou(prikaz, inventory.inventoryDict, chestka)
            else:
                random=randint(0,10)
                if random>5:
                    chestka=inventory.vytvoreniChestky()
                    print("You have found a chest.")
                    prikaz=input("There are "+str(len(chestka))+" items in the chest, what to do? ")
                    inventory.interakceSChestkou(prikaz, inventory.inventoryDict, chestka)
                    chestky[str([coordX, coordY])]=chestka
                else:
                    print("There is no chest in the", pozice)
                    print("There is nothing else you can do in", pozice)
                    chestky[str([coordX, coordY])]=False
        elif pozice == "forest" or pozice == "lake"or pozice == "swamp"or pozice == "mountains":
            if str([coordX, coordY]) in wizardi.keys():
                if wizardi[str([coordX, coordY])]==False:
                    print("There is no one in the", pozice)
                    print("You can't do anything else in the", pozice)
                else:
                    wizard=wizardi[str([coordX, coordY])]
                    print("You have found a wizard.")
                    prikaz=input("He can enchant one of your items by "+str(wizard[0])+". ")
                    inventory.interakceSWizem(prikaz, inventory.inventoryDict, inventory.staty, wizard, inventory.coJeNasazeno)
            else:
                random=randint(0,10)
                if random>6:
                    wizard=inventory.vytvoreniWizarda()
                    print("You have found a wizard.")
                    prikaz=input("He can enchant one of your items by "+str(wizard[0])+". ")
                    inventory.interakceSWizem(prikaz, inventory.inventoryDict, inventory.staty, wizard, inventory.coJeNasazeno)
                    wizardi[str([coordX, coordY])]=wizard
                else:
                    print("There is no one in the", pozice)
                    print("You can't do anything else in the", pozice)
                    wizardi[str([coordX, coordY])]=False
        elif pozice == "cleared":
            print("This dungeon has been cleared. Find yourself another challenge brave adventurer.")
        else: print("There is nothing to enter BAKA!")
    else: print("Wrong command, maybe typo.")
    return coordX, coordY, listPozic, konec

def initPlayer():
    global player

    player=entities.activeEnemy()
    player.findEntity("player")
    player.lvl = int(inventory.staty['level'])
    player.hp = int(inventory.staty['hp'])
    player.dmg = int(inventory.staty['dmg'])
    player.spd = int(inventory.staty['speed'])
    player.armor=int(inventory.staty['armor'])

def roll():
    global playerRoll
    global enemyRoll
    
    playerRoll = randint(0, 10)
    enemyRoll = randint(0, 10)

def fight(entity):
    global player
    global keyTaken
    global goblinSlayed
    global doorsUnlocked
    global enemy

    roll()
    enemy = entities.activeEnemy()
    enemy.findEntity(entity)
    if playerRoll >= enemyRoll:
        print("{} encountered.".format(enemy.name.capitalize()))
        while player.hp > 0 and enemy.hp > 0:
            action = input("What to do? ")
            if action == "cover":
                if player.armor>=enemy.dmg:
                    print("You've dodged enemy attack.")
                    print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
                else:
                    print("You've tried dodge an enemy attack, but you've failed.")
                    player.hp=player.hp-(enemy.dmg-player.armor)
                    print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
                print(" ")
            elif action == "attack":
                round(player, enemy)
                round(enemy, player)
            else:
                print("Wrong move. " + enemy.name.capitalize() + " is attacking you!")
                player.hp -= enemy.dmg
                print(enemy.name.capitalize() + " deals " + str(enemy.dmg) + " damage.")
                print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
    elif playerRoll < enemyRoll:
        print("{} encountered.".format(enemy.name.capitalize()))
        while player.hp > 0 and enemy.hp > 0:
            action = input("What to do? ")
            if action == "cover":
                if player.armor>enemy.dmg:
                    print("You've dodged enemy attack.")
                    print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
                else:
                    print("You've tried dodge an enemy attack, but you've failed.")
                    player.hp=player.hp-(enemy.dmg-player.armor)
                    print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
                print(" ")
            elif action == "attack":
                round(enemy, player)
                round(player, enemy)
            else:
                print("Wrong move. " + enemy.name.capitalize() + " is attacking you!")
                player.hp -= enemy.dmg
                print(enemy.name.capitalize() + " deals " + str(enemy.dmg) + " damage.")
                print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
                print(" ")
    else:
        print("Unknown error")

def round(attacker, defender):
    global konec
    
    dodge1 = randint(0, 20)
    dodge2 = randint(0, 20)
    if attacker.hp > 0 and defender.hp > 0:
        if dodge1 < defender.speed:
            print("{} have missed.".format(attacker.name.capitalize()))
        else:
            defender.hp -= attacker.dmg
            print(attacker.name.capitalize() + " deals " + str(attacker.dmg) + " damage.")
            print("Player has " + str(player.hp) + " ♥, while enemy has " + str(enemy.hp) + " ♥.")
            print(" ")
            if defender.hp <= 0:
                print(defender.name.capitalize() + " was killed!")
                return
            else:
                pass
    else:
        pass

def playerWin():
    print("""\n<>=======() 
(/\___   /|\\          ()==========<>_
      \_/ | \\        //|\   ______/ \)
        \_|  \\      // | \_/
          \|\/|\_   //  /\/
           (oo)\ \_//  /
          //_/\_\/ /  |
         @@/  |=\  \  |         Congratulations! You win.
              \_=\_ \ |
                \==\ \|\_ 
             __(\===\(  )\      Game by: Kryštof Luhan
            (((~) __(_/   |              Lukáš Pravda
                 (((~) \  /              Lukáš Haken
                 ______/ /
                 '------'\n""")
    input()
    return


print("\nType: help - to go to the tutorial page!\n")
konec=False
while konec==False: coordX, coordY, listPozic, konec=pohyb(hans, zeMap, coordX, coordY, listPozic, konec, pozice)
