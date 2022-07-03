MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

# resources = dict(water=300, milk=200, coffee=100, money=0)
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0,
}

coins = dict(quarter=0.25, dime=0.1, nickel=0.05, penny=0.01)


def check_resources(request, current):
    """The function is to check the current resource, no global changes"""
    returnCode = True  # default is enough resources
    for item in request:
        if request[item] > current[item]:
            print(f"Sorry there is not enough {item}.")
            returnCode = False
    return returnCode


def request_money(cost):
    """The function is to request money, no global changes"""

    sumCollected = 0
    for theCoin in coins:
        sumCollected += coins[theCoin] * \
                        int(input(f"Please choose the number of {theCoin} "
                                  f"you prefer to offer: "))
    if sumCollected < cost:
        print("Sorry that's not enough money. Money refunded.")
        return False
    elif sumCollected > cost:
        theChange = round(sumCollected - cost, 2)
        print(f"Here is $ {theChange} in change.")
    return True


def consume_resources(request, current):
    for item in request:
        current[item] -= request[item]
    return current


def make_coffee(coffee_type, inResources):
    """The function to make coffee according to requested type"""

    for theType in MENU:
        if theType == coffee_type:
            validFlag = check_resources(MENU[theType]["ingredients"],
                                        inResources)
            if validFlag:
                print(f"The cost of {theType} is $ {MENU[theType]['cost']}")
                payFlag = request_money(MENU[theType]["cost"])
                if payFlag:
                    outResources = consume_resources(MENU[theType]["ingredients"],
                                                     inResources)
                    outResources["money"] += MENU[theType]["cost"]
                    print(f"Here is your {theType}. Enjoy!\n")
                    return outResources  # Success
                else:
                    return -3  # No enough money
            else:
                return -2  # No enough resources

    print(f"The Coffee type you requested ({coffee_type}) "
          f"is not in our menu, sorry!")
    return -1  # the code -1 indicate not run


def start_coffee_machine(nowResources):
    """The function to run the coffee machine"""

    units = ["ml", "ml", "g", "$"]
    command = input("What would you like? (espresso/latte/cappuccino):") \
        .lower()
    if command == "report":
        resCount = 0
        for theResource in nowResources:
            print(f"{theResource.title()}: {nowResources[theResource]} "
                  f"{units[resCount]}")
            resCount += 1
        nowResources = start_coffee_machine(nowResources)
    elif command == "espresso" or command == "latte" \
            or command == "cappuccino":
        out = make_coffee(command, nowResources)
        if type(out) is dict:
            nowResources = out  # only update upon success
        nowResources = start_coffee_machine(nowResources)
    elif command == "off":
        return nowResources
    else:
        print("unknown command!")
        nowResources = start_coffee_machine(nowResources)


resources = start_coffee_machine(resources)
