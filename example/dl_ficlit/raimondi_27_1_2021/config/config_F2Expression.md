#F2Expression.tsv

## Meta
"resource_template":"F2Expression",
"resource_class":"frbrooconfig_R:F2_Expression",
"item_set":"Raimondi(sample)",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]
"bf:preferredCitation":[{“@value":"cite_as","type":"literal"}]
"crm:P72_has_language":[{"@id":"language","type":"uri"}]
"dcterms:bibliographicCitation":[{“@value":"biblCitation","type":"literal"}]


## Update
"crm:P2_has_type" --> "type" && "E55Type.tsv" && E55Type_id
"crm:P94i_was_created_by" --> "creation_event" && "F28ExpressionCreation.tsv" && F28ExpressionCreation_id
"crm:P102_has_title" --> "title" && "E35Title.tsv" && E35Title_id
"crm:P104_is_subject_to" --> "right" && "E30Right.tsv" && E30Right_id
"crm:P128i_is_carried_by" --> "physical_carrier" && "E19PhysicalObject.tsv" && E19PhysicalObject_id

<!---
properties with multiple values, separated by ' ;; '
-->
"crm:P67_refers_to" --> "referenced_entity" && "E21Person.tsv" && E21Person_id

