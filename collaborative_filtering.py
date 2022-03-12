import json
import pandas as pd
import tqdm

json_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'JK', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'WX', 'Y', 'Z']

def convert_to_str(i_str):
    if type(i_str) is bytes:
        return i_str.decode('utf-8')
    else:
        return i_str.encode('utf-8')

def make_item_lists(file_path):
    items = set()
    with open(file_path) as json_file:
        dataset = json.load(json_file)
        for key in dataset:
            items.add(key)
            demo = dataset[key]['demo']

            for i in range(len(demo)):
                formula = demo[i]['formula']
                total = demo[i]['total']

                for item in formula:
                    items.add(item)
    return items

item_lists = set()
for alphabet in json_list:
    item_lists.update(make_item_lists('./datasets/{}.json'.format(alphabet)))



'''
--------------------------------------------------------
        |    item_#1    |    item_#2    |    item_#3     ...
--------------------------------------------------------
name_#1 |  amount_#1-1  |  amount_#1-2  |  amount_#1-3   ...
name_#2 |  amount_#2-1  |  amount_#2-2  |  amount_#2-3   ...
--------------------------------------------------------
'''


def add_to_dataframe(data_frame, json_path):
    with open(json_path) as json_file:
        dataset = json.load(json_file)
        for key in dataset:
            demo = dataset[key]['demo']
            for i in range(len(demo)):
                data_format = dict.fromkeys(item_lists, 0.0)
                formula = demo[i]['formula']
                total = float(demo[i]['total'])
                #name = demo[i]['name'] 
                for sub_item in formula:
                    #if type(sub_item) is not str:
                    #    continue
                    if formula[sub_item] == 'trace':
                        data_format[sub_item] = 0.0001
                    else:
                        amount = float(formula[sub_item])
                        #amount = 0.0 if type(amount) is bytes else float(amount)
                        data_format[sub_item] = amount/total
                data_frame = data_frame.append(data_format, ignore_index=True)
    return data_frame


table = pd.DataFrame()
for alphabet in tqdm.tqdm(json_list):
    table = add_to_dataframe(table, './datasets/{}.json'.format(alphabet))
table.to_csv('./datasets/AtoZ_relative.csv', sep=',', na_rep='NaN', float_format='%.6e')
    
