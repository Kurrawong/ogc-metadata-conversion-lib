from ocl.mapping import MappingDict
from ocl.models.umm import UMM
from ocl.models.iso4 import ISO4


def process_provider_dates(provider_dates: list) -> dict | None:
    obj = {}
    for date in provider_dates:
        match (date["Type"]):
            case "Create":
                obj["creation"] = date["Date"]
            case "Insert":
                obj["insertion"] = date["Date"]
            case "Update":
                obj["revision"] = date["Date"]
            case "Delete":
                obj["deletion"] = date["Date"]
    if len(obj.keys()) == 0:
        return None
    return obj


def bbox(obj: list | None) -> list[float] | None:
    if obj is None or len(obj) == 0:
        return None

    return [
        obj[0]["WestBoundingCoordinate"],
        obj[0]["SouthBoundingCoordinate"],
        obj[0]["EastBoundingCoordinate"],
        obj[0]["NorthBoundingCoordinate"],
    ]


def geometry(obj: list | None) -> dict | None:
    box = bbox(obj)
    if box is None:
        return None

    coords = [[
        [box[0], box[1]],
        [box[2], box[1]],
        [box[2], box[3]],
        [box[0], box[3]],
        [box[0], box[1]],
    ]]

    return {
        "type": "Polygon",
        "coordinates": coords,
    }


def extent(obj: dict | None) -> list | None:
    if obj is None:
        return None

    extent_obj = {"geographicElement": []}

    if "SpatialCoverageType" in obj:
        extent_obj["description"] = "SpatialCoverageType=" + obj["SpatialCoverageType"]

    if "HorizontalSpatialDomain" in obj:
        if "Geometry" in obj["HorizontalSpatialDomain"]:
            if "BoundingRectangles" in obj["HorizontalSpatialDomain"]["Geometry"]:
                for rectangle in obj["HorizontalSpatialDomain"]["Geometry"]["BoundingRectangles"]:
                    extent_obj["geographicElement"].append({
                        "type": "EX_GeographicBoundingBox",
                        "westBoundLongitude": rectangle["WestBoundingCoordinate"],
                        "eastBoundLongitude": rectangle["EastBoundingCoordinate"],
                        "southBoundLatitude": rectangle["SouthBoundingCoordinate"],
                        "northBoundLatitude": rectangle["NorthBoundingCoordinate"],
                    })

    return [extent_obj]


umm_to_iso4_mapping: MappingDict = {
    "source_model": UMM,
    "target_model": ISO4,
    "mappings": [
        {
            "key": "GranuleUR",
            "to": "id",
        },
        {
            "key": "GranuleUR",
            "to": "properties.metadataIdentifier.code",
        },
        {
            "key": "DataQuality",
            "to": "properties.dataQualityInfo",
        },
        {
            "key": "ProviderDates",
            "to": "properties.identificationInfo.citation",
            "to_func": lambda value, source: process_provider_dates(value)
        },
        {
            "key": "SpatialExtent.HorizontalSpatialDomain.Geometry.BoundingRectangles",
            "to": "bbox",
            "to_func": lambda value, source: bbox(value)
        },
        {
            "key": "SpatialExtent.HorizontalSpatialDomain.Geometry.BoundingRectangles",
            "to": "geometry",
            "to_func": lambda value, source: geometry(value)
        },
        {
            "key": "SpatialExtent",
            "to": "properties.identificationInfo.extent",
            "to_func": lambda value, source: extent(value)
        },
    ],
}