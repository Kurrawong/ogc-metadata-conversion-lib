# Mapping Documentation
The mappings used between the converted formats will be documented here for transparency & review.

The mappings are defined in the Python files in this directory:
- ISO19115-3 XML - [`ISO3toISO4.py`](./ISO3toISO4.py)
- UMM-G JSON - [`UMMtoISO4.py`](./UMMtoISO4.py)
- TrainingDML-AI JSON - [`TrainingDMLtoISO4.py`](./TrainingDMLtoISO4.py)

> [!NOTE]  
> `@` denotes an array in the property path. You can have multiple nested arrays by using multiple `@` flags, however the number of nested arrays must match between the source & target paths.

## ISO19115-3 XML to ISO19115-4 JSON

Source Path| Target Path                                 |Notes
-|---------------------------------------------|-
`mdb:metadataIdentifier.mcc:MD_Identifier.mcc:code.gco:CharacterString`| `id` & `properties.metadataIdentifier.code` |
`mdb:dataQualityInfo.mdq:DQ_DataQuality@.mdq:scope.mcc:MD_Scope.mcc:level.mcc:MD_ScopeCode.#text`| `properties.dataQualityInfo@.scope.level`   |
`mdb:dataQualityInfo.mdq:DQ_DataQuality@.mdq:report`| `properties.dataQualityInfo@.report`        |Post-processing function
`mdb:dateInfo`| `properties.dateInfo`                       |Post-processing function

## UMM-G JSON to ISO19115-4 JSON

Source Path|Target Path|Notes
-|-|-
`GranuleUR`|`id` & `properties.metadataIdentifier.code`|
`MeasuredParameters`|`properties.dataQualityInfo`|Post-processing function
`ProviderDates`|`properties.identificationInfo.citation`|Post-processing function

## TrainingDML-AI JSON to ISO19115-4 JSON

Source Path|Target Path|Notes
-|-|-
`id`|`id` & `properties.metadataIdentifier.code`|
`quality`|`properties.dataQualityInfo`|
