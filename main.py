import os
from time import sleep

import interactor
import roller


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_dialogue():
    choices = ["Roll Weather", "Modify Json Data", "Exit"]
    chosen = interactor.show_and_select(choices)
    if chosen == "Roll Weather":
        roller.roll_loop()
    elif chosen == "Modify Json Data":
        interactor.interact_menu()
    elif chosen == "Exit":
        close()
    main_dialogue()


def close():
    print("Shutting Down")
    sleep(1)
    exit()


if __name__ == "__main__":
    main_dialogue()
