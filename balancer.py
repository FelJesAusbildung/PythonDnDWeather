import json


def items_from_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def write_items_to_file(filename, json_data):
    with open(filename, "w") as file:
        json.dump(json_data, file, indent=2)


def get_chances(items, key='chance'):
    chances = []
    for item in items:
        chances.append(item[key])
    return chances


def get_total_chance(items, key='chance'):
    chances = get_chances(items, key)
    return sum(chances)


def balance(items, key='chance', total=100, inflation_factor=1000):
    chances = get_corrected_chances(inflation_factor=inflation_factor, items=items, key=key, total=total)
    for item, chance in zip(items, chances):
        item[key] = chance
    return items


def get_corrected_chances(inflation_factor, items, key, total):
    new_total = total/inflation_factor
    chances = get_chances(items, key)
    chance_divisor = sum(chances) / new_total
    corrected_chances = []
    for chance in chances:
        corrected_chances.append(int((chance / chance_divisor) * inflation_factor))
    return corrected_chances


def balance_with_output(items, key='chance', total=100, inflation_factor=1000):
    old_chances = get_chances(items, key)
    print("old chances: ", old_chances, "Total:", get_total_chance(items, key))
    balanced_items = balance(items=items, key=key, inflation_factor=inflation_factor, total=total)
    balanced_chances = get_chances(balanced_items, key)
    print("rebalanced chances: ", balanced_chances, "Total:", get_total_chance(items, key))
    return balanced_items


def balance_file(filename, key='chance', total=100, inflation_factor=1000):
    items = items_from_json(filename)
    balanced_items = balance_with_output(items=items, key=key, inflation_factor=inflation_factor, total=total)
    write_items_to_file(filename, balanced_items)


if __name__ == "__main__":
    # balance_file("Weather.json")
    # balance_file("Wind.json", key='apocalypseChance')
    # balance_file("Wind.json", key='nonApocalypseChance')
    # balance_file("SailingEncounter.json")
    balance_with_output(items_from_json("SailingEncounter.json"), total=100)
