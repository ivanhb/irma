import os , json , csv ,re , itertools , pprint , requests
import script.preprocessing as p
import script.util as util
import script.conf as c
from langdetect import detect
from collections import defaultdict, Counter


#def lookup_item(list_lookup_items,data_row,item_type,resource_templates_ids, property_ids, classes_ids, vocabularies_ids):
#lookup_item(row, args_conf, item_set, resource_class, resource_template)
def lookup_item(row, args_conf, lookup_rules, processed_items = []):

    new_items = []
    for k,v in lookup_rules.items():

        #<k>: operation and Column name
        lookup_prop_vals = util.replace_value(k, row) if isinstance(util.replace_value(k, row),list) else [util.replace_value(k, row)]
        for part_v in lookup_prop_vals:
            # -----
            # Check and Add (in case)
            # -----
            # 1) First check all the items that are already in Omeka
            with open(c.ITEMS_INDEX) as items_file:
                items = json.load(items_file)
            item_id_index = get_item_id(v["att_check"], part_v, items, v["resource_template"])
            # 2) Check if item has been already added during the process
            item_id_lookup = get_item_id(v["att_check"], part_v, processed_items, v["resource_template"])
            # 3) add it in case item does not exist in <items> and <processed_items>
            if item_id_index == None and item_id_lookup == None:

                dest_table_conf = get_table_conf_by_id(args_conf, v["table"])
                new_row = gen_table_row(args_conf, dest_table_conf, v["row_values"], row)
                dest_item_set, dest_resource_class, dest_resource_template = map_to_entity(dest_table_conf, args_conf)
                o_item = create_item(new_row, args_conf, dest_item_set, dest_resource_class, dest_resource_template)
                new_items.append(o_item)

    return new_items

# checks if any item in <items> with resouce_template = <template_id> has a property <prop_k> == <prop_v>
def get_item_id(prop_k, val, items, resource_template_name):
    with open(c.RESOURCE_TEMPLATES_INDEX) as items_file:
        rsc_temp_items = json.load(items_file)
    template_id = rsc_temp_items[resource_template_name]
    for i_item in range(0,len(items)):
        item = items[i_item]
        if "o:resource_template" in item:
            if "o:id" in item["o:resource_template"]:
                if item["o:resource_template"]["o:id"] == template_id:
                    if prop_k in item:
                        #check if one of the property values == <val>
                        for a_prop in item[prop_k]:
                            if a_prop["@value"] == val:
                                return i_item
    return None

## Generate a generic row of a table defined according to a <dest_table_conf>, and update some specific <vals_to_update> of the generated row following the values in <row_data>
def gen_table_row(args_conf, dest_table_conf, vals_to_update, row_data):
    a_row = {}
    for k_header in dest_table_conf["header"]:
        a_row[k_header] = dest_table_conf["header"][k_header]
        if k_header in vals_to_update:
            a_row[k_header] = row_data[vals_to_update[k_header]]
    return a_row
