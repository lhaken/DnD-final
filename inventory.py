from random import randint
import webbrowser

url = "http://85.70.120.194/"
staty={}
file = open("entities.txt", "r")
allEntities = file.read()
sortedEntities = allEntities.split("$")
for e in sortedEntities:
    if e.split(";")[0] == "player":
        lvl = int(e.split(";")[1].split(":")[1])
        hp = int(e.split(";")[2].split(":")[1])
        dmg = int(e.split(";")[3].split(":")[1])
        speed = int(e.split(";")[4].split(":")[1])
        armor = int(e.split(";")[5].split(":")[1])
        file.close()
        
staty['level']=int(lvl)
staty['hp']=int(hp)
staty['dmg']=int(dmg)
staty['speed']=int(speed)
staty['armor']=int(armor)

file = open("items.txt", "r")
allItems = file.read()
sortedItems = allItems.split("$")
addons={}
for i in sortedItems:
    if i!='':
        if i.split(";")[1]=="\ntype:ADD ON"or i.split(";")[1]=="\ntype:WEAPON"or i.split(";")[1]=="\ntype:ARMOR":
            addons[i.split(";")[0]]=False

coJeNasazeno=[]

class Item:
    def __init__(self, name):
        random=randint(1,3)
        file = open("items.txt", "r")
        allItems = file.read()
        sortedItems = allItems.split("$")
        for i in sortedItems:
            if i.split(";")[0] == name:
                self.name = name
                self.typ = i.split(";")[1].split(":")[1]
                self.lvl = int(i.split(";")[2].split(":")[1])*random
                rawAbility = i.split(";")[3].split(":")[1]
                self.ability = rawAbility.split(" ")[0]
                self.bonus = int(rawAbility.split(" ")[1])*random
                file.close()
        else: file.close()

names=[]
file = open("items.txt", "r")
allItems = file.read()
sortedItems = allItems.split("$")
for i in sortedItems: names+=[i.split(";")[0]]
for i in names:
    if i=='': names.remove(i)
        
def vytvoreniRandomItemu(names):
    name=names[randint(0, len(names)-1)]
    item=Item(name)
    return item

inventoryDict={}
counter={}
def sebrani(inventoryDict, item):
    if item.name not in counter: counter[item.name]=1
    else: counter[item.name]+=1
    itemName=item.name+"#"+str(counter[item.name])

    inventoryDict[itemName]=item

def odhozeni(inventoryDict, staty, addons, coJeNasazeno):
    co=input("What do you want to drop (1 item)? ")
    if co not in inventoryDict.keys(): print("That is not in your inventory.")
    else:
        if inventoryDict[co].typ=="ADD ON"or inventoryDict[co].typ=="WEAPON"or inventoryDict[co].typ=="ARMOR":
            if co in coJeNasazeno: staty[inventoryDict[co].ability.lower()]-=int(inventoryDict[co].bonus); addons[inventoryDict[co].name]=False; coJeNasazeno.remove(co)
        inventoryDict.pop(co)

def informace(inventoryDict):
    co=input("What do you want to explore (1 item)? ")
    if co not in inventoryDict.keys(): print("That is not in your inventory.")
    else: print("level:", inventoryDict[co].lvl); print("ability:", inventoryDict[co].ability); print("bonus:", inventoryDict[co].bonus)
       
def zobrazeniInventare(inventoryDict, addons, coJeNasazeno):
    print("")
    print("YOUR INVENTORY:")
    types=[]
    for key in inventoryDict:
        if inventoryDict[key].typ not in types: types+=[inventoryDict[key].typ]
    for i in types:
        print("")
        print(i)
        for key in inventoryDict:
            if inventoryDict[key].typ==i:
                if i=="ADD ON":
                    if key in coJeNasazeno: print(key, "(equipped)")
                    else: print(key, "(unequipped)")
                elif i=="WEAPON"or i=="ARMOR":
                    if key in coJeNasazeno: print(key, "(in hand)")
                    else: print(key, "(in bag)")
                else: print(key)
    print("")

def zobrazeniStatu(staty):
    print("")
    print("YOUR STATISTICS:")
    print("")
    for key in staty:
        print(key+": "+str(staty[key]))
    print("")

def prohlidnout(item):
    print(item.name), print("level:", item.lvl); print("ability:", item.ability); print("bonus:", item.bonus)

def pouzit(inventoryDict, staty, addons, coJeNasazeno):
    co=input("What do you want to equip (1 item)? ")
    if co not in inventoryDict.keys(): print("That is not in your inventory.")
    else:
        if inventoryDict[co].typ=="ONETIME"or inventoryDict[co].typ=="POTION": staty[inventoryDict[co].ability.lower()]+=int(inventoryDict[co].bonus); inventoryDict.pop(co)
        elif inventoryDict[co].typ=="ADD ON":
            if addons[inventoryDict[co].name]==False: staty[inventoryDict[co].ability.lower()]+=int(inventoryDict[co].bonus); addons[inventoryDict[co].name]=True; coJeNasazeno+=[co]
            elif co in coJeNasazeno: print("You have this equipped already."); return
            elif addons[inventoryDict[co].name]==True: print("You already have equipped this type of item, you have to unequip it or drop it."); return
        elif inventoryDict[co].typ=="WEAPON"or inventoryDict[co].typ=="ARMOR":
            if addons[inventoryDict[co].name]==False: staty[inventoryDict[co].ability.lower()]+=int(inventoryDict[co].bonus); addons[inventoryDict[co].name]=True; coJeNasazeno+=[co]
            elif co in coJeNasazeno: print("You have this in your hand already."); return
            elif addons[inventoryDict[co].name]==True: print("You already have this type of item in your hand, you have to put it in the bag or drop it."); return

def sundat(inventoryDict, staty, addons, coJeNasazeno):
    co=input("What do you want to unequip (1 item)? ")
    if co not in inventoryDict.keys(): print("That is not in your inventory.")
    else:
        if inventoryDict[co].typ=="ADD ON":
            if co in coJeNasazeno: staty[inventoryDict[co].ability.lower()]-=int(inventoryDict[co].bonus); addons[inventoryDict[co].name]=False; coJeNasazeno.remove(co)
            else: print("You do not have this equipped.")
        elif inventoryDict[co].typ=="WEAPON"or inventoryDict[co].typ=="ARMOR":
            if co in coJeNasazeno: staty[inventoryDict[co].ability.lower()]-=int(inventoryDict[co].bonus); addons[inventoryDict[co].name]=False; coJeNasazeno.remove(co)
            else: print("You do not have this in your hand.")   
        else: print("You can not unequip this.")

def vytvoreniChestky():
    chestka=[]
    random=randint(2,5)
    for i in range(random):
        chestka.append(vytvoreniRandomItemu(names))
    return chestka

def prohlidnoutChestku(chestka):
    print("")
    print("CHEST:")
    for k in chestka:
        print(k.name)
    print("")
    take=0
    for i in range(len(chestka)):
        prikaz=input("What to do with the "+chestka[i-take].name+"? ")
        interakceSItememem(prikaz, inventoryDict, chestka[i-take])
        for j in inventoryDict:
            if chestka[i-take]==inventoryDict[j]: chestka.remove(chestka[i-take]); take+=1
                
def vytvoreniWizarda():
    wizard=[]
    wizard.append(randint(1,5))
    return wizard

def enchant(wizard, staty, coJeNasazeno):
    co=input("Choose one of your items. ")
    if co=="skip": print("Wizard, seeing you can't decide, said that he will wait until you return with item to enchant.")
    elif co not in inventoryDict.keys(): print("That is not in your inventory."); enchant(wizard, staty, coJeNasazeno)
    elif co in coJeNasazeno: staty[inventoryDict[co].ability.lower()]+=int(wizard[0])
    if co in inventoryDict.keys(): inventoryDict[co].bonus+=int(wizard[0]); wizard.remove(int(wizard[0])); wizard.append(int(0)); print("After your item has been enchanted, you thank wise mage and continue in your journey.")
    else: pass

def showHelp():
    webbrowser.open(url)

def interakceSItememem(prikaz, inventoryDict, item):
    if prikaz.lower()=="take": sebrani(inventoryDict, item); print("You took the", item.name)
    elif prikaz.lower()=="help": showHelp(); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="explore": prohlidnout(item); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="inventory": zobrazeniInventare(inventoryDict, addons, coJeNasazeno); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="info": informace(inventoryDict); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="stats": zobrazeniStatu(staty); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="equip": pouzit(inventoryDict, staty, addons, coJeNasazeno); print("You used the", item.name); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="drop": odhozeni(inventoryDict, staty, addons, coJeNasazeno); print("You dropped the", item.name); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="unequip": sundat(inventoryDict, staty, addons, coJeNasazeno); print("You took down the", item.name); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)
    elif prikaz.lower()=="skip": pass
    else: print("Wrong command."); prikaz=input("What to do with the "+item.name+"? "); interakceSItememem(prikaz, inventoryDict, item)

def bezInterakce(prikaz, inventoryDict):
    if prikaz.lower()=="inventory": zobrazeniInventare(inventoryDict, addons, coJeNasazeno)
    elif prikaz.lower()=="help": showHelp()
    elif prikaz.lower()=="info": informace(inventoryDict)
    elif prikaz.lower()=="stats": zobrazeniStatu(staty)
    elif prikaz.lower()=="equip": pouzit(inventoryDict, staty, addons, coJeNasazeno)
    elif prikaz.lower()=="drop": odhozeni(inventoryDict, staty, addons, coJeNasazeno)
    elif prikaz.lower()=="unequip": sundat(inventoryDict, staty, addons, coJeNasazeno)
    elif prikaz.lower()=="skip": pass
    else: pass

def interakceSChestkou(prikaz, inventoryDict, chestka):
    if prikaz.lower()=="loot": prohlidnoutChestku(chestka)
    elif prikaz.lower()=="help": showHelp(); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="inventory": zobrazeniInventare(inventoryDict, addons, coJeNasazeno); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="info": informace(inventoryDict); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="stats": zobrazeniStatu(staty); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="equip": pouzit(inventoryDict, staty, addons, coJeNasazeno); print("You used the", item.name); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="drop": odhozeni(inventoryDict, staty, addons, coJeNasazeno); print("You dropped the", item.name); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="unequip": sundat(inventoryDict, staty, addons, coJeNasazeno); print("You took down the", item.name); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)
    elif prikaz.lower()=="skip": pass
    else: print("Wrong command."); prikaz=input("What to do with the chest? "); interakceSChestkou(prikaz, inventoryDict, chestka)

def interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno):
    if prikaz.lower()=="enchant": enchant(wizard, staty, coJeNasazeno)
    elif prikaz.lower()=="help": showHelp(); prikaz=input("What to do with the wizard? ");interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="inventory": zobrazeniInventare(inventoryDict, addons, coJeNasazeno); prikaz=input("What to do with the wizard? "); interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="info": informace(inventoryDict); prikaz=input("What to do with the wizard? "); interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="stats": zobrazeniStatu(staty); prikaz=input("What to do with the wizard? ");interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="equip": pouzit(inventoryDict, staty, addons, coJeNasazeno); print("You used the", item.name); prikaz=input("What to do with the wizard? "); interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="drop": odhozeni(inventoryDict, staty, addons, coJeNasazeno); print("You dropped the", item.name); prikaz=input("What to do with the wizard? "); interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="unequip": sundat(inventoryDict, staty, addons, coJeNasazeno); print("You took down the", item.name); prikaz=input("What to do with the wizard? "); interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
    elif prikaz.lower()=="skip": pass
    else: print("Wrong command."); prikaz=input("What to do with the wizard? "); interakceSWizem(prikaz, inventoryDict, staty, wizard, coJeNasazeno)
