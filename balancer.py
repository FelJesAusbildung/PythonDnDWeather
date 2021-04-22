import json
import logging

import grouper


def items_from_json(filename):
    logging.info("loading file {}".format(filename))
    with open(filename, "r") as file:
        return json.load(file)


def write_items_to_file(filename, json_data):
    logging.info("saving file {}".format(filename))
    with open(filename, "w") as file:
        json.dump(json_data, file, indent=2)


def get_list_of_items_for_key(items, key='chance'):
    logging.info("building key list for {} in {}".format(key, items))
    chances = []
    for item in items:
        chances.append(item[key])
    logging.info("finished building key list for {}".format(key))
    return chances


def get_sum_of_items_for_key(items, key='chance'):
    logging.info("summing items for {}".format(key))
    logging.debug("items: {}".format(items))
    _sum = 0
    for item in items:
        if 'identifier' in item:
            logging.info("found group, summing recursively")
            _sum += get_sum_of_items_for_key(item['content'])
        else:
            _sum += item[key]
    logging.debug("sum: {}".format(_sum))
    logging.info("finished summing items for {}".format(key))
    return _sum


def balance(items, key='chance', total=100, inflation_factor=1000):
    logging.info("balancing items {}".format(items))
    logging.debug("key: {}, total: {}, inflation_factor: {}".format(key, total, inflation_factor))
    chances = get_corrected_chances(inflation_factor=inflation_factor, items=items, key=key, total=total)
    for item, chance in zip(items, chances):
        logging.debug("overwriting chance {} on item {}".format(chance, item))
        item[key] = chance
    logging.info("finished balancing items {}".format(items))


def get_corrected_chances(items, key, total, inflation_factor):
    logging.info("generating corrected chances for {}".format(items))
    new_total = total / inflation_factor
    chances = get_list_of_items_for_key(items, key)
    chance_divisor = sum(chances) / new_total
    corrected_chances = []
    logging.debug("chance_divisor: {}, total to inflate to: {}".format(chance_divisor, new_total))
    for chance in chances:
        logging.debug("new chance: {}".format(int((chance / chance_divisor) * inflation_factor)))
        corrected_chances.append(int((chance / chance_divisor) * inflation_factor))
    logging.info("finished generating corrected chances {}".format(corrected_chances))
    return corrected_chances


def balance_with_groups(items, total=1000000):
    logging.info("started balancing with groups {}".format(items))
    has_groups = grouper.check_for_groups_in(items)
    for item in items:
        if 'identifier' in item:
            logging.debug("setting chance for group {}".format(item))
            item['chance'] = item['identifier']['total_chance']
    balance(items, total=total)
    for item in items:
        if 'identifier' in item:
            logging.debug("updating total_chance for group {}".format(item))
            item['identifier']['total_chance'] = item['chance']
    if has_groups:
        for item in items:
            if 'identifier' in item:
                logging.info("found group, balancing recursively")
                balance_with_groups(item['content'], item['identifier']['total_chance'])
    logging.info("finished balancing with groups {}".format(items))
