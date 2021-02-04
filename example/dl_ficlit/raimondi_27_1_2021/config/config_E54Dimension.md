#E54Dimension.tsv

## Meta
"resource_template":"E54Dimension",
"resource_class":"crm:E54_Dimension",
"item_set":"Fondo Giuseppe Raimondi",
"item_id": "dcterms:identifier"

## Create
"dcterms:identifier":[{"@id":"permalink","type":"uri"}]
"rdfs:label”:[
{"@value":"label_it","type":"literal", "@language":"it"},
{"@value":"label_en","type":"literal", "@language":"en"}
]
"skos:closeMatch":[{"@id":"close_match","type":"uri"}]
"skos:relatedMatch":[{"@id":"related_match","type":"uri"}]
"crm:P90_value”:[{"@value":"value","type":"xsd:decimal"}]

## Update
"crm:P91_has_unit" --> "unit" && "E58MeasurementUnit.tsv" && E58MeasurementUnit_id