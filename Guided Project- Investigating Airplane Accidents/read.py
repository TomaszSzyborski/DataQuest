with open("AviationData.txt", "r") as f:
    aviation_data = f.readlines()
    
    aviation_list =[]
    for line in aviation_data:
        a = line.strip().split("|")
        aviation_list.append([q.strip() for q  in a])

lax_code = []

for row in aviation_list:
    #print(row)
    if "LAX94LA336" in row:
        lax_code.append(row)
        
#print(lax_code)


aviation_dict_list = []
keys = aviation_data[0].split("|")
for i, line in enumerate(aviation_data):
    l = line.strip().split("|")
    d = {k.strip():v.strip() for k,v in zip(keys,l)}
    aviation_dict_list.append(d)
    
print(aviation_dict_list[1]["Location"].split(",")[1].strip())

lax_dict = []

for d in aviation_dict_list:
    if "LAX94LA336" in d.keys():
        lax_dict.append(d)

from collections import Counter

states = []
for d in aviation_dict_list:
    if d["Country"] == "United States" and ',' in d["Location"]:
        stat = d["Location"].split(',')[1].strip()
        if len(stat)==2:
            states.append(stat)
    
state_accidents = Counter(states)

print(state_accidents)

monthly_injuries = []
for d in aviation_dict_list:
    day, month, year = d["Event Date"].split("/")