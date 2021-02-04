import os , json , csv ,re , itertools , pprint , requests
import script.preprocessing as p
import script.util as util
import script.create as create
import script.conf as c
from langdetect import detect
from collections import defaultdict, Counter


def update_item(row, table_args, args_conf, tables_path, update_rules):

    # re-generates the id of the row and search for it in Omeka
    subject_row_id = create.generate_row_id(row, table_args, args_conf)
    subject_omeka_item = util.find_item_from_row_id(subject_row_id)
    if subject_omeka_item == None:
        return None

    # iterate over the upadting rules
    to_update = False
    res_json = subject_omeka_item[1]
    for k,v_list in update_rules.items():
        inner_list = []
        for v in v_list:
            subject_values = util.replace_value(v["subject_column"], row)
            subject_values = [subject_values] if isinstance(subject_values, str) else subject_values

            #we check the object elem
            for sub_val in subject_values:
                object_omeka_item = check_object_table(args_conf, tables_path, v["object_table"], v["object_column"], sub_val)
                if object_omeka_item != None:
                    with open(c.PROPERTIES_INDEX,"r") as items_index_file:
                        properties_index = json.load(items_index_file)
                        subject_prop = properties_index[k]
                        if k not in res_json:
                            res_json[k] = []
                        res_json[k].append(build_relation_json(subject_omeka_item, object_omeka_item, subject_prop, args_conf))
                        to_update = True

            #print(res_json)

    return (to_update,res_json)

def build_relation_json(subject_omeka_item, object_omeka_item, subject_prop, args_conf):
    return {
        "type": "resource:item",
        "value_resource_name": "items",
        "value_resource_id": object_omeka_item[0],
        "@id": str(args_conf["omeka_api_url"])+"/items/"+str(object_omeka_item[0]),
        "property_id": subject_prop["id"],
        "property_label": subject_prop["label"]
    }

def check_object_table(args_conf, tables_path, object_table, object_column, sub_val):
    with open(str(tables_path)+str(object_table)) as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        row_num = 1
        for row in reader:
            object_values = util.replace_value(object_column,row)
            object_values = [object_values] if isinstance(object_values, str) else object_values
            for v in object_values:
                if v == sub_val:
                    object_table_args = util.get_table_conf_by_file(args_conf, object_table)
                    row["INTERNAL:ROWID"] = str(object_table)+"::"+str(row_num)
                    object_row_id = create.generate_row_id(row, object_table_args, args_conf)
                    return util.find_item_from_row_id(object_row_id)
            row_num += 1
    return None
