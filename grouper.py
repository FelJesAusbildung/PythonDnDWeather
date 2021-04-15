import json
from balancer import get_total_chance, items_from_json, write_items_to_file


def get_group(items, identifier, key='chance'):
    group = []
    flag = False
    for item in items:
        if identifier.upper() in item['name']:
            group.append(item)
        if key in item:
            flag = True
    if flag:
        return group, get_total_chance(group, key=key)
    else:
        return group


def build_group(items, group_identifier):
    return_groups = []
    return_items = []
    items_to_remove = []
    for item in items:
        if 'identifier' in item:
            if group_identifier['name'].upper() in item['identifier']['name'].upper():
                return_groups.append(item)
                items_to_remove.append(item)
        if 'name' in item:
            if group_identifier['name'].upper() in item['name']:
                return_items.append(item)
                items_to_remove.append(item)
    for item in items_to_remove:
        items.remove(item)
    if len(return_items) == 0 and len(return_groups) == 1:
        return return_groups[0]
    else:
        for item in return_items:
            return_groups.append(item)
        total_chance = group_identifier['total_chance']
        return_group_dict = {"identifier": {"name": group_identifier['name'], "total_chance": total_chance},
                             "content": return_groups}
    return return_group_dict


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


def overwrite(group, items):
    for item in items:
        for group_item in group:
            if group_item['name'] == item['name']:
                item = group_item
    return items


def replace(items, entry_to_replace, replacing_entries):
    for count, item in enumerate(items):
        if item['name'] == entry_to_replace['name']:
            items.remove(item)
            for replacing_item in reversed(replacing_entries):
                items.insert(count, replacing_item)
            return items


def insert(subgroup, total):
    total.insert(0, subgroup)


def generate_groups(items, group_identifiers):
    for group_identifier in group_identifiers:
        built = build_group(items, group_identifier)
        insert(built, items)


def test_for_group(items):
    there_are_groups = False
    for item in items:
        if 'identifier' in item:
            there_are_groups = True
    return there_are_groups


def ungroup(items):
    tested = test_for_group(items)
    while tested:
        for item in items:
            if 'identifier' in item:
                for group_item in item['content']:
                    items.append(group_item)
                items.remove(item)
        tested = test_for_group(items)


if __name__ == "__main__":
    groups = items_from_json("Groups.json")
    encounters = items_from_json("SailingEncounter.json")
    generate_groups(encounters, groups)
    print(json.dumps(encounters, indent=2))
    write_items_to_file("grouped_encounters_test.json", encounters)
