from random import uniform, choice, randint
from variables import ores

chance = round(uniform(0, 1), 2)

ores = ores.ores

obtainableOres = []

print("Welcome to mining simulator ⛏")

def pickOre():
    """
        Picks an ore
        # TODO add more ores
    """
    recieved_ore = choice(obtainableOres)
    print(f"""You got a {recieved_ore["name"]}""")

def sellOre():
    """
        Sell a certain amount of ores
        # TODO 
    """
    pass

def buyItems():
    pass

def showShop():
    pass

while True:
    inputToType = randint(1, 100)
    print(f"Type the number {inputToType}")
    userInput = input()
    if(userInput == str(inputToType)):
        for ore in ores:
            if ore["chance"] >= chance:
                obtainableOres.append(ore)

        pickOre()
    else:
        print(f"You were supposed to type {inputToType}")