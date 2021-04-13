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


def gen_group_dict(name, items):
    _, group_total = get_group(items, name)
    return {'name': name, 'total_chance': group_total}


def gen_groups_list(items, group_names):
    groups_list = list()
    for temp_group_name in group_names:
        temp_group = gen_group_dict(temp_group_name, items)
        groups_list.append(temp_group)
    return groups_list


def print_groups_details(groups):
    print(groups)
    for group_name in groups:
        group, group_total = get_group(encounters, group_name['name'])
        print(group_total, group)


def gen_groups_json(filename, items, items_names):
    groups = gen_groups_list(items, items_names)
    write_items_to_file(filename, groups)


if __name__ == "__main__":
    encounters = items_from_json("SailingEncounter.json")
    encounter_group_names = ["damned", "damned9", "damned11", "damned17", "unique", "unique_non", "unique_dragon",
                             "unique_inquisition", "trader"]
    gen_groups_json("Groups.json", encounters, encounter_group_names)
