import json

img = [f"Avatar{i}.png" for i in range(1, 7)]
player = [f"P{i}" for i in range(1, 7)]


ref = dict(zip(player, img))


# Save the dictionary to a JSON file
with open('reference.json', 'w') as json_file:
    json.dump(ref, json_file)



#with open('Input/reference.json', 'r') as json_file:
#    loaded_dict = json.load(json_file)