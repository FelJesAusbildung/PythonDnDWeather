import grouper



def build_group(items, group_identifier):
    return_items = []
    return_groups = []
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


def generate_groups(items, group_identifiers):
    for group_identifier in group_identifiers:
        group = build_group(items, group_identifier)
        items.insert(0, group)


def has_groups(items):
    has_group = False
    for item in items:
        if 'identifier' in item:
            has_group = True
    return has_group


def ungroup(items):
    has_groups = grouper.has_groups(items)
    while has_groups:
        for item in items:
            if 'identifier' in item:
                for group_item in item['content']:
                    items.append(group_item)
                items.remove(item)
        has_groups = has_groups(items)
