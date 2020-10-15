import os , json , csv ,re , itertools , pprint , requests
import script.preprocessing as p
import script.util as util
import script.create as create
import script.conf as c
from langdetect import detect
from collections import defaultdict, Counter



# PATCH /api/:api_resource/:id
#def update_item(data_row, item_set_id=None, item_type=None, res_class=None, property_ids=None):
def update_item(row, table_args, args_conf, tables_path, update_rules):

    subject_row_id = create.generate_row_id(row, table_args, args_conf)
    subject_omeka_item = find_item_from_row_id(subject_row_id)
    if subject_omeka_item == None:
        return None

    for k,v in update_rules.items():
        subject_values = util.replace_value(v["subject_column"], row)
        subject_values = [subject_values] if isinstance(subject_values, str) else subject_values
        object_omeka_item = check_object_table(args_conf, tables_path, v["object_table"], v["object_column"], subject_values)
        if object_omeka_item != None:
            with open(c.PROPERTIES_INDEX,"r") as items_index_file:
                properties_index = json.load(items_index_file)
                subject_prop = properties_index[k]
                res_json = subject_omeka_item[1]
                res_json[k] = []
                res_json[k].append(build_relation_json(subject_omeka_item, object_omeka_item, subject_prop, args_conf))
                return res_json
    return None

def build_relation_json(subject_omeka_item, object_omeka_item, subject_prop, args_conf):
    return {
        "type": "resource:item",
        "value_resource_name": "items",
        "value_resource_id": object_omeka_item[0],
        "@id": str(args_conf["omeka_api_url"])+"/items/"+str(object_omeka_item[0]),
        "property_id": subject_prop["id"],
        "property_label": subject_prop["label"]
    }

def find_item_from_row_id(row_id):
    with open(c.ITEMS_INDEX,"r") as items_index_file:
        all_items = json.load(items_index_file)
        for item in all_items:
            for v_id in row_id[2]:
                for a_part in item[row_id[0]]:
                    if(a_part[row_id[1]] == v_id):
                        return (item["o:id"],item)
    return None

def check_object_table(args_conf, tables_path, object_table, object_column, subject_values):
    with open(str(tables_path)+str(object_table)) as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        row_num = 1
        for row in reader:
            object_values = util.replace_value(object_column,row)
            object_values = [object_values] if isinstance(object_values, str) else object_values
            for v in object_values:
                if v in subject_values:
                    object_table_args = util.get_table_conf_by_file(args_conf, object_table)
                    row["INTERNAL:ROWID"] = str(object_table)+"::"+str(row_num)
                    object_row_id = create.generate_row_id(row, object_table_args, args_conf)
                    return find_item_from_row_id(object_row_id)
            row_num += 1
    return None
