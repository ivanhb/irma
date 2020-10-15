import os , json , csv ,re, requests
import script.preprocessing as preprocessing

def replace_value(val,data_row):
    if '-->' in val:
        vocab = None
        column = val.split('-->',1)[1] # get column name
        if ';' in column:
            column,vocab = column.split(';',1)

        funct = val.split('-->',1)[0].replace("op:","") # call the function specified in preprocessing
        if funct == "create_name":
            value = "data_row,'"+column+"'"
        else:
            value = data_row[column]

        if vocab is not None:
            new_val = eval('preprocessing.'+funct+'("'+str(value).strip()+'","'+vocab.strip()+'")')
        else:
            if funct == "create_name":
                new_val = eval('preprocessing.'+funct+'('+value+')')
            else:
                value = json.dumps(value) if (value is not None and len(value) != 0) else "''"
                new_val = eval('preprocessing.'+funct+'('+value+')')  # replace the final json

    if '-->' not in val:
        new_val = data_row[val]
    return new_val

def get_from_omeka(api_url, api_opr, curr_page=1, curr_data=[]):
    response = requests.get(api_url+"/"+api_opr+"?page="+str(curr_page), verify=False)
    if response.status_code == 200:
        l_elems = json.loads(response.text)
        if len(l_elems) == 0:
            return curr_data
        else:
            return get_from_omeka(api_url, api_opr, curr_page+1, curr_data + l_elems)
    else:
        return curr_data

# Get a table family having a <filename> in it
def get_table_conf_by_file(args_conf, filename):
    for a_tab in args_conf["tables"]:
        if filename in a_tab["files"]:
            return a_tab
    return None
