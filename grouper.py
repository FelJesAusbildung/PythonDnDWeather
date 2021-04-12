from balancer import *


def get_group(items, identifier):
    group = []
    for item in items:
        if identifier.upper() in item['name']:
            group.append(item)
    return group


if __name__ == "__main__":
    encounters = items_from_json("SailingEncounter.json")
    randoms = get_group(encounters, "random")
    randoms_sting = json.dumps(randoms, indent=2)
    print(randoms_sting)
    randoms, _ = balance(randoms, total=5, key='chance')
    randoms_sting = json.dumps(randoms, indent=2)
    print(randoms_sting)

    pass
