from balancer import *


def show_and_select(items, key=['chance']):
    for count, item in enumerate(items):
        print("[{0}] {1}".format(count, item))
        # if type(item) is dict:
        #     if key[1] is not None:
        #         print('[{0}] {1} {2}%'.format(count, item['name'], item[key[0]]/10000, item[key[1]]/10000))
        #     else:
        #         print('[{0}] {1} {2}%'.format(count, item['name'], item[key[0]]/10000))
        # else:
        #     print("[{0}] {1}".format(count, item))
    selection = int(input("Input Int To Select Item To Modify\n"))
    return items[selection]


def select_and_modify(item):
    for count, field in enumerate(item):
        print('[{0}] {1}'.format(count, field))
    selection = int(input("Input Int To Select Field To Modify\n"))
    for count, field in enumerate(item):
        if count == selection:
            return field, item[field]


def bool_decider():
    selector = int(input('[1] True\n[2] False\n'))
    if selector == 1:
        return True
    if selector == 2:
        return False
    else:
        return bool_decider()


def edit_field(field):
    if type(field[1]) == str:
        new_value = input('Enter A New Value For "{0}"\n'.format(field[0]))
    elif type(field[1]) == int:
        new_value = int(input('Enter A New Value For "{0}"\n'.format(field[0])))
    elif type(field[1]) == float:
        new_value = float(input('Enter A New Value For "{0}"\n'.format(field[0])))
    elif type(field[1]) == bool:
        new_value = bool_decider()
    return field[0], new_value


def save_field_to_item(field, item):
    item[field[0]] = field[1]
    return item


def save_item_to_items(new_item, items):
    for item in items:
        if item['name'] == new_item['name']:
            item == new_item
    return items


def confirm_done():
    print("Do you want to modify another item?")
    return bool_decider()


def modify(filename, keys=['chance']):
    items = items_from_json(filename)
    done = False
    while not done:
        selected_item = show_and_select(items)
        print(selected_item)
        selected_field = select_and_modify(selected_item)
        print(selected_field)
        edited_field = edit_field(selected_field)
        edited_item = save_field_to_item(edited_field, selected_item)
        items = save_item_to_items(edited_item, items)
        done = not confirm_done()
    print("Balance New Chances?")
    if bool_decider():
        for key in keys:
            print(key)
            items = balance(items, total=1000000, key=key)
        print(items)
        for key in keys:
            print("Items({0}) Were Rebalanced To {1}%".format(key, get_total_chance(items, key=key) / 10000))
    else:
        print("Chances Were Not Balanced! This Leads To Strange Chances")
    print("Write Modified Json To File?")
    if bool_decider():
        write_items_to_file(filename, items)
        print("File Saved!")
    else:
        print("All Changes Were Discarded!")


if __name__ == "__main__":
    modifiable = ["Weather.json", "Wind.json", "Groups.json", "SailingEncounters.json"]
    pick = show_and_select(modifiable)
    if pick is "Wind.json":
        modify(pick, keys=['apocalypseChance', 'nonApocalypseChance'])
    else:
        modify(pick)
    # old_test(weather)
