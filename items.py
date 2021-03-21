def hasNumber(string):
    for character in string:
        if character.isdigit():
            return True
        else:
            pass
    return False

def isNumber(integer):
    try:
        integer = int(integer)
        return True
    except ValueError:
        return False

abilities = ["DMG", "SPEED", "HP", "ARMOR"]
types = ["ONETIME", "POTION", "ARMOR", "WEAPON", "ADD ON"]

class item:     
    def fAbility(self):
        print(abilities)
        self.ability = input("Jaká je schopnost předmětu? > ")
        if self.ability.upper() not in abilities:
            print("ERROR - Schopnost není v nabídce. Prosím zkuste to znovu.")
            self.fAbility()
        else:
            self.bonus = input("Kolik dává schopnost bonus? (+) > ")
            while not isNumber(self.bonus):
                print("ERROR - Bonus musí býz celé číslo. Prosím zkuste to znovu.")
                self.bonus = input("Kolik dává schopnost bonus? (+) > ")

    def createItem(self):
        self.name = input("Jméno předmětu > ")
        while hasNumber(self.name):
            print("ERROR - Jméno předmětu nesmí obsahovat číslo. Prosím zkuste to znovu.")
            self.name = str(input("Jméno předmětu > "))

        print(types)
        self.itemType = input("Typ předmětu > ")
        while self.itemType.upper() not in types:
            print("ERROR - Typ předmětu není v nabídce. Prosím zkuste to znovu.")
            print(types)
            self.itemType = input("Typ předmětu > ") 

        self.level = input("Úroveň předmětu > ")
        while not isNumber(self.level):
            print("ERROR - Úroveň předmětu musí být reprezentována celým číslem. Prosím zkuste to znovu.")
            self.level = input("Úroveň předmětu > ")

        self.fAbility()

    def saveItem(self):
        itemsFile = open("items.txt", "a+")
        itemsFile.write("${};\ntype:{};\nlevel:{};\nability:{} +{}\n".format(self.name, self.itemType.upper(), self.level, self.ability.upper(), self.bonus))
        itemsFile.close()
        
class pickItem:
    def findItem(self, name):
        file = open("items.txt", "r")
        allItems = file.read()
        sortedItems = allItems.split("$")
        for i in sortedItems:
            if i.split(";")[0] == name:
                self.name = name
                self.type = i.split(";")[1].split(":")[1]
                self.lvl = int(i.split(";")[2].split(":")[1])
                rawAbility = i.split(";")[3].split(":")[1]
                self.ability = rawAbility.split(" ")[0]
                self.bonus = int(rawAbility.split(" ")[1])
                file.close()
                return True
        else:
            file.close()
            return False
    
if __name__ == "__main__":
    addItem = item()
    addItem.createItem()
    addItem.saveItem()
            
