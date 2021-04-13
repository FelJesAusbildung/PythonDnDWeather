from balancer import *


def show_and_select(items):
    for count, item in enumerate(items):
        print('[{0}] {1} {2}'.format(count, item['name'], item['chance']))
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
    print(field)
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


def modify(filename):
    items = items_from_json(filename)
    done = False
    while not done:
        selected_item = show_and_select(items)
        selected_field = select_and_modify(selected_item)
        edited_field = edit_field(selected_field)
        edited_item = save_field_to_item(edited_field, selected_item)
        items = save_item_to_items(edited_item, items)
        done = not confirm_done()
    print("Balance New Chances?")
    if bool_decider():
        items = balance(items, total=100000)
        print(items)
        print("Items Were Rebalanced To {0}%".format(get_total_chance(items)/1000))
    else:
        print("Chances Were Not Balanced! This Leads To Strange Chances")
    print("Write Modified Json To File?")
    if bool_decider():
        write_items_to_file(filename, items)
        print("File Saved!")
    else:
        print("All Changes Were Discarded!")


def old_test(weather):
    selected_item = show_and_select(weather)
    selected_field = select_and_modify(selected_item)
    edited_field = edit_field(selected_field)
    edited_item = save_field_to_item(edited_field, selected_item)
    print(save_item_to_items(edited_item, weather))


if __name__ == "__main__":
    modify("Weather.json")
    # old_test(weather)
