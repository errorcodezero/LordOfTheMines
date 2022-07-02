from random import uniform, choice, randint
from variables.ores import ores
from variables.shop import shopItems
from rich import print as rprint
from art import *
from rich.console import Console
from rich.table import Table
from pystyle import Colorate, Colors
from database import Database
import sys
from animations.load_animation import load_animation

console = Console()
console.clear()

obtainableOres = []
db = Database("database.json")
try:
    userInventory = db.printdb()
except:
    userInventory = {}


def get_random_line(file_name):
    line = choice(open(file_name).readlines())
    return line


def main_menu():
    splash_screen = text2art("LordOfTheMines")
    rgb_splash_screen = Colorate.Diagonal(Colors.blue_to_red, splash_screen)

    print(rgb_splash_screen)
    splash_text = get_random_line("variables/splash.txt")
    rprint(f"[white]{splash_text}[/white]")

    rprint("[blue]What would you like to do?[/blue]")
    rprint("[green]1. Mine[/green]")
    rprint("[green]2. Sell[/green]")
    rprint("[green]3. Shop[/green]")
    rprint("[green]4. Inventory[/green]")
    rprint("[green]5. Info[/green]")
    userInput = input()
    console = Console()
    if userInput == "1" or userInput.lower() == "mine":
        while True:
            console.clear()
            return mine()
    elif userInput == "2" or userInput.lower() == "sell":
        while True:
            console.clear()
            return sell()
    elif userInput == "3" or userInput.lower() == "shop":
        while True:
            console.clear()
            return shop()
    elif userInput == "4" or userInput.lower() == "inventory":
        while True:
            console.clear()
            return inventory()
    elif userInput == "5" or userInput.lower == "info":
        while True:
            console.clear()
            return info()
    else:
        rprint("[red]Invalid input[/red]")
        main_menu()


def mine():
    while True:
        """
            Picks an ore
            # TODO add more ores
        """
        chance = round(uniform(0, 1), 2)
        inputToType = randint(1, 100)
        rprint(f"Type the number {inputToType}(or type exit to exit)")
        userInput = input()
        recieved_ore = []
        if userInput == str(inputToType):
            for ore in ores:
                if ores[ore]["chance"] >= chance:
                    obtainableOres.append(ore)
            try:
                recieved_ore = choice(obtainableOres)
            except:
                rprint("[red]You didn't recieve any ore[/red]")
                return mine()
            try:
                userInventory[recieved_ore] += 1
            except:
                userInventory[recieved_ore] = 1
            print(f"""You got a {recieved_ore}""")
            console = Console()
        elif userInput == "exit":
            console = Console()
            console.clear()
            return main_menu()
        else:
            rprint(f"You were supposed to type {inputToType}")


def sell():
    """
        Sell a certain amount of ores
    """
    while True:
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")
        table.add_column("Amount", justify="right", style="magenta")

        for ore in userInventory:
            if ore == "coins":
                continue
            elif userInventory[ore] <= 0:
                userInventory[ore] = 0
                continue
            else:
                try:
                    table.add_row(
                        f"""{ore}""", f"""{ores[ore]["price"]}""", f"""{userInventory[ore]}""")
                except:
                    table.add_row(
                        f"""{ore}""", f"""{shopItems[ore]["price"]}""", f"""{userInventory[ore]}""")

        console = Console()
        console.print(table)

        try:
            rprint(f"""Coins: {userInventory["coins"]}""")
        except:
            userInventory["coins"] = 0
            rprint(f"""Coins: 0""")

        rprint("[magenta]What ore would you like to sell?[/magenta](type exit to exit and type sellall to sell everything)")

        userInput = input()

        console = Console()

        if userInput == "exit":
            console.clear()
            return main_menu()

        if userInput == "sellall":
            console.clear()
            for ore in userInventory:
                if ore == "coins":
                    continue
                elif ore in shopItems:
                    continue
                else:
                    userInventory["coins"] += ores[ore]["price"] * \
                        userInventory[ore]
                    userInventory[ore] = 0
            rprint("[green]You sold all your ore[/green]")
            rprint("Press enter to continue")

            input()
            return main_menu()

        if userInput.lower() not in userInventory.keys():
            return rprint(f"[red]{userInput} is not a valid ore[/red]")

        if userInventory[userInput.lower()] == 0:
            return rprint(f"""[red]You don't enough {userInput.lower()} to sell[/red]""")

        elif userInput.lower() == "coins":
            return rprint(f"[red]You can't sell coins[/red]")

        ore_to_sell = userInput

        rprint(
            f"[magenta]How many {ore_to_sell} would you like to sell(type exit to exit)?[/magenta]")
        userInput = input()

        if(userInput == "exit"):
            return main_menu()

        try:
            userInput = int(userInput)
        except:
            return rprint(f"[red]{userInput} is not a valid number[/red]")

        if userInput > userInventory[ore_to_sell]:
            return rprint(f"[red]You don't have enough {ore_to_sell} to sell[/red]")
        elif userInput < 0:
            return rprint(f"[red]You can't sell negative amounts of ore[/red]")

        userInventory[ore_to_sell] -= userInput
        userInventory["coins"] += userInput * ores[ore_to_sell]["price"]

        rprint(f"[green]You sold {userInput} {ore_to_sell}[/green]")

        for ore in userInventory:
            if userInput == ore.lower():
                userInventory[ore] = userInventory[ore] - 1
                userInventory["coins"] = userInventory["coins"] + 1
                rprint(f"[orange] You sold {1} {ore}! [orange]")


def inventory():
    while True:
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")
        table.add_column("Amount", justify="right", style="magenta")

        for ore in userInventory:
            if ore == "coins":
                continue
            elif userInventory[ore] <= 0:
                userInventory[ore] = 0
                continue
            else:
                try:
                    table.add_row(
                        f"""{ore}""", f"""{ores[ore]["price"]}""", f"""{userInventory[ore]}""")
                except:
                    table.add_row(
                        f"""{ore}""", f"""{shopItems[ore]["price"]}""", f"""{userInventory[ore]}""")

        console = Console()
        console.print(table)
        try:
            rprint(f"""Coins: {userInventory["coins"]}""")
        except:
            userInventory["coins"] = 0
            rprint(f"""Coins: 0""")
        rprint("Press enter to continue")
        input()
        return main_menu()


def shop():
    table = Table(title="Shop")

    table.add_column("Item", justify="right", style="green", no_wrap=True)
    table.add_column("Price", justify="right", style="blue")

    for item in shopItems:
        try:
            table.add_row(
                f"""{item.title()}""", f"""{shopItems[item]["price"]}""")
        except:
            table.add_row(f"""{item}""", f"""Priceless""")

    console.log(table)
    try:
        rprint(f"Coins: {userInventory['coins']}")
    except:
        userInventory["coins"] = 0
        rprint(f"Coins: 0")
    print("What would you like to buy(type exit to exit)")
    userInput = input()
    for item in shopItems:
        if userInput.lower() == item.lower():
            if userInventory["coins"] >= shopItems[item]["price"]:
                userInventory["coins"] -= shopItems[item]["price"]
                try:
                    for contents in shopItems[item]["contents"]:
                        userInventory[contents] += shopItems[item]["contents"][item]
                except:
                    for contents in shopItems[item]["contents"]:
                        userInventory[contents] = shopItems[item]["contents"][contents]
                rprint(f"[green]You bought {item}![/green]")
            else:
                rprint(f"[red]You don't have enough coins to buy {item}[/red]")
            return shop()
    if userInput.lower() == "exit":
        return main_menu()


def info():
    while True:
        rprint("[green]What item would you like to see more about(type exit to exit)?([/green]")

        userInput = input()
        if userInput.lower() == "exit":
            return main_menu()
        try:
            for item in shopItems:
                if userInput.lower() == item.lower():
                    rprint(f"""Name: [green bold]{item}[/green bold]""")
                    rprint(
                        f"""Description: [green]{shopItems[item]["description"]}[/green]""")
                    rprint("Contents:")
                    for contents in shopItems[item]["contents"]:
                        if len(contents):
                            break
                        rprint(f"""- [green]{contents}[/green]""")
                    rprint("[blue]Press enter to exit")
                    input()
                    return main_menu()

            for ore in ores:
                if userInput.lower() == ore.lower():
                    rprint(f"""Name: [green bold]{ore}[/green bold]""")
                    rprint(f"""Price: [green]{ores[ore]["price"]}[/green]""")
                    rprint("[blue]Press enter to exit")
                    input()
                    return main_menu()
                else: 
                    rprint(f"[red]{userInput} is not a valid item[/red]")
                    return info()
        except:
            rprint(f"[red]{userInput} is not a valid item[/red]")
            return info()


if __name__ == "__main__":
    try:
        while True:
            main_menu()

    except:
        load_animation("Saving your data", 10)
        db.setdb(userInventory)
        sys.exit()
