import os , json , csv ,re , itertools , pprint , requests
from langdetect import detect
from collections import defaultdict, Counter

import script.conf as c
import script.util as util
import script.create as create
import script.lookup as lookup
import script.update as update
import script.media as media

pp = pprint.PrettyPrinter(indent=4)

# Get a table family having a specific <id>
def get_table_conf_by_id(args_conf, id):
    for a_tab in args_conf["tables"]:
        if a_tab["id"] == id:
            return a_tab
    return None

# Finds and returns the entries of: res_class, res_template, item_set
def map_to_entity(entity_index, args_conf):

    #Find the itemset
    with open(c.ITEM_SETS_INDEX,"r") as items_index_file:
        all_items = json.load(items_index_file)
        item_set = all_items[entity_index["item_set"]] if entity_index["item_set"] in all_items else None
        if item_set == None and "item_set" in args_conf:
            if entity_index["item_set"] in args_conf["item_set"]:
                item_set = args_conf["item_set"][entity_index["item_set"]]

    #Find the resource_class
    with open(c.RESOURCE_CLASSES_INDEX,"r") as items_index_file:
        all_items = json.load(items_index_file)
        resource_class = all_items[entity_index["resource_class"]] if entity_index["resource_class"] in all_items else None

    #Find the resource_template
    with open(c.RESOURCE_TEMPLATES_INDEX,"r") as items_index_file:
        all_items = json.load(items_index_file)
        resource_template = all_items[entity_index["resource_template"]] if entity_index["resource_template"] in all_items else None

    #Return all the entries
    return item_set,resource_class,resource_template

# Do some automatic operations to normalize the configuration file
def auto_normalize_conf(args_conf):
    for a_table_fam in args_conf["tables"]:
        if "item_id" not in a_table_fam or a_table_fam["item_id"] == None:
            if "dcterms:identifier" not in a_table_fam["create"]:
                a_table_fam["create"]["dcterms:identifier"] = [{ "@value": "op:gen_id", "type":"literal"}]
            a_table_fam["item_id"] = "dcterms:identifier"
    return args_conf

# Get the indexes ('resource_classes','properties','resource_templates',and 'item_sets') of OmekaS
def get_indexes(api_url,lookup = ['resource_classes','properties','resource_templates','item_sets']):
    res = {}
    for api_opr in lookup:
        if api_opr in c.INDEXES:

            res[api_opr] = {}
            f_name = c.INDEX_DATA_PATH+api_opr+"_index"+".json"

            elems_dict = {}
            l_elems = util.get_from_omeka(api_url,api_opr)

            ##iterate over all elems
            for elem in l_elems:
                inner_block = {}
                for k,val in c.INDEXES[api_opr].items():
                    if k != "<KEY>":
                        inner_block[k] = elem[val]
                elem_key = elem[c.INDEXES[api_opr]["<KEY>"]]
                elems_dict[elem_key]= inner_block

        #the json file is empty in case of an error with the request
        res[api_opr] = elems_dict
        d=open(f_name,'w')
        d.write(json.dumps(elems_dict))
        d.close()

    return res

# Backup all the items
def backup_items(d, api_url=None, online=False):
    if online:
        d = util.get_from_omeka(api_url,"items")
    #in case there is other items then append the given items (i.e. <d>) to the current items
    if os.path.exists(c.ITEMS_INDEX):
        with open(c.ITEMS_INDEX,"r") as created_items_file:
            created_items = json.load(created_items_file)
            d = d + created_items
    #print all to the file
    with open(c.ITEMS_INDEX,"w") as items_index_file:
        items_index_file.write(json.dumps(d))
    items_index_file.close()

# Backup all the items
def backup_files(d, api_url=None, online=False):
    #in case there is other items then append the given items (i.e. <d>) to the current items
    if os.path.exists(c.FILES_INDEX):
        with open(c.FILES_INDEX,"r") as created_items_file:
            created_items = json.load(created_items_file)
            d = d + created_items
    #print all to the file
    with open(c.FILES_INDEX,"w") as items_index_file:
        items_index_file.write(json.dumps(d))
    items_index_file.close()

# Read all the tables (in TSV format) inside a specified directory (i.e. <tables_path>) and apply an operation (i.e. <operation>).
# this methods needs also the configurations (i.e. <args_conf>) provided by the user
def read_tables(tables_path, args_conf, operation="create"):

    list_items = []
    for filename in os.listdir(tables_path):
        table_args = util.get_table_conf_by_file(args_conf, filename)
        if filename.endswith(".tsv") and table_args != None:
            item_set,resource_class,resource_template = map_to_entity(table_args, args_conf)
            # if it is a lookup operation then make sure this table have this option defined in its configuration
            # OR if this table has no entries move to the next table
            if operation not in table_args or item_set == None or resource_class == None or resource_template == None:
                continue

            #Process the items of the TSV table
            with open(str(tables_path)+filename) as tsv_file:
                reader = csv.DictReader(tsv_file, delimiter='\t')
                row_num = 1
                for row in reader:
                    row["INTERNAL:ROWID"] = str(filename)+"::"+str(row_num)
                    if operation == 'create' and 'create' in table_args:
                        create.init_created_items_index()
                        o_item = create.create_item(row, args_conf, table_args["create"], item_set, resource_class, resource_template)
                        list_items.append(o_item)

                    if operation == 'lookup' and 'lookup' in table_args:
                        #list_lookup_items = lookup_item(list_items,row,entity,resource_templates_ids, property_ids, classes_ids, vocabularies_ids)
                        list_lookup_items = lookup.lookup_item(row, args_conf, table_args["lookup"], list_items)
                        for index, item in enumerate(list_lookup_items):
                            row["INTERNAL:ROWID"] = str(filename)+"::"+str(row_num)+"."+str(index)
                            list_items.append(item)

                    if operation == 'update' and 'update' in table_args:
                        updated_item = update.update_item(row, table_args, args_conf, tables_path, table_args["update"])
                        if updated_item[0]:
                            list_items.append(updated_item[1])

                    if operation == 'media' and 'media' in table_args:
                        media.init_created_files_index()
                        tab_list_index = table_args['files'].index(filename)
                        # Check if the script should handle the media files
                        item_media = media.import_media(row, row_num, args_conf, table_args, tables_path + table_args['media'][tab_list_index])
                        if item_media != None:
                            list_items.append(item_media)

                    row_num += 1

        #print(filename," :",len(list_items))

    return list_items
