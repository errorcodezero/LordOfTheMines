from random import uniform, choice, randint
from variables import ores
from rich import print
from art import *
from rich.console import Console
from rich.table import Table

ores = ores.ores

console = Console()

console.clear()

obtainableOres = []

userInventory = {
    "stone": 0,
    "coal": 0,
    "copper": 0,
    "amethyst": 0,
    "iron": 0,
    "silver": 0,
    "gold": 0,
    "diamond": 0,
    "platinum": 0,
    "coins": 0
}


def main_menu():
    splash_screen = text2art("LordOfTheMines")

    print(splash_screen)

    print("[green]What would you like to do?[/green]")
    print("[green]1. Mine[/green]")
    print("[green]2. Sell[/green]")
    print("[green]3. Shop[/green]")
    print("[green]4. Inventory[/green]")
    print("[green]5. Exit[/green]")
    userInput = input()
    console = Console()
    if userInput == "1":
        while True:
            console.clear()
            return mine()
    elif userInput == "2":
        while True:
            console.clear()
            return sell()
    elif userInput == "3":
        while True:
            console.clear()
            return shop()
    elif userInput == "4":
        while True:
            console.clear()
            return inventory()
    elif userInput == "5":
        print("[red]Goodbye![/red]")
        quit(1)
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
        recieved_ore = []
        if userInput == str(inputToType):
            for ore in ores:
                if ores[ore]["chance"] >= chance:
                    obtainableOres.append(ore)
            try:
                recieved_ore = choice(obtainableOres)
            except:
                print("[red]You didn't recieve any ore[/red]")
                return mine()
            userInventory[recieved_ore] += 1
            print(f"""You got a {recieved_ore}""")
            console = Console()
        elif userInput == "exit":
            console = Console()
            console.clear()
            return main_menu()
        else:
            print(f"You were supposed to type {inputToType}")


def sell():
    """
        Sell a certain amount of ores
    """
    while True:
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")
        table.add_column("Amount", justify="right", style="magenta")

        for ore in ores:
            if ore == "coin":
                break
            table.add_row(
                f"""{ore}""", f"""{ores[ore]["price"]}""", f"""{userInventory[ore]}""")
            if userInventory[ore] < 0:
                userInventory[ore] = 0

        console = Console()
        console.print(table)

        print(f"""Coins: {userInventory["coins"]}""")

        print("[magenta]What ore would you like to sell?[/magenta](type exit to exit)")

        userInput = input()

        console = Console()

        if(userInput == "exit"):
            console.clear()
            return main_menu()

        if userInput.lower() not in userInventory.keys():
            return print(f"[red]{userInput} is not a valid ore[/red]")

        if userInventory[userInput.lower()] == 0:
            return print(f"""[red]You don't enough {userInput.lower()} to sell[/red]""")

        elif userInput.lower() == "coins":
            return print(f"[red]You can't sell coins[/red]")

        ore_to_sell = userInput

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

        userInventory[ore_to_sell] -= userInput
        userInventory["coins"] += userInput * ores[ore_to_sell]["price"]

        print(f"[green]You sold {userInput} {ore_to_sell}[/green]")

        for ore in userInventory:
            if userInput == ore.lower():
                userInventory[ore] = userInventory[ore] - 1
                userInventory["coins"] = userInventory["coins"] + 1
                print(f"[orange] You sold {1} {ore}! [orange]")


def inventory():
    while True:
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")
        table.add_column("Amount", justify="right", style="magenta")

        for ore in ores:
            if ore == "coin":
                break
            table.add_row(f"""{ore}""", f"""{ores[ore]["price"]}""", f"""{userInventory[ore]}""")
            if userInventory[ore] < 0:
                userInventory[ore] = 0
        console = Console()
        console.log(table)
        print(f"""Coins: {userInventory["coins"]}""")
        print("Press enter to exit")
        input()
        return main_menu()


def shop():
    print("This command is not added yet")
    print("Press enter to continue")
    input()
    return main_menu()


try:
    while True:
        main_menu()
except:
    print("[red]Goodbye![/red]")
    print(exit)
    exit()
