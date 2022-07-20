from flask import Flask
from database import Database
from variables.ores import ores
from variables.shop import shopItems
from random import randint, choice, uniform
app = Flask(__name__)

db = Database("database.json")

def auth(username: str, password: str):
    print(db.get(f"{username}_password"))
    try:
        if password == db.get(f"{username}_password"):
            return True
        else:
            print("error")
            return False
    except:
        print(db.get(f"{username}_password"))
        return False


def getUserInv(username: str):
    return db.get(f"{username}_inv")


def getUserDiscord(username):
    try:
        return db.get(f"{username}_discord")
    except:
        return False


def setUserInv(username: str, value: str, amount: int):
    try:
        changedInv = db.get(f"{username}_inv")
        changedInv[value] = amount
        db.set(f"{username}_inv", changedInv)
    except:
        return False

def saveDB():
    db.dumpdb()
    
@app.route("/", methods=["GET"])
def main():
    return {
        "status": 200
    }


@app.route('/signup/<username>/<password>', methods=["GET"])
def login(username, password):
    if getUserInv(username) == False:
        db.set(f"{username}_inv", {})
        db.set(f"{username}_discord", "")
        db.set(f"{username}_password", password)
        saveDB()
        return {"message": "New user created"}
    else:
        return {"message": "User already exists"}


@app.route('/sell/<username>/<password>/<item>/<amount>', methods=["GET"])
def sell(username, password, item, amount: int):
    if auth(username, password) == False:
        return "Authentication Failed"
    else:
        try:
            if getUserInv(username)[item] >= int(amount) and int(amount) > 0:
                setUserInv(username, item, getUserInv(username)[item] - int(amount))
                setUserInv(username, "coins", getUserInv(username)["coins"] + int(amount) * shopItems[item]["price"])
                return {"sold": True}
            else:
                return {"sold": False}
        except:
            return {"sold": False}


@app.route('/shop/<username>/<password>', methods=["GET"])
def shop(username, password):
    if auth(username, password) == False:
        return "Authentication Failed"
    return {"items": shopItems, "ores": ores}


@app.route('/buy/<username>/<password>/<item>/<amount>', methods=["GET"])
def buy(username, password, item, amount):
    if auth(username, password) == False:
        return "Authentication Failed"
    for thing in shopItems:
        if thing.lower() == item.lower():
            if shopItems[item]["price"] < getUserInv(username)["coins"] * amount:
                return {
                    "got_item": False,
                }
            setUserInv(username, item, getUserInv(username)[item] + amount)
            saveDB()
            return {
                "got_item": True
            }


@app.route('/craft/<username>/<password>/<item>/<amount>', methods=["GET"])
def craft(username, password, item, amount):
    if auth(username, password) == False:
        return "Authentication Failed"
    for thing in shopItems:
        try:
            if thing.lower() == item.lower():
                for ingredient in shopItems[item]["recipe"]:
                    if ingredient.lower() in getUserInv(username) and getUserInv(username)[ingredient] < shopItems[item]["recipe"][ingredient]:
                        setUserInv(username, ingredient, getUserInv(username)[
                            ingredient] - shopItems[item]["recipe"][ingredient])
                        saveDB()
                        return {
                            "crafted": True
                        }
        except:
            return {
                "crafted": False
            }


@app.route('/mine/<username>/<password>', methods=["GET"])
def mine(username: str, password: str):
    if auth(username, password) == False:
        return {"message": "Authentication Failed"}
    else:
        chance = round(uniform(0, 1), 2)
        obtainable_ores = []
        recieved_ore = []

        for ore in ores:
            if ores[ore]["chance"] >= chance:
                obtainable_ores.append(ore)
        try:
            recieved_ore = choice(obtainable_ores)
        except:
            return {"item": None, "amount": 0}
        for item in getUserInv(username):
            try:
                if shopItems[item]["item_type"] == "totem":
                    if randint(1, shopItems[item]["totem_chance"]) == 1:
                        setUserInv(username, item, getUserInv(username)[
                            item] + shopItems[item]["totem_multiply"])
                        setUserInv(username, recieved_ore, getUserInv(username)+ shopItems[item]["totem_multiply"])
                        saveDB()
                        return {"item": recieved_ore, "amount": shopItems[item]["totem_multiply"]}
                    else:
                        continue
            except:
                continue
        try:
            setUserInv(username, recieved_ore, getUserInv(
                username)[recieved_ore] + 1)
        except:
            setUserInv(username, recieved_ore, 1)
        return {"item": recieved_ore, "amount": 1}


@app.route("/info/<username>/<password>/<item>", methods=["GET"])
def info(username, password, item):
    if auth(username, password) == False:
        return {"message": "Authentication Successful"}
    try:
        for thing in shopItems:
            if item.lower() == thing.lower():
                return {
                    "name": shopItems[thing]["name"],
                    "price": shopItems[thing]["price"],
                    "description": shopItems[thing]["description"],
                }
            else:
                continue
        for ore in ores:
            if item.lower() == ore.lower():
                return {
                    "name": ore,
                    "price": ores[ore]["price"],
                }
            else:
                continue
        return {
            "name": "Invalid item"
        }
    except:
        return {
            "message": "We encountered an error"
        }


@app.route("/sync/<username>/<password>/", methods=["GET"])
def sync(username, password):
    if auth(username, password) == False:
        return {"message": "Authentication Failed"}
    userInventory = db.get(f"{username}_inv")
    return {"user_inventory": userInventory}

if __name__ == '__main__':
    app.run()