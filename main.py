from random import uniform, choice, randint
from variables import ores, oreIndexes
from rich import print
from os.path import exists

ores = ores.ores
oreIndexes = oreIndexes.oreIndexes

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

    for ore in ores:
        if ores[ore]["chance"] >= chance:
            obtainableOres.append(ore)
        
    if obtainableOres == []:
        return print("[red]You got nothing :( [/red]")
    recieved_ore = choice(obtainableOres)
    userInventory[recieved_ore] = userInventory[recieved_ore] + 1
    print(f"""You got a {recieved_ore}""")


def sellOre():
    """
        Sell a certain amount of ores
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
        return print(f"""[red]You don't enough {userInput.lower()} to sell[/red]""")

    ore_to_sell = userInput.lower()

    print(f"[magenta]How many {ore_to_sell} would you like to sell?[/magenta]")
    userInput = input()

    try:
        userInput = int(userInput)
    except:
        return print(f"[red]{userInput} is not a valid number[/red]")

    if userInput > userInventory[ore_to_sell]:
        return print(f"[red]You don't have enough {ore_to_sell} to sell[/red]")

    userInventory[ore_to_sell] -= userInput
    userInventory["coins"] += userInput * ores[ore_to_sell]["price"]

    print(f"[green]You sold {userInput} {ore_to_sell}[/green]")

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
