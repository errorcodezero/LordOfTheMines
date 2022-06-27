from random import uniform, choice, randint
from variables import ores
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


def main_menu():
    print("[green]What would you like to do?[/green]")
    print("[green]1. Mine[/green]")
    print("[green]2. Sell[/green]")
    print("[green]3. Shop[/green]")
    print("[green]4. Inventory[/green]")
    print("[green]5. Exit[/green]")
    userInput = input()
    if userInput == "1":
        while True:
            return mine()
    elif userInput == "2":
        while True:
            return sell()
    elif userInput == "3":
        while True:
            return shop()
    elif userInput == "4":
        while True:
            return inventory()
    elif userInput == "5":
        print("[red]Goodbye![/red]")
        exit()
    else:
        print("[red]Invalid input[/red]")
        main_menu()


def mine():
    while True:
        """
            Picks an ore
            # TODO add more ores
        """
        chance = round(uniform(0, 1), 2)
        inputToType = randint(1, 100)
        print(f"Type the number {inputToType}(or type exit to exit)")
        userInput = input()
        if userInput == str(inputToType):
            for ore in ores:
                if ores[ore]["chance"] >= chance:
                    obtainableOres.append(ore)

            if obtainableOres == []:
                print("[red]You got nothing :( [/red]")
            recieved_ore = choice(obtainableOres)
            userInventory[recieved_ore] = userInventory[recieved_ore] + 1
            print(f"""You got a {recieved_ore}""")
        elif userInput == "exit":
            return main_menu()
        else:
            print(f"You were supposed to type {inputToType}")


def sell():
    """
        Sell a certain amount of ores
    """
    while True:
        print("[magenta]What ore would you like to sell?[/magenta]")
        print("[green]Inventory:[/green]")
        for ore in userInventory:
            print(f"""{ore}: {userInventory[ore]}""")
            if userInventory[ore] < 0:
                userInventory[ore] = 0

        print("\n")

        userInput = input()

        if(userInput == "exit"):
            return main_menu()

        if userInput.lower() not in userInventory.keys():
            return print(f"[red]{userInput} is not a valid ore[/red]")

        if userInventory[userInput.lower()] == 0:
            return print(f"""[red]You don't enough {userInput.lower()} to sell[/red]""")

        ore_to_sell = userInput.lower()

        print(
            f"[magenta]How many {ore_to_sell} would you like to sell?[/magenta]")
        userInput = input()

        if(userInput == "exit"):
            return main_menu()

        try:
            userInput = int(userInput)
        except:
            return print(f"[red]{userInput} is not a valid number[/red]")

        if userInput > userInventory[ore_to_sell]:
            return print(f"[red]You don't have enough {ore_to_sell} to sell[/red]")
        elif userInput < 0:
            return print(f"[red]You can't sell negative amounts of ore[/red]")
        elif userInput.lower() == "coins":
            return print(f"[red]You can't sell coins[/red]")

        userInventory[ore_to_sell] -= userInput
        userInventory["coins"] += userInput * ores[ore_to_sell]["price"]

        print(f"[green]You sold {userInput} {ore_to_sell}[/green]")

        for ore in userInventory:
            if userInput == ore.lower():
                userInventory[ore] = userInventory[ore] - 1
                userInventory["coins"] = userInventory["coins"] + 1
                print(f"[orange] You sold {1} {ore}! [orange]")


def shop():
    pass


def inventory():
    pass


while True:
    main_menu()
