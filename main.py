from random import uniform, choice, randint
from variables import ores
import json
import rich
from rich import print
from os.path import exists

ores = ores.ores

obtainableOres = []

userInventory = {
    "stone": 0,
    "copper": 0,
    "coins": 0
}

print("Welcome to mining simulator ⛏")


def pickOre():
    """
        Picks an ore
        # TODO add more ores
    """
    i = 0
    for ore in ores:
        if ore["chance"] >= chance:
            obtainableOres.append(ore)
        
    if obtainableOres == []:
        return print("[red]You got nothing :( [/red]")
    recieved_ore = choice(obtainableOres)
    userInventory[recieved_ore["name"]] = userInventory[recieved_ore["name"]] + 1
    print(f"""You got a {recieved_ore["name"]}""")


def sellOre():
    """
        Sell a certain amount of ores
        # TODO make it so it sells more than 1 ore
    """
    print("[magenta]What ore would you like to sell?[/magenta]")
    print("[green]Inventory:[/green]")
    for ore in userInventory:
        print(f"""{ore}: {userInventory[ore]}""")
        if userInventory[ore] < 0:
            userInventory[ore] = 0

    print("\n")

    userInput = input()

    if userInput.lower() not in userInventory.keys():
        return print(f"[red]{userInput} is not a valid ore[/red]")

    if userInventory[userInput.lower()] == 0:
        return print(f"""[red]You don't enough {ore[userinput]}[/red]""")

    for ore in userInventory:
        if userInput == ore.lower():
            userInventory[ore] = userInventory[ore] - 1
            userInventory["coins"] = userInventory["coins"] + 1
            print(f"[orange] You sold {1} {ore}! [orange]")


def buyItems():
    pass


def showShop():
    pass


while True:
    chance = round(uniform(0, 1), 2)
    inputToType = randint(1, 100)
    print(f"Type the number {inputToType}(or type exit to exit)")
    userInput = input()
    if userInput == str(inputToType):
        pickOre()
    elif userInput == "exit":
        sellOre()
    else:
        print(f"You were supposed to type {inputToType}")
