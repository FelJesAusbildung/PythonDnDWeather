import json
import random
import logging

import interactor
import main


def get_random_item(items):
    logging.info("picking random item")
    total_chance = sum(item['chance'] for item in items)
    random_chance = random.uniform(1, total_chance + 1)
    logging.info("picked {} out of {}".format(random_chance, total_chance))
    for ordinal, item in enumerate(items):
        if random_chance > 0:
            logging.debug("{} {} is still above 0. item:{}".format(ordinal, random_chance, item))
            random_chance -= item['chance']
        else:
            logging.debug("{} {} is no longer above 0. item:{}".format(ordinal, random_chance, item))
            chosen = items[ordinal - 1]
            break
        chosen = items[len(items) - 1]
    logging.info("picked {}".format(chosen))
    return chosen


def roll_weather():
    logging.info("rolling weather")
    with open("Weather.json", "r") as weather_file:
        weathers = json.load(weather_file)
        chosen_weather = get_random_item(weathers)
        print("{}".format(chosen_weather['flavor']))
        roll_wind(chosen_weather)
    logging.info("finished rolling weather")


def roll_encounter():
    logging.info("rolling encounter")
    with open("SailingEncounter.json", "r") as encounter_file:
        encounters = json.load(encounter_file)
        chosen_encounter = get_random_item(encounters)
        if chosen_encounter['flavor'] != "":
            print("{}".format(chosen_encounter['flavor']))
    logging.info("finished rolling encounter")


def roll_wind(weather):
    logging.info("rolling wind with {}".format(weather))
    with open("Wind.json", "r") as wind_file:
        winds = json.load(wind_file)
        for wind in winds:
            if weather['isApocalypse']:
                logging.debug("assigning apocalypseChance({}) to chance for {}".format(wind['apocalypseChance'], wind))
                wind['chance'] = wind['apocalypseChance']
            else:
                logging.debug("assigning nonApocalypseChance({}) to chance for {}".format(wind['nonApocalypseChance'], wind))
                wind['chance'] = wind['nonApocalypseChance']
        chosen_wind = get_random_item(winds)
        speed = random.randint(chosen_wind['minSpeed'], chosen_wind['maxSpeed'])
        logging.debug("speed {} in range of {}-{}".format(speed, chosen_wind['minSpeed'], chosen_wind['maxSpeed']))
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        direction = random.choice(directions)
        print("{}, Wind Speed: {}km/h, Wind Direction: {}".format(chosen_wind['flavor'], speed, direction))
        logging.info("finished rolling wind")


def roll():
    logging.info("starting roll dialogue")
    weeks = int(input('number of weeks to calculate: \n'))
    for number in range(0, weeks):
        print("\nWeek {}:".format(number + 1))
        roll_encounter()
        roll_weather()
    logging.info("finished roll dialogue")


def roll_loop():
    logging.info("starting roll loop")
    done = False
    while not done:
        roll()
        done = not interactor.show_confirm_continue()
        main.clear()
    logging.info("finished roll loop")
