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


def balance(items, key='chance', total=100, inflation_factor=1000):
    chances = get_chances(items, key)
    chance_divisor = sum(chances) / total
    corrected_chances = []
    for chance in chances:
        corrected_chances.append(int((chance / chance_divisor) * inflation_factor))
    sum_corrected_chances = sum(corrected_chances)
    for item, chance in zip(items, chances):
        item[key] = chance
    return items


def balance_with_output(items, key='chance', total=100, inflation_factor=1000):
    chances = get_chances(items, key)
    print("old chances: ", chances)
    balanced_chances, new_total = balance(items, key, inflation_factor)
    print("rebalanced chances: ", balanced_chances, "Total: ", new_total)
    return balanced_chances, new_total


def balance_file(filename, key='chance', total=100, inflation_factor=1000):
    items = items_from_json(filename)
    balanced_chances, _ = balance_with_output(items, key, inflation_factor)
    for item, chance in zip(items, balanced_chances):
        item[key] = chance
    write_items_to_file(filename, items)


if __name__ == "__main__":
    balance_file("Weather.json")
    balance_file("Wind.json", key='apocalypseChance')
    balance_file("Wind.json", key='nonApocalypseChance')
    balance_file("SailingEncounter.json")
