#E19PhysicalObject.tsv

## Meta
"resource_template":"E19PhysicalObject",
"resource_class":"crm:E19_Physical_Object",
"item_set":"Raimondi(sample)",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]
"crm:P3_has_note":[{“@value":"archival_note","type":"literal"}]

## Update
"crm:P128_carries" --> "expression" && "F2Expression.tsv" && F2Expression_id
"crm:P2_has_type" --> "type" && "E55Type.tsv" && E55Type_id
"crm:P43_has_dimension" --> "height" && "E54Dimension.tsv" && E54Dimension_id
"crm:P43_has_dimension" --> "extent" && "E54Dimension.tsv" && E54Dimension_id
"crm:P1_is_identified_by" --> "inventory_number" && "E42Identifier.tsv" && E42Identifier_id
"crm:P1_is_identified_by" --> "shelfmark" && "E42Identifier.tsv" && E42Identifier_id
"crm:P46i_forms_part_of" --> "archival_unit" && "E19PhysicalObject.tsv" && E19PhysicalObject_id
"seq:follows" --> "preceding_item" && "E19PhysicalObject.tsv" && E19PhysicalObject_id
"crm:P52_has_current_owner" --> "owner" && "E40LegalBody.tsv" && E40LegalBody_id
"crm:P50_has_current_keeper" --> "keeper" && "E40LegalBody.tsv" && E40LegalBody_id
"crm:P55_has_current_location" --> "location" && "E53Place.tsv" && E53Place_id
"crm:P104_is_subject_to" --> "right" && "E30Right.tsv" && E30Right_id