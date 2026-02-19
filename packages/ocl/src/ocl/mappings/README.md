# Mapping Documentation
The mappings used between the converted formats will be documented here for transparency & review.

The mappings are defined in the Python files in this directory:
- ISO 19115-3 XML - [`ISO3toISO4.py`](./ISO3toISO4.py)
- UMM JSON - [`UMMtoISO4.py`](./UMMtoISO4.py)
- TrainingDML-AI JSON - [`TrainingDMLtoISO4.py`](./TrainingDMLtoISO4.py)

> [!NOTE]  
> `@` denotes an array in the property path. You can have multiple nested arrays by using multiple `@` flags, however the number of nested arrays must match between the source & target paths.

## ISO19115-3 XML to ISO19115-4 JSON

| Source Path                                                             | Target Path                                 | Notes                    |
|-------------------------------------------------------------------------|---------------------------------------------|--------------------------|
| `mdb:metadataIdentifier.mcc:MD_Identifier.mcc:code.gco:CharacterString` | `id` & `properties.metadataIdentifier.code` |                          |
| `mdb:metadataIdentifier.mcc:MD_Identifier`                              | `properties.metadataIdentifier`             | Post-processing function |
| `mdb:dataQualityInfo`                                                   | `properties.dataQualityInfo`                | Post-processing function |
| `mdb:dateInfo`                                                          | `properties.dateInfo`                       | Post-processing function |
| `mdb:identificationInfo.mri:MD_DataIdentification`                      | `properties.identificationInfo`             | Post-processing function |
| `mdb:identificationInfo.mri:MD_DataIdentification.mri:extent`           | `geometry` & `bbox`                         | Post-processing function |
| `mdb:defaultLocale.lan:PT_Locale`                                       | `properties.defaultLocale`                  | Post-processing function |
| `mdb:otherLocale`                                                       | `properties.otherLocale`                    | Post-processing function |
| `mdb:metadataScope`                                                     | `properties.metadataScope`                  | Post-processing function |
| `mdb:contact`                                                           | `properties.contact`                        | Post-processing function |
| `mdb:resourceLineage`                                                   | `properties.resourceLineage`                | Post-processing function |

## UMM-G JSON to ISO19115-4 JSON

| Source Path                                                         | Target Path                                 | Notes                    |
|---------------------------------------------------------------------|---------------------------------------------|--------------------------|
| `GranuleUR`                                                         | `id` & `properties.metadataIdentifier.code` |                          |
| `DataQuality`                                                       | `properties.dataQualityInfo`                |                          |
| `ProviderDates`                                                     | `properties.identificationInfo.citation`    | Post-processing function |
| `SpatialExtent`                                                     | `properties.identificationInfo.extent`      | Post-processing function |
| `SpatialExtent.HorizontalSpatialDomain.Geometry.BoundingRectangles` | `geometry` & `bbox`                         | Post-processing function |

## TrainingDML-AI JSON to ISO19115-4 JSON

| Source Path | Target Path                                                   | Notes                    |
|-------------|---------------------------------------------------------------|--------------------------|
| `id`        | `id` & `properties.metadataIdentifier.code`                   |                          |
| `quality`   | `properties.dataQualityInfo`                                  |                          |
| `extent`    | `geometry` & `bbox` &  `properties.identificationInfo.extent` | Post-processing function |
