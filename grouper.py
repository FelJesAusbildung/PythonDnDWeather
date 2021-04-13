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


if __name__ == "__main__":
    encounters = items_from_json("SailingEncounter.json")
    randoms, randoms_total = get_group(encounters, "random")
    print("-------------------------------------------------")
    randoms = balance_with_output(randoms, total=100, key='chance')
    insert(randoms, encounters)
    pass
