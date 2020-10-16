from argparse import ArgumentParser
import requests , json , os , sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from collections import defaultdict, Counter

import script.main as m
import script.conf as c

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
REQ_SESSION = requests.Session()
retries = Retry(total=10, backoff_factor=1, status_forcelist=[ 502, 503, 504, 524 ])
REQ_SESSION.mount('http://', HTTPAdapter(max_retries=retries))
REQ_SESSION.mount('https://', HTTPAdapter(max_retries=retries))

########################
############ Things to do manually
########################

# 1. upload ontologies
# 2. upload custom controlled vocabularies: use the same names as in vocabularies.json
# 3. create the itemset/s, add the itemset in the "item_sets_ids.json"
# 3. copy the ids of vocabularies in vocabularies.json and substitute IDs in "templates" folder
# 5. upload templates where vocabularies are already selected (import in next instances -- control vocab ids match with correct number)
# 6. create the item_set/s if not yet in Omeka

if __name__ == "__main__":
    arg_parser = ArgumentParser("run.py", description="Upload into an OmekaS Digital Library a collection of items taken from a .TSV tabular dataset")
    arg_parser.add_argument("-conf", "--configuration", required=True, dest="conf", help="Specify the configuration file (JSON format)")
    arg_parser.add_argument("-tabs", "--tables", dest="tables", required=True, help="Specify the directory containing the tabular datasets (TSV format).\nNote: each file must contain items of the same class.")
    arg_parser.add_argument("-i", "--items", dest="items", action="store_true", required=False, help="Import the items into OmekaS")
    arg_parser.add_argument("-m", "--media", dest="media", action="store_true", required=False, help="Import the media files into OmekaS")
    #arg_parser.add_argument("-d", "--def", dest="base_def", default=False, action="store_true", help="Get the 'resource_classes', 'properties', and 'resource_templates'")

    args = arg_parser.parse_args()

    ## -------
    ## Args Conf and definitions
    ## -------
    args_conf = None
    with open(args.conf) as json_file:
        args_conf = json.load(json_file)
        params = {
            'key_identity': args_conf["key_identity"],
            'key_credential': args_conf["key_credential"]
        }

    def update_omeka(all_data, print_on_file = False):
        data_to_print = []
        if len(all_data)>0:
            for item_num, payload in enumerate(all_data):
                response = REQ_SESSION.post('{}/items/'.format(args_conf["omeka_api_url"]), json=payload, params=params, verify=False)
                if str(response) != "<Response [200]>":
                    print(response.content)
                    print("--> ERROR: couldn't add element number:"+str(item_num + 1))
                    break
                json_data = json.loads(response.content)
                data_to_print.append(json_data)
                sys.stdout.write('\r--> %d/%d items uploaded on Omeka' %(item_num + 1,len(all_data)))
                sys.stdout.flush()
            if print_on_file:
                #print("--> print on file (i.e. 'created_items.json')")
                m.backup_items(data_to_print)
            print("")

    def connect_omeka_items(updated_data):
        if len(updated_data)>0:
            for item_num, update_payload in enumerate(updated_data):
                # upload
                resp = REQ_SESSION.put('{}/items/{}'.format(args_conf["omeka_api_url"],update_payload["o:id"]), json=update_payload, params=params, verify=False)
                sys.stdout.write('\r--> %d/%d items uploaded on Omeka' %(item_num + 1,len(updated_data)))
                sys.stdout.flush()
            print("")

    print("\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\nIrma, a tool for the automatic instantiation of an Omeka S digital archive \n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n\n",flush=True)

    ## PHASE 1) call the APIs and store into <dict_ids> the 'resource_classes','properties','resource_templates','item_sets'
    # --- e.g. dict_ids["resource_classes"] -> a dict of all the resource_classes in Omeka
    print("PRE-0) Get from Omeka the indexes (i.e. 'resource_classes', 'properties', 'item_sets', and 'resource_templates') ...", flush=True)
    omeka_ids = m.get_indexes(args_conf["omeka_api_url"])
    args_conf = m.auto_normalize_conf(args_conf)
    print("Step-0 Done \n")

    if args.items:
        print("\nCreating and Adding a Collection of Items to the Omeka-S Instance\n-----------------------------------------------------------------\n",flush=True)

        ## -------
        ## PHASE 2) CREATE/ADD items of the table
        ## -------
        print("1) Create the new items to add to Omeka ...",flush=True)
        print("-> read the tables",flush=True)
        created_data = m.read_tables(args.tables, args_conf, "create")
        print("-> add [",len(created_data), "] item/s to Omeka",flush=True)
        update_omeka(created_data, True)
        print("Step-1 Done \n")

        ## -------
        ## PHASE 3) LOOKUP
        ## -------
        print("2) Lookup into other columns of the tables and create/add new items to Omeka ...",flush=True)
        print("-> read the tables",flush=True)
        lookup_data = m.read_tables(args.tables, args_conf, "lookup")
        print("-> add [",len(lookup_data), "] item/s to Omeka",flush=True)
        update_omeka(lookup_data, True)
        print("Step-2 Done \n")

        ## -------
        ## PHASE 4) Update
        ## -------
        print("3) Update the items in Omeka by linking them together ...",flush=True)
        print("-> read the tables",flush=True)
        updated_data = m.read_tables(args.tables, args_conf, "update")
        print("-> update [",len(updated_data), "] item/s",flush=True)
        connect_omeka_items(updated_data)
        print("Step-3 Done \n")

    def update_media(all_data, print_on_file = False):
        res = defaultdict(list)
        data_to_print = []
        if len(all_data)>0:
            for item in all_data:
                # files_list = [...,(<file_title>,<file_path>,<file_json_block>),...]
                for f_num, a_file_tupla in enumerate(item["files"]):
                    files = {
                        "file":(a_file_tupla[0], open(a_file_tupla[1], 'rb'),'multipart/form-data')
                    }
                    file_data = {'data': json.dumps(a_file_tupla[2])}
                    response = REQ_SESSION.post('{}/files'.format(args_conf["omeka_api_url"]), params=params, data=file_data, files=files, verify=False)
                    if str(response) != "<Response [200]>":
                        print(response.content)
                        print("--> ERROR: couldn't add file number:"+str(f_num+1))
                        break
                    json_data = json.loads(response.content)
                    data_to_print.append(json_data)
                    sys.stdout.write('\r--> %d/%d file uploaded on Omeka' %(f_num+1,len(all_data)))
                    sys.stdout.flush()

            if print_on_file:
                #print("--> print on file (i.e. 'created_items.json')")
                m.backup_files(data_to_print)

            print("")
        return res

    if args.media:
        print("\nUploading the Media Files into the Omeka-S Instance\n-----------------------------------------------------------------\n",flush=True)

        print("1) Mapping the media files with their corresponding Omeka Items...",flush=True)
        print("-> read the tables",flush=True)
        media_data = m.read_tables(args.tables, args_conf, "media")
        print(media_data)
        update_media(media_data, True)
        print("Step-1 Done \n")
