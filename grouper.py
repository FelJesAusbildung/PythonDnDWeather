import logging


def build_group(items, group_identifier):
    logging.info("building group for {}".format(group_identifier))
    return_groups = []
    return_items = []
    items_to_remove = []
    for item in items:
        if 'identifier' in item:
            if group_identifier['name'].upper() in item['identifier']['name'].upper():
                logging.debug("matched {} to {}".format(item, group_identifier))
                return_groups.append(item)
                items_to_remove.append(item)
        if 'name' in item:
            if group_identifier['name'].upper() in item['name']:
                logging.debug("matched {} to {}".format(item, group_identifier))
                return_items.append(item)
                items_to_remove.append(item)
    for item in items_to_remove:
        logging.debug("removing from items: {}".format(item))
        items.remove(item)
    if len(return_items) == 0 and len(return_groups) == 1:
        logging.info("only found one group({})".format(return_groups[0]))
        return return_groups[0]
    else:
        for item in return_items:
            logging.debug("moving item({}) to consolidated group content".format(item))
            return_groups.append(item)
        total_chance = group_identifier['total_chance']
        return_group_dict = {"identifier": {"name": group_identifier['name'], "total_chance": total_chance},
                             "content": return_groups}
        logging.debug("built group dictionary {}".format(return_group_dict))
    logging.info("finished building group for {}".format(group_identifier))
    return return_group_dict


def generate_groups(items, group_identifiers):
    logging.info("stated generating groups")
    for group_identifier in group_identifiers:
        built = build_group(items, group_identifier)
        logging.debug("inserting new group {}".format(built))
        items.insert(0, built)
    logging.info("finished generating groups")


def check_for_groups_in(items):
    logging.info("checking for groups in {}".format(items))
    there_are_groups = False
    for item in items:
        if 'identifier' in item:
            logging.debug("found group {}".format(item))
            there_are_groups = True
    logging.info("finished checking for groups, Found: {}".format(there_are_groups))
    return there_are_groups


def ungroup(items):
    logging.info("ungrouping {}".format(items))
    tested = check_for_groups_in(items)
    while tested:
        for item in items:
            if 'identifier' in item:
                for group_item in item['content']:
                    logging.debug("moving item({}) from group({}) to items".format(group_item, item))
                    items.append(group_item)
                logging.debug("removing group({})".format(item))
                items.remove(item)
        tested = check_for_groups_in(items)
    logging.info("finished ungrouping")
