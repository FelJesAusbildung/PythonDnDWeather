from balancer import *


def get_group(items, identifier, key='chance'):
    group = []
    for item in items:
        if identifier.upper() in item['name']:
            group.append(item)
    return group, get_total_chance(group, key=key)


def insert(group, items):
    for item in items:
        for group_item in group:
            if group_item['name'] == item['name']:
                item = group_item
    return items


def test():
    encounters_test = items_from_json("SailingEncounter.json")
    randoms, randoms_total = get_group(encounters_test, "random")
    print(randoms_total)
    print("-------------------------------------------------")
    randoms[3]['chance'] = 2000
    randoms = balance_with_output(randoms, total=randoms_total, key='chance', inflation_factor=1)
    insert(randoms, encounters_test)


# unnecessary as a dict but good choice if groups need to be expanded later
def gen_group(name):
    return {'name': name}


if __name__ == "__main__":
    groups = list()
    group_names = ["damned", "damned9", "damned11", "damned17", "unique", "unique_non", "unique_dragon", "unique_inquisition", "trader"]
    for group_name in group_names:
        group = gen_group(group_name)
        groups.append(group)
    print(groups)
    with open("Groups.json", "w") as file:
        json.dump(groups, file, indent=2)
    encounters = items_from_json("SailingEncounter.json")
    for group_name in groups:
        group, group_total = get_group(encounters, group_name['name'])
        print(group_total, group)
