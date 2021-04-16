from time import sleep
import interactor, roller
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_main_decider():
    choices = ["Roll Weather", "Modify Json Data"]
    pick = interactor.show_and_select(choices)
    if pick == "Roll Weather":
        done = False
        while not done:
            roller.roll()
            done = not interactor.confirm_done()
            clear()
    elif pick == "Modify Json Data":
        interactor.main_loop()
    print("Shutting Down")
    sleep(1)


if __name__ == "__main__":
    run_main_decider()
