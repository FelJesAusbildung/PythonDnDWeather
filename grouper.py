from balancer import *


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
        # print(return_groups)
        total_chance = get_total_chance(return_groups)
        return_group_dict = {"identifier": {"name": group_identifier['name'], "total_chance": total_chance},
                             "content": return_groups}
    return return_group_dict


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
            return items


def insert_group(items, replacing_group):
    position = 0
    items_to_remove = []
    for count, item in enumerate(items):
        if 'identifier' in item:
            continue
        if replacing_group['identifier']['name'].upper() in item['name']:
            items_to_remove.append(item)
            if not position:
                position = count
    for item in items_to_remove:
        items.remove(item)
    items.insert(position, replacing_group)
    return items


def extract_group(items, group_identifier):
    contents_placeholder, _ = get_group(items, group_identifier['name'])
    for group_item in contents_placeholder:
        for item in items:
            if item['name'] == group_item['name']:
                items.remove(item)
    return items, contents_placeholder


def groupify(items, groups):
    grouped_items = []
    inserted = list(items)
    for group_identifier in groups:
        _, contents = extract_group(inserted, group_identifier)
        temp_group = {"identifier": group_identifier, "content": contents}
        insert_group(inserted, temp_group)
        grouped_items.append(temp_group)
        print(grouped_items)
    for group_to_insert in reversed(grouped_items):
        inserted = insert_group(inserted, group_to_insert)
    return inserted


def insert(subgroup, total):
    total.insert(0, subgroup)


if __name__ == "__main__":
    groups = items_from_json("Groups.json")
    encounters = items_from_json("SailingEncounter.json")
    test1 = [{"identifier": {"name": "A_A", "total_chance": "4"},
              "content": [{"name": "A_A1", "chance": "1"}, {"name": "A_A2", "chance": "1"}]},
             {"name": "A_B1", "chance": "1"},
             {"name": "A_B2", "chance": "1"}, {"name": "B_Z1", "chance": "1"}, {"name": "B_Z2", "chance": "1"},
             {"name": "C_Z1", "chance": "1"}, {"name": "D_Z1", "chance": "1"}, {"name": "E_Z1", "chance": "1"}]
    test2 = [{"name": "A_A", "total_chance": "2"}, {"name": "A_B", "total_chance": "2"},
             {"name": "A", "total_chance": "4"}, {"name": "B_", "total_chance": "2"}]
    # for group_identifier in test2:
    #     built = get_group_for_extract(test1, group_identifier)
    #     insert(built, test1)
    # print(json.dumps(test1, indent=2))
    for group_identifier in groups:
        built = build_group(encounters, group_identifier)
        insert(built, encounters)
    string = json.dumps(encounters, indent=2)
    write_items_to_file("grouped_encounters_test.json", encounters)
    pass
