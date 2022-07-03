from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

theMaker = CoffeeMaker()
theMachine = MoneyMachine()
theMenu = Menu()
isOn = True

while isOn:
    choice = input(f"Please choose your preferred drink ({theMenu.get_items()}): ")
    if choice == "off":
        isOn = False
    elif choice == "report":
        theMaker.report()
        theMachine.report()
    else:
        drink = theMenu.find_drink(choice)
        if theMaker.is_resource_sufficient(drink) \
                and theMachine.make_payment(drink.cost):
            theMaker.make_coffee(drink)

# print(theMenu.get_items())
# input("Please ")
