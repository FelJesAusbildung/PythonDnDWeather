import json
import grouper


def items_from_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def write_items_to_file(filename, json_data):
    with open(filename, "w") as file:
        json.dump(json_data, file, indent=2)


def get_list_of_items_for_key(items, key='chance'):
    chances = []
    for item in items:
        chances.append(item[key])
    return chances


def get_total_chance(items, key='chance'):
    chance_placeholder = 0
    for item in items:
        if 'identifier' in item:
            chance_placeholder += get_total_chance(item['content'])
        else:
            chance_placeholder += item[key]
    return chance_placeholder


def balance(items, key='chance', total=100, inflation_factor=1000):
    chances = get_corrected_chances(inflation_factor=inflation_factor, items=items, key=key, total=total)
    for item, chance in zip(items, chances):
        item[key] = chance


def get_corrected_chances(items, key, total, inflation_factor):
    new_total = total / inflation_factor
    chances = get_list_of_items_for_key(items, key)
    chance_divisor = sum(chances) / new_total
    corrected_chances = []
    for chance in chances:
        corrected_chances.append(int((chance / chance_divisor) * inflation_factor))
    return corrected_chances


def balance_with_groups(items, total=1000000):
    has_groups = grouper.check_for_groups_in(items)
    for item in items:
        if 'identifier' in item:
            item['chance'] = item['identifier']['total_chance']
    balance(items, total=total)
    for item in items:
        if 'identifier' in item:
            item['identifier']['total_chance'] = item['chance']
    if has_groups:
        for item in items:
            if 'identifier' in item:
                balance_with_groups(item['content'], item['identifier']['total_chance'])
    else:
        return items
