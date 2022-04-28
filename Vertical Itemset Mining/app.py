from collections import defaultdict
import pandas as pd

min_support = 2
data = pd.read_csv("data.csv", names=['t_id', 'items'])
data['items'] = [item.split(';') for item in data['items']]

vertical_data = defaultdict(set)
for i,row in data.iterrows():
    for item in row['items']:
        vertical_data[item].add(row['t_id'])
print(vertical_data)

freq_1_itemset = {}
for item in vertical_data.keys():
    if len(vertical_data[item]) >= min_support:
        freq_1_itemset[item] = vertical_data[item]
print(freq_1_itemset)

freq_2_itemset = {}
for item in vertical_data.keys():
    for other_item in vertical_data.keys():
        if item == other_item:
            continue
        result = vertical_data[item].intersection(vertical_data[other_item])
        if len(result) >= min_support:
            freq_2_itemset[item+" "+other_item] = result
print(freq_2_itemset)

filtered_freq_2_items = set()

for items in freq_2_itemset.keys():
    current_items = items.split(' ')
    for i in current_items:
        filtered_freq_2_items.add(i)

filtered_freq_2_items = list(filtered_freq_2_items)

freq_3_itemset = {}

for i in range(len(filtered_freq_2_items)-2):
    for j in range(i+1, len(filtered_freq_2_items)-1):
        for k in range(j+1, len(filtered_freq_2_items)):
            result = vertical_data[filtered_freq_2_items[i]].intersection(vertical_data[filtered_freq_2_items[j]]).intersection(vertical_data[filtered_freq_2_items[k]])
            if len(result) >= min_support:
                freq_3_itemset[filtered_freq_2_items[i]+" "+filtered_freq_2_items[j]+" "+filtered_freq_2_items[k]] = result

print(freq_3_itemset)

filtered_freq_3_items = set()

for items in freq_3_itemset.keys():
    current_items = items.split(' ')
    for i in current_items:
        filtered_freq_3_items.add(i)

filtered_freq_3_items = list(filtered_freq_3_items)
freq_4_itemset = {}
for i in range(len(filtered_freq_3_items)-3):
    for j in range(i+1, len(filtered_freq_3_items)-2):
        for k in range(j+1, len(filtered_freq_3_items)-1):
            for l in range(k+1, len(filtered_freq_3_items)):
                result = vertical_data[filtered_freq_3_items[i]].intersection(vertical_data[filtered_freq_3_items[j]]).intersection(vertical_data[filtered_freq_3_items[k]]).intersection(vertical_data[filtered_freq_3_items[l]])
                print(result)
                if len(result) >= min_support:
                    freq_4_itemset[filtered_freq_3_items[i]+" "+filtered_freq_3_items[j]+" "+filtered_freq_3_items[k]+" "+filtered_freq_3_items[l]] = result
print(freq_4_itemset)