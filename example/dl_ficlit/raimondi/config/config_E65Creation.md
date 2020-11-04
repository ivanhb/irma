#E65Creation.tsv

## Meta
"resource_template":"E65Creation",
"resource_class":"crm:E65_Creation",
"item_set":"Raimondi(sample)",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]

## Update
"crm:P32_used_general_technique" --> "production_technique" && "E55Type.tsv" && E55Type_id
"crm:P14_carried_out_by" --> "agent" && "E21Person.tsv" && E21Person_id
"crm:P4_has_time-span" --> "time_span" && "E52TimeSpan.tsv" && E52TimeSpan_id
 