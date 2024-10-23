import json

img = [f"Avatar{i}.png" for i in range(1, 7)]
player = [f"P{i}" for i in range(1, 7)]


ref = dict(zip(player, img))


# Save the dictionary to a JSON file
with open('reference.json', 'w') as json_file:
    json.dump(ref, json_file)



img = [f"Avatar{i}.png" for i in range(7, 13)]
player = [f"P{i}" for i in range(1, 7)]


ref = dict(zip(player, img))


# Save the dictionary to a JSON file
with open('reference_bis.json', 'w') as json_file:
    json.dump(ref, json_file)



img = [f"Intruder{i}.png" for i in range(1, 5)]
player = [f"I{i}" for i in range(1, 5)]


ref = dict(zip(player, img))


# Save the dictionary to a JSON file
with open('reference_intruders.json', 'w') as json_file:
    json.dump(ref, json_file)

