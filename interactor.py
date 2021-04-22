import grouper
import balancer


def interact_menu():
    menu_items = ["Wind.json", "Weather.json", "Groups.json", "SailingEncounter.json"]
    chosen = show_and_select(menu_items)
    chosen_items = balancer.items_from_json(chosen)
    if chosen is "Wind.json":
        interact_main(chosen, chosen_items, keys=['apocalypseChance', 'nonApocalypseChance'])
    elif chosen is "Weather.json":
        interact_main(chosen, chosen_items)
    elif chosen is "Groups.json":
        interact_main(chosen, chosen_items, keys=['total_chance'])
    elif chosen is "SailingEncounter.json":
        group_data = balancer.items_from_json("Groups.json")
        grouper.generate_groups(chosen_items, group_data)
        interact_main(chosen, chosen_items)


def interact_main(filename, items, keys=['chance']):
    items = interact_modify(items)
    items = interact_balance(items, keys=keys)
    grouper.ungroup(items)
    interact_save(items, filename)


def interact_modify(items):
    done = False
    while not done:
        chosen = show_and_select(items)
        if 'content' in chosen:
            interact_modify(chosen['content'])
        else:
            items = modify_selected_item(items, chosen)
        done = not show_confirm_continue()
    return items


def interact_balance(items, keys):
    print("Balance New Chances?")
    if show_bool_decider():
        for key in keys:
            balancer.balance_with_groups(items, total=1000000, key=key)
            print("Items({}) Were Rebalanced To {}%".format(key, balancer.get_total_chance(items, key=key) / 10000))
    else:
        print("Chances Were Not Balanced! This Leads To Wrong Chances")
    return items


def interact_save(items, filename):
    print("Write Modified Json To File?")
    if show_bool_decider():
        balancer.write_items_to_file(filename, items)
        print("File Saved!")
    else:
        print("All Changes Were Discarded!")


def show_entry(entry):
    string_placeholder = ""
    if isinstance(entry, str):
        return entry
    if "name" in entry:
        string_placeholder += entry['name'] + " "
    if "chance" in entry:
        string_placeholder += "chance: " + str(entry['chance'] / 10000) + "% "
    if "apocalypseChance" in entry:
        string_placeholder += "apo_chance: " + str(entry['apocalypseChance'] / 10000) + "% "
    if "nonApocalypseChance" in entry:
        string_placeholder += "non_apo_chance: " + str(entry['nonApocalypseChance'] / 10000) + "% "
    if "identifier" in entry:
        string_placeholder += "Group: " + entry['identifier']['name']
    if string_placeholder is not "":
        return string_placeholder


def show_bool_decider():
    chosen = int(custom_input('[1] True\n[2] False\n', 2))
    if chosen == 1:
        return True
    if chosen == 2:
        return False
    else:
        return show_bool_decider()


def show_confirm_continue():
    print("Do you want to keep going?")
    return show_bool_decider()


def show_and_select(items):
    for count, item in enumerate(items):
        print("[{}] {}".format(count + 1, show_entry(item)))
    selection = int(custom_input("Input Int To Select\n", len(items)))
    if isinstance(items, list):
        return items[selection - 1]
    else:
        return selection - 1


def custom_input(string, int_max):
    input_string = input(string)
    while not validate(input_string, int_max):
        input_string = input(string)
    return input_string


def validate(input_string, int_max):
    if not input_string.isdecimal():
        print("Your Selection Has To Be A Number")
        return False
    elif not (1 <= int(input_string) <= int_max):
        print("Your Selection Has To Be Within The Shown Range")
        return False
    else:
        return True


def modify_selected_item(items, chosen):
    print(chosen)
    selected_field = select_dict_field(chosen)
    print(selected_field)
    edited_field = edit_field(selected_field)
    edited_item = save_field_to_item(edited_field, chosen)
    items = save_item_to_items(edited_item, items)
    return items


def select_dict_field(item):
    selection = show_and_select(item)
    for count, field in enumerate(item):
        if count == selection:
            return field, item[field]


def edit_field(field):
    new_value = ""
    if isinstance(field[1], str):
        new_value = input('Enter A New Value For "{}"\n'.format(field[0]))
    elif isinstance(field[1], int):
        while not new_value.isdecimal():
            new_value = input('Enter A New Value For "{}"\n'.format(field[0]))
        new_value = int(new_value)
    elif isinstance(field[1], bool):
        new_value = show_bool_decider()
    return field[0], new_value


def save_field_to_item(field, item):
    item[field[0]] = field[1]
    return item


def save_item_to_items(new_item, items):
    for item in items:
        if item['name'] == new_item['name']:
            item = new_item
    return items
