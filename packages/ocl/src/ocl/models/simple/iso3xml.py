from pydantic_xml import BaseXmlModel, element

from ocl.models.simple.iso4 import ISO4


class Code(
    BaseXmlModel,
    tag='code',
    ns='mcc',
    nsmap={
        "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
        "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",
    },
):
    CharacterString: str = element(tag="CharacterString", ns="gco")


class MDIdentifier(
    BaseXmlModel,
    tag='MD_Identifier',
    ns='mcc',
    nsmap={
        "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
    },
):
    code: Code


class MetadataIdentifier(
    BaseXmlModel,
    tag='metadataIdentifier',
    ns='mdb',
    nsmap={
        "mdb": "http://standards.iso.org/iso/19115/-3/mdb/1.0",
        "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
    },
):
    MD_Identifier: MDIdentifier

class ISO3(
    BaseXmlModel,
    tag='MD_Metadata',
    ns='mdb',
    nsmap={
        "mdb": "http://standards.iso.org/iso/19115/-3/mdb/1.0",
    },
):
    metadataIdentifier: MetadataIdentifier
    # title: str
    # dataQualityInfo: DataQuality

    def model_convert_iso4(self) -> ISO4:
        return ISO4(
            id=self.metadataIdentifier.MD_Identifier.code.CharacterString,
        )
