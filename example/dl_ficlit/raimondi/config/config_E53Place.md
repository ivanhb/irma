#E53Place.tsv

## Meta
"resource_template":"E53Place",
"resource_class":"crm:E53_Place",
"item_set":"Raimondi(sample)",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]
"owl:sameAs":[{"@id":"geonames","type":"uri"}]
"owl:sameAs":[{"@id":"wikidata","type":"uri"}]

## Update
"crm:P89_falls_within" --> "place" && "E53Place.tsv" && E53Place_id
"crm:P76_has_contact_point" --> "address" && "E45Address.tsv" && E45Address_id