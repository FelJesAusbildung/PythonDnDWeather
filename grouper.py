import json
import balancer


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


def insert(subgroup, total):
    total.insert(0, subgroup)


def generate_groups(items, group_identifiers):
    for group_identifier in group_identifiers:
        built = build_group(items, group_identifier)
        insert(built, items)


def check_for_groups_in(items):
    there_are_groups = False
    for item in items:
        if 'identifier' in item:
            there_are_groups = True
    return there_are_groups


def ungroup(items):
    tested = check_for_groups_in(items)
    while tested:
        for item in items:
            if 'identifier' in item:
                for group_item in item['content']:
                    items.append(group_item)
                items.remove(item)
        tested = check_for_groups_in(items)


if __name__ == "__main__":
    pass
