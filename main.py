import os
from time import sleep
import logging

import interactor
import roller


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_dialogue():
    logging.info("starting main dialogue")
    choices = ["Roll Weather", "Modify Json Data", "Exit"]
    chosen = interactor.show_and_select(choices)
    if chosen == "Roll Weather":
        roller.roll_loop()
    elif chosen == "Modify Json Data":
        interactor.main_loop()
    elif chosen == "Exit":
        close()
    main_dialogue()


def close():
    print("Shutting Down")
    sleep(1)
    logging.info("shutting down program")
    exit()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s' , filename="DnDWeather.log", filemode="w", level=logging.DEBUG)
    main_dialogue()
