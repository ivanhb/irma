#F28ExpressionCreation.tsv

## Meta
"resource_template":"F28ExpressionCreation",
"resource_class":"frbroo:F28_Expression_Creation",
"item_set":"Fondo Giuseppe Raimondi",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]

## Update
"frbroo:R17_created" --> "expression" && "F2Expression.tsv" && F2Expression_id
"frbroo:R18_created" --> "object" && "E19PhysicalObject.tsv" && E19PhysicalObject_id
"crm:P32_used_general_technique" --> "production_technique" && "E55Type.tsv" && E55Type_id
"crm:P14_carried_out_by" --> "agent" && "E21Person.tsv" && E21Person_id
"crm:P4_has_time-span" --> "time_span" && "E52TimeSpan.tsv" && E52TimeSpan_id
 