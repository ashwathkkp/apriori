from collections import defaultdict, Counter
from itertools import permutations
import pandas as pd

def get_count(data, input_set):
	data['items'] = [set(items) for items in data['items']]
	result = 0
	for i,row in data.iterrows():
		freq = row['items'].intersection(input_set)
		if len(freq) == len(input_set):
			result += 1
	return result

min_support, confidence = 3, 0.8
data = pd.read_csv("data1.csv", names=['t_id', 'items'])
data['items'] = [list(entry) for entry in data['items']]

all_transaction_items = []
for item in data['items']:
    all_transaction_items.extend(item)

freq_1_itemset = Counter(all_transaction_items)
filtered_items = defaultdict(list)

for item,count in freq_1_itemset.items():
    if count >= min_support:
        filtered_items[count].append(item)

sorted_frequencies = list(filtered_items.keys())
sorted_frequencies.sort(reverse=True)

rearraged_transactions = pd.DataFrame({})
sorted_items_on_ranking = []

for frequency in sorted_frequencies:
    sorted_items_for_current_frequency = filtered_items[frequency]
    sorted_items_for_current_frequency.sort()
    for item in sorted_items_for_current_frequency:
        sorted_items_on_ranking.append(item)

# print(sorted_items_on_ranking)


for i,transaction in data.iterrows():
    rearranged_items = []
    for item_count in sorted_frequencies:
        sorted_items_for_current_frequency = filtered_items[item_count]
        sorted_items_for_current_frequency.sort()
        for item in sorted_items_for_current_frequency:
            for current_item in transaction['items']:
                if current_item == item:
                    rearranged_items.append(current_item)
    rearraged_transactions = rearraged_transactions.append({
        't_id': transaction['t_id'],
        'items': rearranged_items
    }, ignore_index=True)

# print(rearraged_transactions)

# frequent_pattern_tree = {}
# for i,transaction in rearraged_transactions.iterrows():
#     temp = frequent_pattern_tree
#     for item in transaction['items']:
#         if item not in temp:
#             temp[item] = {}
#         temp = temp[item]
# print(frequent_pattern_tree)

conditional_pattern_base = defaultdict(list)
for item in sorted_items_on_ranking:
    result = []
    conditional_pattern_base[item] = []
    for i,transaction in rearraged_transactions.iterrows():
        if item not in transaction['items']:
            continue
        result.extend(transaction['items'][:transaction['items'].index(item)])
    conditional_pattern_base[item].extend(result)
# print(conditional_pattern_base)

path_result = {}
for item in conditional_pattern_base:
    item_counter = Counter(conditional_pattern_base[item])
    result = []
    for t_item,count in item_counter.items():
        if count >= min_support:
            result.append(t_item)
    result.append(item)
    if len(result) > 1:
        path_result[item] = result

print(path_result)

# path = {}
# for i,t_items in path_result.items():
#     temp = path
#     for item in t_items:
#         if item not in temp:
#             temp[item] = {}
#         temp = temp[item]
# print(path)

all_paths = []
for node in path_result.keys():
	all_paths.append("".join(path_result[node]))
all_paths.sort(reverse=True)
print(all_paths)

ignore_paths, removed_redundant_paths = [],set()
for i in range(len(all_paths)-1):
	for j in range(i+1, len(all_paths)):
		if all_paths[j].startswith(all_paths[i]):
			ignore_paths.append(all_paths[i])
		if all_paths[i].startswith(all_paths[j]):
			ignore_paths.append(all_paths[j])
		if all_paths[i] not in ignore_paths:
			removed_redundant_paths.add(all_paths[i])
print(removed_redundant_paths)

longest_path = max(removed_redundant_paths, key=len)
possible_permutations = list(permutations(list(longest_path)))
print(possible_permutations)

rule_outcome_map = {}
numerator = get_count(data, set(longest_path))
print(numerator)
for i in range(1, len(longest_path)):
	for permutation in possible_permutations:
		permutation_string = "".join(list(permutation))
		left, right = list(permutation_string[:i]), list(permutation_string[i:])
		left.sort()
		right.sort()
		left, right = "".join(left), "".join(right)
		if left+"->"+right in rule_outcome_map:
			continue
		res = numerator/get_count(data, set(left))
		if res >= confidence:
			rule_outcome_map[left+"->"+right] = numerator/get_count(data, set(left))
print(rule_outcome_map)

