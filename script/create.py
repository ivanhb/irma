import os , json , csv ,re , itertools , pprint , requests
import script.util as util
import script.conf as c
import copy
from langdetect import detect
from collections import defaultdict, Counter

pp = pprint.PrettyPrinter(indent=4)

# This function takes: row, item_set, resource_class, resource_template
def create_item(row, args_conf, creation_rules, item_set, resource_class, resource_template):
    # The basic structure
    create_json = {
                "@type":["o:Item"],
                "o:resource_class": {
                    "o:id": resource_class["id"],
                    '@id': '{}/resource_class/{}'.format(args_conf["omeka_api_url"], resource_class["id"])
                },
                "o:item_set": [{"o:id": item_set["id"]}],
                "o:resource_template": {
                    "o:id": resource_template["id"],
                    '@id': '{}/resource_templates/{}'.format(args_conf["omeka_api_url"], resource_template["id"])
                }
            }
    # Prepare the data block
    data = prepare_json(row, creation_rules, args_conf["custom_vocabularies"])
    #Push everythong in a single JSON block and return it
    for k,v in data.items():
        create_json[k] = v
    return create_json

def prepare_json(data_row, creation_rules, vocabularies_index):
    # Get the properties index
    with open(c.PROPERTIES_INDEX,"r") as items_index_file:
        properties_index = json.load(items_index_file)
    #Elaborate and prepare the data-block
    data = fill_json(data_row, creation_rules, vocabularies_index)
    data = clean_dict(data)
    data = pop_empty(data)
    data = detect_lang(data)
    data = change_prop_id(data, properties_index)
    return data

def fill_json(data_row, mapping_rules, vocabularies_index=None):
    #item_data = {k:v for k,v in mapping_rules.items()}
    item_data = copy.deepcopy(mapping_rules)
    for prop, values_list in item_data.items():
        for value_dict in values_list:
            object = "@value" if "@value" in value_dict else "@id"
            # Note for future me: "op:" has always to be in the mapping, even if it's just for stripping
            if "op:" in value_dict[object]:
                # Generate identifier
                if "gen_id" in value_dict[object]:
                    value_dict[object] = data_row["INTERNAL:ROWID"]
                else:
                    # pre-processing operations
                    if "split_values" in value_dict[object]:
                        values = util.replace_value(value_dict[object],data_row)
                        if isinstance(values, str):
                            value_dict[object] = values
                        elif isinstance(values, list) and len(values) >= 1:
                            count_prop = 0
                            for value in values:
                                count_prop += 1
                                new_dict = {}
                                # if "property_id" in value_dict:
                                #     new_dict["property_id"] = count_prop
                                new_dict[object] = value
                                if "type" in value_dict:
                                    new_dict["type"] = value_dict["type"]
                                if value_dict["type"] == "literal":
                                    if "@language" in value_dict:
                                        new_dict["@language"] = value_dict["@language"]
                                values_list.append(new_dict)
                    else:
                        if "customvocab" in value_dict["type"]:
                            vocab = value_dict["type"].split(":")[1]
                            value_dict["type"] = "customvocab:"+str(vocabularies_index[vocab]["id"])

                        replace_res = util.replace_value(value_dict[object],data_row)

                        if type(replace_res) == tuple:
                            for o_item in replace_res[1]:
                                value_dict[o_item[0]] = o_item[1]
                            replace_res = replace_res[0]

                        value_dict[object] = replace_res

    return item_data

def clean_dict(item_data):
    new_dict = defaultdict(list)
    for prop, values_list in item_data.items():
        for value_dict in values_list:
            object = "@value" if "@value" in value_dict.keys() else "@id"
            if "op:" in value_dict[object] \
                or value_dict[object] is None \
                or len(value_dict[object].strip()) == 0 \
                or value_dict[object] == 'None' \
                or value_dict[object] == "''":
                #values_list.remove(value_dict)
                pass
            else:
                new_dict[prop].append(value_dict)
    clean_dict = dict(new_dict)
    return clean_dict

def pop_empty(item_data):
    item_data = { k : v for k,v in item_data.items() if v}
    return item_data

def detect_lang(item_data):
    for prop, values_list in item_data.items():
        for value_dict in values_list:
            if "@language" in value_dict and value_dict["@language"] == "detect":
                try:
                    lang = detect(value_dict["@value"])
                    lang = "ar" if lang == 'ar' else "en"
                    value_dict["@language"] = lang
                except:
                    value_dict.pop("@language", None)
    return item_data

def change_prop_id(item_data, properties_index):
    for prop, values_list in item_data.items():
        for dictionary in values_list:
            dictionary["property_id"] = properties_index[prop]["id"]
    return item_data

def generate_row_id(row, table_args, args_conf):
    data = prepare_json(row, table_args["create"], args_conf["custom_vocabularies"])
    res_list = []
    for a_part in data[table_args["item_id"]]:
        object = "@value" if "@value" in a_part.keys() else "@id"
        res_list.append(a_part[object])
    return (table_args["item_id"],object,res_list)
