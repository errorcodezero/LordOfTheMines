# Imports
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

# Clears the screen
console = Console()
console.clear()

# Ores that are obtained are picked from this list
obtainableOres = []

# Json based database
db = Database("database.json")
try:
    userInventory = db.printdb()
except:
    userInventory = {}

# Function to get random splash text


def get_random_line(file_name):
    line = choice(open(file_name).readlines())
    return line

# Main menu


def main_menu():
    # Splash Screen
    splash_screen = text2art("LordOfTheMines")

    # Colored Splash Screen
    rgb_splash_screen = Colorate.Diagonal(Colors.blue_to_red, splash_screen)

    print(rgb_splash_screen)

    # Random splash text
    splash_text = get_random_line("variables/splash.txt")
    rprint(f"[white]{splash_text}[/white]")

    # Asks questions to the user
    rprint("[blue]What would you like to do?[/blue]")
    rprint("[green]1. Mine[/green]")
    rprint("[green]2. Sell[/green]")
    rprint("[green]3. Shop[/green]")
    rprint("[green]4. Inventory[/green]")
    rprint("[green]5. Info[/green]")
    rprint("[green]6. Craft[/green]")
    userInput = input()
    console = Console()
    # Mine
    if userInput == "1" or userInput.lower() == "mine":
        while True:
            console.clear()
            return mine()
    # Sell
    elif userInput == "2" or userInput.lower() == "sell":
        while True:
            console.clear()
            return sell()
    # Shop
    elif userInput == "3" or userInput.lower() == "shop":
        while True:
            console.clear()
            return shop()
    # Inventory
    elif userInput == "4" or userInput.lower() == "inventory":
        while True:
            console.clear()
            return inventory()
    # Info
    elif userInput == "5" or userInput.lower == "info":
        while True:
            console.clear()
            return info()
    # Craft
    elif userInput == "6" or userInput.lower() == "craft":
        while True:
            console.clear()
            return craft()
    # Invalid input
    else:
        rprint("[red]Invalid input[/red]")
        main_menu()


def mine():
    while True:
        """
            Picks an ore
            # TODO add more ores
        """
        # Random number
        chance = round(uniform(0, 1), 2)

        # Asks user to type random number(To prove they are not afk)
        inputToType = randint(1, 100)
        rprint(f"Type the number {inputToType}(or type exit to exit)")
        userInput = input()
        recieved_ore = []
        # Checks if what they typed is the random number
        if userInput == str(inputToType):
            # Puts all obtainable ores into a list
            for ore in ores:
                if ores[ore]["chance"] >= chance:
                    obtainableOres.append(ore)
            try:
                # Picks an ore from the list
                recieved_ore = choice(obtainableOres)
            except:
                # When list is empty
                rprint("[red]You didn't recieve any ore[/red]")
                return mine()
            # Gives ore to user
            try:
                userInventory[recieved_ore] += 1
            except:
                userInventory[recieved_ore] = 1

            if ores[recieved_ore]["type"] == "legendary":
                text = Colorate.Diagonal(
                    Colors.rainbow, f"""You got a {recieved_ore}!!!""")
                print(text)
                return mine()
            # elif "lucky totem" in userInventory and randint(1, 4) == 1:
            #     rprint(
            #         f"[yellow]Your lucky totem made you lucky and you got 2 {recieved_ore}[/yellow]")
            #     try:
            #         userInventory[recieved_ore] += 1
            #     except:
            #         userInventory[recieved_ore] = 2
            for item in userInventory:
                try:
                    if shopItems[item]["item_type"] == "totem":
                        if randint(1, shopItems[item]["totem_chance"]) == 1:
                            rprint(
                                f"""[yellow]Your [bold]{item}[/bold] made you lucky and you got {shopItems[item]["totem_multiply"]} {recieved_ore}s[/yellow]""")
                            try:
                                userInventory[recieved_ore] += userInventory[item]["totem_multiply"] + 1
                                return mine()
                            except:
                                userInventory[recieved_ore] = userInventory[item]["totem_multiply"] + 1
                                return mine()
                except:
                    continue
            print(f"You got a {recieved_ore}")
        # Exit
        elif userInput == "exit":
            console.clear()
            return main_menu()
        # If user doesn't type specified number
        else:
            rprint(f"You were supposed to type {inputToType}")

# Sell


def sell():
    """
        Sell a certain amount of ores
    """
    while True:
        # Inventory table
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")
        table.add_column("Amount", justify="right", style="magenta")

        # Adds all the elements to inventory table
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
        # Prints the table
        console.print(table)

        # Coins
        try:
            rprint(f"""Coins: {userInventory["coins"]}""")
        except:
            userInventory["coins"] = 0
            rprint(f"""Coins: 0""")

        # Asks what to sell
        rprint("[magenta]What ore would you like to sell?[/magenta](type exit to exit and type sellall to sell everything)")

        # Gets user input
        userInput = input()

        # If user wants to exit
        if userInput == "exit":
            console.clear()
            return main_menu()

        # If user wants to sell everything
        elif userInput == "sellall":
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
            rprint(f"""Coins: {userInventory["coins"]}""")
            rprint("Press enter to continue")

            input()
            return main_menu()

        # If ore is invalid
        elif userInput.lower() not in userInventory.keys():
            rprint(f"[red]{userInput} is not a valid ore[/red]")
            return sell()

        # If they don't have enough of an ore to sell
        elif userInventory[userInput.lower()] == 0:
            return rprint(f"""[red]You don't enough {userInput.lower()} to sell[/red]""")

        # If they try to sell coins
        elif userInput.lower() == "coins":
            return rprint(f"[red]You can't sell coins[/red]")

        try:
            if shopItems[userInput]["sellable"] == False:
                rprint("[red]You can't sell that[/red]")
                return sell()
        except:
            rprint("[red]You can't sell that[/red]")
            return sell()

        ore_to_sell = userInput

        # How much does user want to sell
        rprint(
            f"[magenta]How many {ore_to_sell} would you like to sell(type exit to exit)?[/magenta]")
        userInput = input()

        # Again they can type exit
        if(userInput == "exit"):
            return main_menu()

        try:
            userInput = int(userInput)
        except:
            return rprint(f"[red]{userInput} is not a valid number[/red]")

        # If they don't have enough of an ore to sell
        if userInput > userInventory[ore_to_sell]:
            return rprint(f"[red]You don't have enough {ore_to_sell} to sell[/red]")

        # To prevent them from selling negative amounts
        elif userInput < 0:
            return rprint(f"[red]You can't sell negative amounts of ore[/red]")

        # Actually selling the ore
        userInventory[ore_to_sell] -= userInput
        userInventory["coins"] += userInput * ores[ore_to_sell]["price"]

        rprint(f"[green]You sold {userInput} {ore_to_sell}[/green]")

        for ore in userInventory:
            if userInput == ore.lower():
                userInventory[ore] -= 1
                userInventory["coins"] += 1
                rprint(f"[orange] You sold {1} {ore}! [orange]")

# Inventory


def inventory():
    while True:
        # Inventory table
        table = Table(title="Inventory")

        table.add_column("Ore", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")
        table.add_column("Amount", justify="right", style="magenta")

        # Adds all the elements to inventory table
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

        # Prints the table
        console.print(table)

        # Coins
        try:
            rprint(f"""Coins: {userInventory["coins"]}""")
        except:
            userInventory["coins"] = 0
            rprint(f"""Coins: 0""")
        rprint("Press enter to continue")
        input()
        return main_menu()


def shop():
    """
        Shop
        # TODO
    """
    # Shop table
    table = Table(title="Shop")

    table.add_column("Item", justify="right", style="green", no_wrap=True)
    table.add_column("Price", justify="right", style="blue")

    # Adds all the elements to shop table
    for item in shopItems:
        try:
            table.add_row(
                f"""{item.title()}""", f"""{shopItems[item]["price"]}""")
        except:
            table.add_row(f"""{item}""", f"""Priceless""")

    console.log(table)

    # Coins
    try:
        rprint(f"Coins: {userInventory['coins']}")
    except:
        userInventory["coins"] = 0
        rprint(f"Coins: 0")

    # Asks what to buy
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
    # Exit
    if userInput.lower() == "exit":
        return main_menu()

# Info


def info():
    while True:
        # Asks user what they would like to see info about
        rprint(
            "[green]What item would you like to see more about(type exit to exit)?([/green]")

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

# Craft


def craft():
    """
        Lets you craft craftable items
    """
    while True:
        # Shop table
        table = Table(title="All Craftable Items")

        table.add_column("Item", justify="right", style="green", no_wrap=True)
        table.add_column("Price", justify="right", style="blue")

        # Adds all the elements to shop table
        for item in shopItems:
            if shopItems[item]["craftable"] == False:
                continue
            try:
                table.add_row(
                    f"""{item.title()}""", f"""{shopItems[item]["price"]}""")
            except:
                table.add_row(f"""{item}""", f"""Priceless""")

        console.log(table)

        print("What would you like to craft(type exit to exit)?")
        userInput = input()
        if userInput.lower() == "exit":
            return main_menu()
        for item in shopItems:
            if userInput.lower() == item.lower():
                for ores in shopItems[item]["recipe"]:
                    try:
                        if userInventory[ores] < shopItems[item]["recipe"][ores]:
                            rprint(
                                f"[red]You don't have enough {ores} to craft {item}[/red]")
                            return craft()
                    except:
                        rprint(
                            f"[red]You don't have enough {ores} to craft {item}[/red]")
                        return craft()
                for ores in shopItems[item]["recipe"]:
                    userInventory[ores] -= shopItems[item]["recipe"][ores]
                try:
                    for contents in shopItems[item]["contents"]:
                        userInventory[contents] += shopItems[item]["contents"][contents]
                except:
                    for contents in shopItems[item]["contents"]:
                        userInventory[contents] = shopItems[item]["contents"][contents]
                rprint(f"[green]You crafted a {item}![/green]")
                return craft()
            else:
                continue
        rprint(f"[red]{userInput} is not a valid item[/red]")


# Error handling
if __name__ == "__main__":
    try:
        while True:
            main_menu()

    except:
        load_animation("Saving your data", 10)
        db.setdb(userInventory)
        sys.exit()


# while True:
#     main_menu()
