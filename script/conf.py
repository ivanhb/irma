#----------
#-- INDEXES
#----------

# The structure of each saved index
INDEXES = {
    "resource_classes": {"<KEY>":"o:term", "id":"o:id", "label":"o:label"},
    "properties": {"<KEY>":"o:term","id":"o:id", "label":"o:label"},
    "resource_templates": {"<KEY>":"o:label","id":"o:id", "label":"o:label", "template":"o:resource_template_property"},
    "item_sets": {"<KEY>":"o:title","id":"o:id", "label":"o:title"}
}

# The path of each file saved locally
INDEX_DATA_PATH = "data/.index/"
ITEMS_INDEX = INDEX_DATA_PATH + "created_items.json"
RESOURCE_TEMPLATES_INDEX = INDEX_DATA_PATH + "resource_templates_index.json"
RESOURCE_CLASSES_INDEX = INDEX_DATA_PATH + "resource_classes_index.json"
ITEM_SETS_INDEX = INDEX_DATA_PATH + "item_sets_index.json"
PROPERTIES_INDEX = INDEX_DATA_PATH + "properties_index.json"
