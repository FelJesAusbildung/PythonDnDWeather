import json
import random

import interactor
import main


def get_random_item(items):
    total_chance = sum(item['chance'] for item in items)
    random_chance = random.uniform(1, total_chance + 1)
    for ordinal, item in enumerate(items):
        if random_chance > 0:
            random_chance -= item['chance']
        else:
            chosen = items[ordinal - 1]
            break
        chosen = items[len(items) - 1]
    return chosen


def roll_weather():
    with open("Weather.json", "r") as weather_file:
        weathers = json.load(weather_file)
        chosen_weather = get_random_item(weathers)
        print("{}".format(chosen_weather['flavor']))
        roll_wind(chosen_weather)


def roll_encounter():
    with open("SailingEncounter.json", "r") as encounter_file:
        encounters = json.load(encounter_file)
        chosen_encounter = get_random_item(encounters)
        if chosen_encounter['flavor'] != "":
            print("{}".format(chosen_encounter['flavor']))


def roll_wind(weather):
    with open("Wind.json", "r") as wind_file:
        winds = json.load(wind_file)
        for wind in winds:
            if weather['isApocalypse']:
                wind['chance'] = wind['apocalypseChance']
            else:
                wind['chance'] = wind['nonApocalypseChance']
        chosen_wind = get_random_item(winds)
        speed = random.randint(chosen_wind['minSpeed'], chosen_wind['maxSpeed'])
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        direction = random.choice(directions)
        print("{}, Wind Speed: {}km/h, Wind Direction: {}".format(chosen_wind['flavor'], speed, direction))


def roll():
    weeks = int(input('number of weeks to calculate: \n'))
    for number in range(0, weeks):
        print()
        print("Week {}:".format(number + 1))
        roll_encounter()
        roll_weather()


def roll_loop():
    done = False
    while not done:
        roll()
        done = not interactor.confirm_done()
        main.clear()


if __name__ == "__main__":
    pass
