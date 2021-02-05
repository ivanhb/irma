#E21Person.tsv

## Meta
"resource_template":"E21Person",
"resource_class":"crm:E21_Person",
"item_set":"Raimondi(sample)",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]
"owl:sameAs":[{"@id":"viaf","type":"uri"}]
"owl:sameAs":[{"@id":"worldcat","type":"uri"}]
"owl:sameAs":[{"@id":"wikidata","type":"uri"}]

## Update
<!---
properties with multiple values, separated by ' ;; '
-->
"pro:holdsRoleInTime" --> "rit_rdq" && "RoleInTime.tsv" && RoleInTime_id
"crm:P67i_is_referred_to_by" --> "referred_to_by" && "F2Expression.tsv" && F2Expression_id