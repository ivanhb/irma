import os , json , csv ,re , itertools , pprint , requests
import script.preprocessing as p
import script.util as util
import script.create as create
import script.conf as c
from collections import defaultdict, Counter

def import_media(row, row_num, args_conf, table_args, media_dir):
    list_media = []
    subdirs_list = [x[0] for x in os.walk(media_dir)]
    if media_dir+"/"+str(row_num) not in subdirs_list:
        return None
    else:
        #handle_row_media(row, media_dir+"/"+row_media_dir, row_media_dir)
        for media_filename in sorted(os.listdir(media_dir+"/"+str(row_num))):
            if media_filename.endswith(".jpg"):
                list_media.append((media_filename,media_dir+"/"+str(row_num)+"/"+media_filename))

    row_id = create.generate_row_id(row, table_args, args_conf)
    omeka_item = util.find_item_from_row_id(row_id)

    return prepare_jsons(omeka_item[0], list_media)

# returns a dict such that each key is an item_id and the value is a list of all its corresponding files
# each element of the list is represented as a tupla (<file_title>,<file_path>,<file_json_block>)
# Sample = 'data={"o:ingester": "upload", "file_index": "0", "o:item": {"o:id": 888}}'
def prepare_jsons(item_id, list_media):
    res_list_jsons = []
    with open(c.PROPERTIES_INDEX,"r") as items_index_file:
        properties_index = json.load(items_index_file)
    for order_in_list,a_media in enumerate(list_media):
        media_json = {
            "o:ingester": "upload",
            "file_index": "0",
            "o:item": {"o:id": item_id}
        }
        res_list_jsons.append((a_media[0],a_media[1],media_json))

    return {"item_id": item_id, "files":res_list_jsons}


def init_created_files_index():
    #init also the created_items.json index
    with open(c.FILES_INDEX,"w") as items_index_file:
        items_index_file.write(json.dumps([]))
