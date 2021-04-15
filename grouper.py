from balancer import *


def get_group(items, identifier, key='chance'):
    group = []
    for item in items:
        if identifier.upper() in item['name']:
            group.append(item)
    return group, get_total_chance(group, key=key)


def overwrite(group, items):
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


def gen_groups_json(filename, items, items_names):
    groups = gen_groups_list(items, items_names)
    write_items_to_file(filename, groups)


def gen_json_for_encounters():
    encounters = items_from_json("SailingEncounter.json")
    encounter_group_names = ["damned", "damned9", "damned11", "damned17", "unique", "unique_non", "unique_dragon",
                             "unique_inquisition", "trader", "other"]
    gen_groups_json("Groups.json", encounters, encounter_group_names)


def print_groups_details(groups, items):
    print(groups)
    for group_name in groups:
        group, group_total = get_group(items, group_name['name'])
        print(group_total, group)


def replace(items, entry_to_replace, replacing_entries):
    for count, item in enumerate(items):
        if item['name'] == entry_to_replace['name']:
            items.remove(item)
            for replacing_item in reversed(replacing_entries):
                items.insert(count, replacing_item)
            return


if __name__ == "__main__":
    list1 = [{"name": "1"}, {"name": "2"}, {"name": "3"}, {"name": "4"}]
    list2 = [{"name": "a"}, {"name": "b"}, {"name": "c"}, {"name": "d"}]
    to_replace = list1[2]
    replace(list1, to_replace, list2)
    print(list1)
    replace(list1, {"name": "c"}, [{"name": "z"}])
    print(list1)
    pass
